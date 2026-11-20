-- Update 1: Klassenstufe pro Klasse. Neue Schüler bekommen ihre Klassenstufe über den Klassencode.
-- Einmal im Supabase SQL Editor ausführen (Inhalt einfügen, Run). Darf mehrmals ausgeführt werden.
-- Das Lehrer-Kennwort bleibt dabei unverändert.

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
