-- Online-Funktionen für die Spiele (Klassenrangliste, Wunsch- und Fehlerliste)
-- Einmal im Supabase-Projekt ausführen: SQL Editor → New query → alles einfügen → Run.
-- Das Skript kann gefahrlos mehrmals ausgeführt werden.
--
-- WICHTIG: In der letzten Zeile dieses Skripts das Lehrer-Kennwort eintragen.

create table if not exists wq_config (
  key text primary key,
  value text not null
);

create table if not exists wq_classes (
  code text primary key,
  app text not null,
  name text not null,
  created_at timestamptz not null default now()
);

create table if not exists wq_scores (
  class_code text not null references wq_classes(code) on delete cascade,
  player_id uuid not null,
  secret_hash text not null,
  name text not null,
  cls int not null default 0,
  xp int not null default 0,
  levels int not null default 0,
  wins int not null default 0,
  updated_at timestamptz not null default now(),
  primary key (class_code, player_id)
);

create table if not exists wq_feedback (
  id bigint generated always as identity primary key,
  app text not null,
  kind text not null,
  body text not null,
  ctx jsonb,
  image text,
  name text,
  class_code text,
  done boolean not null default false,
  created_at timestamptz not null default now()
);

-- Niemand darf direkt auf die Tabellen zugreifen. Alles läuft über die Funktionen unten.
alter table wq_config enable row level security;
alter table wq_classes enable row level security;
alter table wq_scores enable row level security;
alter table wq_feedback enable row level security;

create or replace function wq_h(t text) returns text
language sql immutable as $$ select encode(sha256(convert_to(coalesce(t, ''), 'UTF8')), 'hex') $$;

-- Prüft das Lehrer-Kennwort. Bei falschem Kennwort kurze Pause gegen Durchprobieren.
create or replace function wq_admin(p_admin text) returns void
language plpgsql security definer set search_path = public as $$
begin
  if not exists (select 1 from wq_config where key = 'admin_hash' and value = wq_h(p_admin)) then
    perform pg_sleep(0.5);
    raise exception 'KENNWORT_FALSCH';
  end if;
end $$;

create or replace function wq_admin_check(p_admin text) returns boolean
language plpgsql security definer set search_path = public as $$
begin perform wq_admin(p_admin); return true; end $$;

-- ---------- Klassen ----------
create or replace function wq_class_create(p_admin text, p_app text, p_name text) returns text
language plpgsql security definer set search_path = public as $$
declare c text; abc text := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; i int;
begin
  perform wq_admin(p_admin);
  if length(trim(coalesce(p_name, ''))) < 1 then raise exception 'NAME_FEHLT'; end if;
  loop
    c := '';
    for i in 1..5 loop c := c || substr(abc, 1 + floor(random() * length(abc))::int, 1); end loop;
    exit when not exists (select 1 from wq_classes where code = c);
  end loop;
  insert into wq_classes(code, app, name) values (c, coalesce(p_app, ''), left(trim(p_name), 40));
  return c;
end $$;

create or replace function wq_class_list(p_admin text, p_app text)
returns table(code text, name text, created_at timestamptz, players bigint, xp bigint)
language plpgsql security definer set search_path = public as $$
begin
  perform wq_admin(p_admin);
  return query
    select k.code, k.name, k.created_at,
           (select count(*) from wq_scores s where s.class_code = k.code),
           (select coalesce(sum(s.xp), 0) from wq_scores s where s.class_code = k.code)
    from wq_classes k where k.app = p_app order by k.created_at desc;
end $$;

create or replace function wq_class_delete(p_admin text, p_code text) returns boolean
language plpgsql security definer set search_path = public as $$
begin
  perform wq_admin(p_admin);
  delete from wq_classes where code = upper(p_code);
  return found;
end $$;

create or replace function wq_player_remove(p_admin text, p_code text, p_player uuid) returns boolean
language plpgsql security definer set search_path = public as $$
begin
  perform wq_admin(p_admin);
  delete from wq_scores where class_code = upper(p_code) and player_id = p_player;
  return found;
end $$;

-- Rangliste einer Klasse. Wer den Code kennt, darf sie lesen.
create or replace function wq_board(p_code text) returns json
language plpgsql security definer set search_path = public as $$
declare k wq_classes%rowtype;
begin
  select * into k from wq_classes where code = upper(p_code);
  if not found then raise exception 'KLASSE_UNBEKANNT'; end if;
  return json_build_object(
    'code', k.code, 'name', k.name,
    'board', coalesce((select json_agg(json_build_object('id', s.player_id, 'name', s.name, 'cls', s.cls, 'xp', s.xp, 'levels', s.levels, 'wins', s.wins, 'at', s.updated_at)
                       order by s.xp desc, s.levels desc, s.updated_at)
                       from wq_scores s where s.class_code = k.code), '[]'::json));
end $$;

-- Beitreten und Stand melden in einem Schritt. Gibt die aktuelle Rangliste zurück.
create or replace function wq_sync(p_code text, p_player uuid, p_secret text, p_name text, p_cls int, p_xp int, p_levels int, p_wins int) returns json
language plpgsql security definer set search_path = public as $$
declare c text := upper(trim(coalesce(p_code, ''))); h text;
begin
  if not exists (select 1 from wq_classes where code = c) then raise exception 'KLASSE_UNBEKANNT'; end if;
  if length(coalesce(p_secret, '')) < 16 or length(trim(coalesce(p_name, ''))) < 1 then raise exception 'ANGABEN_FEHLEN'; end if;
  select secret_hash into h from wq_scores where class_code = c and player_id = p_player;
  if not found then
    if (select count(*) from wq_scores where class_code = c) >= 80 then raise exception 'KLASSE_VOLL'; end if;
    insert into wq_scores(class_code, player_id, secret_hash, name, cls, xp, levels, wins)
    values (c, p_player, wq_h(p_secret), left(trim(p_name), 20), greatest(0, least(9, coalesce(p_cls, 0))),
            greatest(0, least(2000000, coalesce(p_xp, 0))), greatest(0, least(200, coalesce(p_levels, 0))), greatest(0, least(100000, coalesce(p_wins, 0))));
  elsif h = wq_h(p_secret) then
    update wq_scores set name = left(trim(p_name), 20), cls = greatest(0, least(9, coalesce(p_cls, 0))),
      xp = greatest(0, least(2000000, coalesce(p_xp, 0))), levels = greatest(0, least(200, coalesce(p_levels, 0))),
      wins = greatest(0, least(100000, coalesce(p_wins, 0))), updated_at = now()
    where class_code = c and player_id = p_player;
  else
    raise exception 'NICHT_ERLAUBT';
  end if;
  return wq_board(c);
end $$;

create or replace function wq_leave(p_code text, p_player uuid, p_secret text) returns boolean
language plpgsql security definer set search_path = public as $$
begin
  delete from wq_scores where class_code = upper(p_code) and player_id = p_player and secret_hash = wq_h(p_secret);
  return found;
end $$;

-- ---------- Wunsch- und Fehlerliste ----------
create or replace function wq_feedback_add(p_app text, p_kind text, p_body text, p_ctx jsonb, p_image text, p_name text, p_code text) returns bigint
language plpgsql security definer set search_path = public as $$
declare n bigint;
begin
  if length(trim(coalesce(p_body, ''))) < 3 then raise exception 'TEXT_FEHLT'; end if;
  if length(coalesce(p_image, '')) > 700000 then raise exception 'BILD_ZU_GROSS'; end if;
  if (select count(*) from wq_feedback where created_at > now() - interval '1 hour') >= 60 then raise exception 'ZU_VIELE_MELDUNGEN'; end if;
  insert into wq_feedback(app, kind, body, ctx, image, name, class_code)
  values (left(coalesce(p_app, ''), 40), case when p_kind = 'fehler' then 'fehler' else 'wunsch' end, left(trim(p_body), 3000), p_ctx,
          nullif(p_image, ''), left(coalesce(p_name, ''), 20), left(upper(coalesce(p_code, '')), 8))
  returning id into n;
  return n;
end $$;

create or replace function wq_feedback_list(p_admin text, p_app text)
returns table(id bigint, kind text, body text, ctx jsonb, has_image boolean, name text, class_code text, done boolean, created_at timestamptz)
language plpgsql security definer set search_path = public as $$
begin
  perform wq_admin(p_admin);
  return query select f.id, f.kind, f.body, f.ctx, f.image is not null, f.name, f.class_code, f.done, f.created_at
    from wq_feedback f where f.app = p_app order by f.done, f.created_at desc limit 300;
end $$;

create or replace function wq_feedback_image(p_admin text, p_id bigint) returns text
language plpgsql security definer set search_path = public as $$
declare t text;
begin
  perform wq_admin(p_admin);
  select image into t from wq_feedback where id = p_id;
  return t;
end $$;

create or replace function wq_feedback_set(p_admin text, p_id bigint, p_done boolean) returns boolean
language plpgsql security definer set search_path = public as $$
begin
  perform wq_admin(p_admin);
  update wq_feedback set done = p_done where id = p_id;
  return found;
end $$;

create or replace function wq_feedback_delete(p_admin text, p_id bigint) returns boolean
language plpgsql security definer set search_path = public as $$
begin
  perform wq_admin(p_admin);
  delete from wq_feedback where id = p_id;
  return found;
end $$;

-- Die Spiele rufen die Funktionen mit dem öffentlichen Schlüssel auf.
grant execute on function wq_admin_check(text), wq_class_create(text, text, text), wq_class_list(text, text), wq_class_delete(text, text),
  wq_player_remove(text, text, uuid), wq_board(text), wq_sync(text, uuid, text, text, int, int, int, int), wq_leave(text, uuid, text),
  wq_feedback_add(text, text, text, jsonb, text, text, text), wq_feedback_list(text, text), wq_feedback_image(text, bigint),
  wq_feedback_set(text, bigint, boolean), wq_feedback_delete(text, bigint) to anon, authenticated;
revoke execute on function wq_admin(text) from public, anon, authenticated;

-- ---------- Update 1 (Klassenstufe), bei Neuinstallation gleich mit ausgeführt ----------

alter table wq_classes add column if not exists stufe int not null default 0;

drop function if exists wq_class_create(text, text, text);
drop function if exists wq_class_list(text, text);

create or replace function wq_class_create(p_admin text, p_app text, p_name text, p_stufe int) returns text
language plpgsql security definer set search_path = public as $$
declare c text; abc text := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; i int;
begin
  perform wq_admin(p_admin);
  if length(trim(coalesce(p_name, ''))) < 1 then raise exception 'NAME_FEHLT'; end if;
  loop
    c := '';
    for i in 1..5 loop c := c || substr(abc, 1 + floor(random() * length(abc))::int, 1); end loop;
    exit when not exists (select 1 from wq_classes where code = c);
  end loop;
  insert into wq_classes(code, app, name, stufe) values (c, coalesce(p_app, ''), left(trim(p_name), 40), greatest(0, least(9, coalesce(p_stufe, 0))));
  return c;
end $$;

create or replace function wq_class_list(p_admin text, p_app text)
returns table(code text, name text, stufe int, created_at timestamptz, players bigint, xp bigint)
language plpgsql security definer set search_path = public as $$
begin
  perform wq_admin(p_admin);
  return query
    select k.code, k.name, k.stufe, k.created_at,
           (select count(*) from wq_scores s where s.class_code = k.code),
           (select coalesce(sum(s.xp), 0) from wq_scores s where s.class_code = k.code)
    from wq_classes k where k.app = p_app order by k.created_at desc;
end $$;

-- Klassenstufe ändern, zum Beispiel beim Wechsel ins nächste Schuljahr
create or replace function wq_class_set_stufe(p_admin text, p_code text, p_stufe int) returns boolean
language plpgsql security definer set search_path = public as $$
begin
  perform wq_admin(p_admin);
  update wq_classes set stufe = greatest(0, least(9, coalesce(p_stufe, 0))) where code = upper(p_code);
  return found;
end $$;

create or replace function wq_board(p_code text) returns json
language plpgsql security definer set search_path = public as $$
declare k wq_classes%rowtype;
begin
  select * into k from wq_classes where code = upper(p_code);
  if not found then raise exception 'KLASSE_UNBEKANNT'; end if;
  return json_build_object(
    'code', k.code, 'name', k.name, 'stufe', k.stufe,
    'board', coalesce((select json_agg(json_build_object('id', s.player_id, 'name', s.name, 'cls', s.cls, 'xp', s.xp, 'levels', s.levels, 'wins', s.wins, 'at', s.updated_at)
                       order by s.xp desc, s.levels desc, s.updated_at)
                       from wq_scores s where s.class_code = k.code), '[]'::json));
end $$;

grant execute on function wq_class_create(text, text, text, int), wq_class_list(text, text), wq_class_set_stufe(text, text, int), wq_board(text) to anon, authenticated;

-- ---------- Update 2 (Kennwort ändern), bei Neuinstallation gleich mit ausgeführt ----------

create or replace function wq_admin_change(p_admin text, p_new text) returns boolean
language plpgsql security definer set search_path = public as $$
begin
  perform wq_admin(p_admin);
  if length(coalesce(p_new, '')) < 8 then raise exception 'KENNWORT_ZU_KURZ'; end if;
  update wq_config set value = wq_h(p_new) where key = 'admin_hash';
  return found;
end $$;

grant execute on function wq_admin_change(text, text) to anon, authenticated;

-- ---------- Update 3 (Einstellungen online), bei Neuinstallation gleich mit ausgeführt ----------

create table if not exists wq_settings (
  app text primary key,
  data jsonb not null,
  updated_at timestamptz not null default now()
);
alter table wq_settings enable row level security;

-- Lesen darf jedes Gerät, damit die Einstellungen auch bei den Schülern gelten.
create or replace function wq_settings_get(p_app text) returns jsonb
language sql security definer set search_path = public as $$
  select data from wq_settings where app = p_app
$$;

-- Ändern nur mit dem Lehrer-Kennwort.
create or replace function wq_settings_set(p_admin text, p_app text, p_data jsonb) returns boolean
language plpgsql security definer set search_path = public as $$
begin
  perform wq_admin(p_admin);
  if p_data is null or jsonb_typeof(p_data) <> 'object' or length(p_data::text) > 2000 then raise exception 'EINSTELLUNGEN_UNGUELTIG'; end if;
  insert into wq_settings(app, data, updated_at) values (left(coalesce(p_app, ''), 40), p_data, now())
  on conflict (app) do update set data = excluded.data, updated_at = now();
  return true;
end $$;

grant execute on function wq_settings_get(text), wq_settings_set(text, text, jsonb) to anon, authenticated;

-- ===== HIER DAS LEHRER-KENNWORT EINTRAGEN (zwischen den Hochkommas), dann Run =====
insert into wq_config(key, value) values ('admin_hash', wq_h('HIER-EIN-LANGES-KENNWORT-EINTRAGEN'))
on conflict (key) do update set value = excluded.value;
