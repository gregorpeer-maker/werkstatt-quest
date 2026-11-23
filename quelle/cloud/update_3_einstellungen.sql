-- Update 3: Einstellungen des Lehrer-Bereichs online speichern. Sie gelten dann auf allen Geräten.
-- Einmal im Supabase SQL Editor ausführen (Inhalt einfügen, Run). Darf mehrmals ausgeführt werden.

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
