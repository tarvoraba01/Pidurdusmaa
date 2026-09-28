# Järgmised autod (2026-09-28, kaheksas ring tehtud)

Seitsmendas ringis lisati 128 ja kaheksandas 143 autot (vehicles_ee.py "seitsmes ring" ja
"kaheksas ring"); kokku on nüüd 1030 autot. Need jäid välja, sest olulised andmed jäid
kinnitamata (reegel: mitte midagi välja mõelda). Veebiotsingu limiit (200 sessiooni kohta)
sai kaheksanda ringi keskel täis, osa neist võib uues sessioonis leida.

## Seitsmendast ringist

- `ford_transit_custom_2` — Ford Transit Custom II (2023+): kaubiku kõrgus, teljevahe ja mass kinnitamata.
- `mg_hs_2` — MG HS II (2024+): tehase rehvimõõtu ei leitud, teljevahe puudu.

## Kaheksandast ringist

- `audi_q5_3` — Audi Q5 III 2.0 TDI (2024+): puudu: kerb_kg, height_m
- `citroen_jumper_2` — Citroën Jumper II 2.0 HDi (1994-2006): puudu: kerb_kg, width_m, height_m, wheelbase_m
- `fiat_ducato_2` — Fiat Ducato II 2.8 JTD (1994-2006): puudu: width_m
- `ford_escort_4` — Ford Escort Mk4 1.4 (1986-1990): puudu: kerb_kg, width_m, height_m, wheelbase_m
- `ford_transit_6` — Ford Transit VI 2.4 TDCi (2000-2006): puudu: kerb_kg, width_m, height_m, wheelbase_m
- `hyundai_accent_2` — Hyundai Accent II 1.3 (1999-2006): baasmõõt puudub; puudu: kerb_kg, width_m, height_m, wheelbase_m
- `mb_vito_w638` — Mercedes-Benz Vito W638 2.2 CDI (1996-2003): puudu: kerb_kg, wheelbase_m
- `mb_sprinter_901` — Mercedes Sprinter 901 2.2 CDI (1995-2006): puudu: kerb_kg
- `mb_g_w463_1` — Mercedes G350d W463 (1990-2018): puudu: kerb_kg
- `nissan_navara_d22` — Nissan Navara D22 2.5 dCi (1997-2005): baasmõõt puudub; puudu: kerb_kg
- `nissan_murano_z50` — Nissan Murano Z50 3.5 (2003-2008): puudu: kerb_kg
- `nissan_sunny_n13` — Nissan Sunny N13 1.6 (1986-1990): puudu: wheelbase_m
- `opel_corsa_a` — Opel Corsa A 1.2 (1982-1993): puudu: wheelbase_m
- `opel_movano_a` — Opel Movano A 2.5 CDTI (1998-2010): puudu: kerb_kg
- `opel_movano_c` — Opel Movano C 2.2 BlueHDi (2021+): baasmõõt puudub; puudu: kerb_kg, width_m, height_m, wheelbase_m
- `peugeot_boxer_2` — Peugeot Boxer II 2.8 HDi (1994-2006): puudu: kerb_kg, width_m, height_m, wheelbase_m
- `renault_master_2` — Renault Master II 2.5 dCi (1998-2010): puudu: kerb_kg
- `renault_trafic_1` — Renault Trafic I 2.1 D (1980-2001): puudu: height_m, wheelbase_m
- `suzuki_grandvitara_1` — Suzuki Grand Vitara I 2.0 (1998-2005): puudu: kerb_kg, width_m, height_m
- `suzuki_swift_2` — Suzuki Swift II 1.3 (1989-2003): puudu: kerb_kg
- `toyota_hilux_6` — Toyota Hilux VI 2.5 D-4D (1997-2005): puudu: kerb_kg, width_m, height_m, wheelbase_m
- `toyota_carina_2` — Toyota Carina II 1.6 (1987-1992): puudu: kerb_kg, width_m, height_m
- `vw_caddy_2` — VW Caddy II 1.9 SDI (1996-2004): puudu: wheelbase_m
- `volvo_740` — Volvo 740 2.3 (1984-1992): puudu: wheelbase_m
- `skoda_120` — Škoda 120 1.2 (1976-1990): baasmõõt puudub; puudu: wheelbase_m

Reeglid uurimisel: ainult WebSearch/WebFetch; wheel-size.com ja wheel-sizes.com keelatud;
Euroopa versioonid; esi- ja tagamõõdu erinevus märkida (mudel kasutab esimõõtu);
kaubikutel ainult tühja sõiduki rõhk; mitte midagi välja mõelda.
