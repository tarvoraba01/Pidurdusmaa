-- Pidurdusmaa.ee — Supabase skeem
--
-- Kuidas kasutada: Supabase → SQL Editor → kleebi kogu fail → Run.
-- Faili võib käivitada mitu korda (kõik on "if not exists" / "or replace").
--
-- Turvalisus:
--  * Kõigil tabelitel on RLS sees ja ühtegi poliitikat pole → avaliku
--    (anon/publishable) võtmega ei saa ühtegi tabelit lugeda ega kirjutada.
--  * Server kasutab salajast võtit (SUPABASE_SECRET_KEY), mis RLS-ist mööda läheb.
--    See võti on ainult Coolify keskkonnamuutujas, mitte kunagi koodis ega brauseris.
--  * Avaliku võtmega saab kutsuda AINULT funktsiooni failsafe_bump()
--    (GitHub Actions, vt .github/workflows/supabase-failsafe.yml).

-- 1. Anonüümne kasutuslogi (endine logi.jsonl) -----------------------------
create table if not exists public.kasutuslogi (
	id bigint generated always as identity primary key,
	t timestamptz not null default now(),
	k text,            -- sessiooni räsi päeva soolaga (IP-d ei ole)
	s real,            -- sekundit lehe avamisest
	e text not null,   -- sündmus
	v text             -- väärtus
);
create index if not exists kasutuslogi_t on public.kasutuslogi (t);
alter table public.kasutuslogi enable row level security;

-- 2. Kontaktivormi kirjad (endine kontakt.jsonl) — isikuandmed, hoitakse 12 kuud
create table if not exists public.kontakt (
	id bigint generated always as identity primary key,
	aeg timestamptz not null default now(),
	teema text,
	nimi text,
	email text,
	firma text,
	sonum text
);
create index if not exists kontakt_aeg on public.kontakt (aeg);
alter table public.kontakt enable row level security;

-- 3. Pakkujate puhver: viimane õnnestunud kataloog (taastub serveri restardil)
create table if not exists public.pakkumised_hetktommis (
	pakkuja text primary key,
	laetud timestamptz not null,
	info jsonb,
	andmed jsonb not null  -- { "20555R16": [ {mark, mudel, hind, ...}, ... ], ... }
);
alter table public.pakkumised_hetktommis enable row level security;

-- 4. Hinnaajalugu: rida ainult siis, kui hind või laoseis muutus (või toode on uus)
create table if not exists public.hinnaajalugu (
	id bigint generated always as identity primary key,
	t timestamptz not null default now(),
	pakkuja text not null,
	voti text not null,
	moot text not null,
	mark text,
	mudel text,
	hind numeric(10, 2) not null,
	kogus integer
);
create index if not exists hinnaajalugu_voti_t on public.hinnaajalugu (pakkuja, voti, t);
alter table public.hinnaajalugu enable row level security;

-- 5. Serveri väike olek (nt IndexNow: mis aadressid on juba teatatud)
create table if not exists public.seis (
	voti text primary key,
	vaartus jsonb not null,
	uuendatud timestamptz not null default now()
);
alter table public.seis enable row level security;

-- 6. Failsafe: Supabase'i tasuta projekt pannakse pausile pärast 7 päeva
--    vaikust. Server (iga päev) ja GitHub Actions (2× nädalas) kutsuvad
--    failsafe_bump() — write_count kasvab +1 kord nädalas (ISO nädal).
create table if not exists public."supabase-free-failsafe" (
	name text primary key,
	write_count integer not null default 1,
	nadal text not null default to_char(now() at time zone 'utc', 'IYYY-IW'),
	uuendatud timestamptz not null default now(),
	allikas text
);
insert into public."supabase-free-failsafe" (name) values ('failsafe') on conflict (name) do nothing;
alter table public."supabase-free-failsafe" enable row level security;

create or replace function public.failsafe_bump(p_allikas text default 'server')
returns integer
language plpgsql
security definer
set search_path = public
as $$
declare
	v_nadal text := to_char(now() at time zone 'utc', 'IYYY-IW');
	v_count integer;
begin
	insert into public."supabase-free-failsafe" (name, write_count, nadal, allikas)
	values ('failsafe', 1, v_nadal, left(coalesce(p_allikas, '?'), 40))
	on conflict (name) do update set
		write_count = public."supabase-free-failsafe".write_count
			+ case when public."supabase-free-failsafe".nadal <> v_nadal then 1 else 0 end,
		nadal = v_nadal,
		uuendatud = now(),
		allikas = left(coalesce(p_allikas, '?'), 40)
	returning write_count into v_count;
	return v_count;
end;
$$;
revoke all on function public.failsafe_bump(text) from public;
grant execute on function public.failsafe_bump(text) to anon, service_role;

-- 7. Kasutuslogi kokkuvõte (/api/kokkuvote) — arvutatakse andmebaasis, mitte serveris
create or replace function public.kasutuslogi_kokkuvote(alates timestamptz)
returns jsonb
language sql
stable
security definer
set search_path = public
as $$
	with r as (
		select k, e, v from public.kasutuslogi where t >= alates
	),
	s as (
		select e, count(*) as n from r group by e
	),
	vv as (
		select e, v, count(*) as n,
			row_number() over (partition by e order by count(*) desc) as rn
		from r where v is not null group by e, v
	)
	select jsonb_build_object(
		'ridu', (select count(*) from r),
		'sessioone', (select count(distinct k) from r),
		'sundmused', coalesce((select jsonb_object_agg(e, n) from s), '{}'::jsonb),
		'top', coalesce((
			select jsonb_object_agg(e, arr) from (
				select e, jsonb_agg(jsonb_build_array(v, n) order by n desc) as arr
				from vv where rn <= 15 group by e
			) x
		), '{}'::jsonb)
	);
$$;
revoke all on function public.kasutuslogi_kokkuvote(timestamptz) from public, anon, authenticated;
grant execute on function public.kasutuslogi_kokkuvote(timestamptz) to service_role;

-- 6. Koolitus: õpetaja loodud grupid ja õpilaste vastused (isikuandmeid pole) ----
--    Õpetaja võtit ei hoita: ainult selle sha256 räsi. Õpilase sessioon = juhuslik id.
create table if not exists public.koolitus_grupid (
	kood text primary key,
	nimi text not null,
	teemad text[] not null,
	kysimusi int not null default 10,
	voti_rasi text not null,
	loodud timestamptz not null default now()
);
alter table public.koolitus_grupid enable row level security;

create table if not exists public.koolitus_vastused (
	id bigint generated always as identity primary key,
	aeg timestamptz not null default now(),
	kood text not null references public.koolitus_grupid (kood) on delete cascade,
	sessioon text not null,
	etapp text not null check (etapp in ('eel', 'jarel')),
	kysimus text not null,
	oige boolean not null
);
create index if not exists koolitus_vastused_kood on public.koolitus_vastused (kood, aeg);
alter table public.koolitus_vastused enable row level security;
