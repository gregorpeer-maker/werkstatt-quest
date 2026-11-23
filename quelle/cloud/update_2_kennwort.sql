-- Update 2: Lehrer-Kennwort im Spiel ändern. Das Kennwort gilt dann auf allen Geräten.
-- Einmal im Supabase SQL Editor ausführen (Inhalt einfügen, Run). Darf mehrmals ausgeführt werden.
-- Das aktuelle Kennwort bleibt dabei unverändert.

create or replace function wq_admin_change(p_admin text, p_new text) returns boolean
language plpgsql security definer set search_path = public as $$
begin
  perform wq_admin(p_admin);
  if length(coalesce(p_new, '')) < 8 then raise exception 'KENNWORT_ZU_KURZ'; end if;
  update wq_config set value = wq_h(p_new) where key = 'admin_hash';
  return found;
end $$;

grant execute on function wq_admin_change(text, text) to anon, authenticated;
