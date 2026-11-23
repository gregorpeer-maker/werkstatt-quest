-- Update 4: Spielstand online sichern und auf mehreren Geräten weiterspielen.
-- Einmal im Supabase SQL Editor ausführen (Inhalt einfügen, Run). Darf mehrmals ausgeführt werden.

create table if not exists wq_progress (
  player_id uuid primary key,
  secrets text[] not null,
  name text not null,
  data jsonb not null,
  updated_at timestamptz not null default now()
);
alter table wq_progress enable row level security;

create table if not exists wq_links (
  code text primary key,
  player_id uuid not null references wq_progress(player_id) on delete cascade,
  expires timestamptz not null
);
alter table wq_links enable row level security;

-- Gehört dieses Geräte-Geheimnis zu diesem Spieler?
create or replace function wq_owner(p_player uuid, p_secret text) returns boolean
language sql security definer set search_path = public as $$
  select exists (select 1 from wq_progress where player_id = p_player and wq_h(p_secret) = any(secrets))
$$;

create or replace function wq_progress_load(p_player uuid, p_secret text) returns json
language plpgsql security definer set search_path = public as $$
declare r wq_progress%rowtype;
begin
  select * into r from wq_progress where player_id = p_player;
  if not found then return null; end if;
  if not (wq_h(p_secret) = any(r.secrets)) then raise exception 'NICHT_ERLAUBT'; end if;
  return json_build_object('name', r.name, 'data', r.data);
end $$;

create or replace function wq_progress_save(p_player uuid, p_secret text, p_name text, p_data jsonb) returns boolean
language plpgsql security definer set search_path = public as $$
declare r wq_progress%rowtype;
begin
  if length(coalesce(p_secret, '')) < 16 or length(trim(coalesce(p_name, ''))) < 1 then raise exception 'ANGABEN_FEHLEN'; end if;
  if p_data is null or jsonb_typeof(p_data) <> 'object' or length(p_data::text) > 400000 then raise exception 'SPIELSTAND_UNGUELTIG'; end if;
  select * into r from wq_progress where player_id = p_player;
  if not found then
    insert into wq_progress(player_id, secrets, name, data) values (p_player, array[wq_h(p_secret)], left(trim(p_name), 20), p_data);
  elsif wq_h(p_secret) = any(r.secrets) then
    update wq_progress set name = left(trim(p_name), 20), data = p_data, updated_at = now() where player_id = p_player;
  else
    raise exception 'NICHT_ERLAUBT';
  end if;
  return true;
end $$;

-- Kurzer Code (15 Minuten gültig, nur einmal verwendbar), um ein weiteres Gerät zu verbinden
create or replace function wq_link_create(p_player uuid, p_secret text) returns text
language plpgsql security definer set search_path = public as $$
declare c text; abc text := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; i int;
begin
  if not wq_owner(p_player, p_secret) then raise exception 'NICHT_ERLAUBT'; end if;
  delete from wq_links where expires < now() or player_id = p_player;
  loop
    c := '';
    for i in 1..6 loop c := c || substr(abc, 1 + floor(random() * length(abc))::int, 1); end loop;
    exit when not exists (select 1 from wq_links where code = c);
  end loop;
  insert into wq_links(code, player_id, expires) values (c, p_player, now() + interval '15 minutes');
  return c;
end $$;

create or replace function wq_link_use(p_code text) returns json
language plpgsql security definer set search_path = public as $$
declare l wq_links%rowtype; r wq_progress%rowtype; s text;
begin
  select * into l from wq_links where code = upper(trim(coalesce(p_code, ''))) and expires > now();
  if not found then perform pg_sleep(0.5); raise exception 'CODE_UNGUELTIG'; end if;
  delete from wq_links where code = l.code;
  s := md5(random()::text || clock_timestamp()::text) || md5(random()::text || l.code);
  update wq_progress set secrets = (secrets[greatest(1, array_length(secrets, 1) - 8):] || wq_h(s)) where player_id = l.player_id
  returning * into r;
  return json_build_object('player', r.player_id, 'secret', s, 'name', r.name, 'data', r.data);
end $$;

-- Klassenrangliste: Ein verbundenes Gerät darf denselben Platz in der Klasse aktualisieren
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
  elsif h = wq_h(p_secret) or wq_owner(p_player, p_secret) then
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
  delete from wq_scores where class_code = upper(p_code) and player_id = p_player and (secret_hash = wq_h(p_secret) or wq_owner(p_player, p_secret));
  return found;
end $$;

grant execute on function wq_progress_load(uuid, text), wq_progress_save(uuid, text, text, jsonb), wq_link_create(uuid, text), wq_link_use(text),
  wq_sync(text, uuid, text, text, int, int, int, int), wq_leave(text, uuid, text) to anon, authenticated;
revoke execute on function wq_owner(uuid, text) from public, anon, authenticated;
