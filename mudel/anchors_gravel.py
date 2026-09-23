"""
Kruusa ankrud.

Kruus oli pikka aega mudeli suurim auk: mu_gravel = 0,50 oli puhas
oletus, mille taga ei olnud ainsatki mõõtmist. Rehviajakirjad kruusal
pidurdusmaad EI MÕÕDA -- ADAC-i all-terrain testis on kruusal ainult
kurvirada ja veojõud 20-50 km/h, pidurdus käib asfaldil. Andmed tulid
lõpuks hoopis liiklusõnnetuste ekspertiisi ja regulaatorite maailmast.

KÕIGE OLULISEM LEID: kruusal on ABS-iga pidurdusmaa PIKEM kui ABS-ita.
See on vastupidine kõigile teistele pindadele ja mudelis oli see enne
täpselt tagurpidi. Põhjus on füüsikaline: lukustatud ratas kaevub
kruusa sisse ja lükkab enda ette valli, mis on omaette pidurdusjõud.
ABS hoiab ratta veerlemas ja seda valli ei teki.

Allikad:

  [ESV98] Macnabb, Ribarits, Mortimer & Chafe, "ABS Performance on
          Gravel Roads", ESV 98-S2-W-36, 16. ESV konverents.
          UBC / Transport Canada / RCMP.
          6 ABS-iga autot + 1 ilma, u 50 km/h, ABS sisse JA välja,
          värskelt greideritud lahtine kruus (sõelanalüüs: 22,6 %
          kruus, 64,5 % liiv, 13,0 % peenosised), kalle -1,5...-1,8 %,
          kuiv, tuulevaikne, 15 °C. Vähemalt 3 katset olukorra kohta.
          G-analyst mõõtis aeglustuse OTSE: ABS väljas 0,59-0,66 g,
          ABS sees 0,37-0,52 g. "In no test did the ABS provide equal
          or higher deceleration values."
          https://www-nrd.nhtsa.dot.gov/pdf/esv/esv16/98s2w36.pdf

  [SATC19] Proctor-Parker & Stopforth, "Experimental Skid Analysis of a
          Vehicle on a Gravel Road", 38. Southern African Transport
          Conference, 2019. VW Polo Vivo 2019 (läbisõit 188 km), VBox
          Lite, TIHEDALT TALLATUD kruusatee Durbanis, kuiv, greideritud
          paar nädalat varem. Kolm rehviseisundit, kolm kiirust,
          ABS sees ja väljas. See on ainus leitud allikas, kus kruusal
          on mõõdetud KIIRUSEVAHEMIK -- just see lubab kontrollida,
          kas kruusal on kiirusest sõltuvust (ei ole).
          https://repository.up.ac.za/bitstreams/
          5f8c54b1-71fd-4791-85bc-55b5e8ec52da/download

  [SA4X4] SA4x4 ajakiri, veebruar 2018, 17 all-terrain rehvi.
          Ford Ranger FX4, 265/65 R17, 2,4 bar, 80->0 km/h, VBox,
          19-23 °C, Klipbokkop. Rada pühiti iga katse järel puhtaks.
          KÕVA, tihe kruus -- selgelt haardevam kui [ESV98] lahtine.
          Kogu 17 rehvi hajuvus on ainult 34,73-38,31 m ehk 10 %:
          kruusal on rehvivalik teisejärguline, pinna seisund ja ABS
          on kordades tähtsamad.
          https://blobs.generaltire-tyres.com/www8/servlet/blob/2497540/
          0563de3a88612760cbed33eb1a2cb50d/best-sa-all-terrain-tyre-data.pdf

  [NHTSA99] Forkenbrock & Garrott, SAE 1999-01-1287. 9 autot, 56 km/h,
          lahtine kruus (#617 purustatud lubjakivi, 5,1 cm sügavuselt).
          ABS pikendas pidurdusmaad KÕIGIL üheksal: +24,6 % täiskoormaga,
          +30,0 % kergelt koormatuna. Absoluutnumbrid on ainult
          tulpdiagrammil, seega siin kasutatakse ainult SUHET.
          https://www.nhtsa.gov/sites/nhtsa.dot.gov/files/sae1999-01-1287.pdf

KÕIGE OLULISEM LEID NR 2 (lisatud hiljem, [SA4X4] andmetest):
kruusal EI SAA rehve järjestada asfaldi järgi. Sama test mõõtis kõiki
17 rehvi MÕLEMAL pinnal ja järjestus oli peaaegu vastupidine --
astaku korrelatsioon u -0,5. Asfaldil halvim (BF Goodrich, 52,60 m)
oli kruusal teine parim (35,02 m); asfaldil teine (Cooper, 45,88 m)
oli kruusal viimane (38,31 m). Rehvi vahe kruusal on olemas (10 %),
aga mudelil EI OLE ühtegi sisendit, millest seda tuletada -- tema
ainus rehvipõhine number on märghaarde G, ja just see on see, mis
siin vastassuunas eksitab. Seepärast ei paku mudel kruusal
rehvijärjestust ja leht ütleb selle otse välja.

MIDA SIIN EI OLE: märg kruus, külmunud kruus, liiv, talverehvid kruusal.
Ühtegi mõõtmist ei leitud. Kõik allpool on KUIV kruus 15-23 °C juures.
Otsitud on inglise, saksa, rootsi, soome, vene ja eesti keeles. Kaks
uuringut, mis wet-vs-dry kruusa kindlasti sisaldavad -- Koorey & Cenek
1999 (Uus-Meremaa, instrumenteeritud sõiduk katmata teedel) ja Shoop &
Kestler 2015 (TRR 2472, US Army CRREL) -- on mõlemad tasumüüri taga.
Shoop & Kestler ise soovitavad edasisi mõõtmisi "a wider range of tires
and vehicles" peal, ehk 2015. aastal pidas selle valdkonna juhtiv
asutus rehvivariatsiooni küsimust kruusal LAHTISEKS.
"""

# See fail on PUHAS ANDMEFAIL -- Anchor-objektid ehitab anchors.py
# (_gravel), nagu ka ADAC-i failide puhul. Nii ei teki ringimporti.

SATC_ROWS = [
    # (kiirus, muster mm, ABS sees?, mõõdetud m)
    (40.0, 7.7, True,  11.930),
    (40.0, 2.9, True,  14.770),
    (40.0, 1.1, True,  16.667),
    (40.0, 7.7, False, 10.125),
    (40.0, 2.9, False, 11.833),
    (40.0, 1.1, False, 11.867),
    (60.0, 7.7, True,  31.670),
    (60.0, 2.9, True,  31.857),
    (60.0, 1.1, True,  35.143),
    (60.0, 7.7, False, 23.273),
    (60.0, 2.9, False, 25.667),
    (60.0, 1.1, False, 25.533),
    (80.0, 7.7, True,  51.812),
    (80.0, 2.9, True,  55.800),
    (80.0, 1.1, True,  58.445),
    (80.0, 7.7, False, 39.275),
    (80.0, 2.9, False, 45.800),
    (80.0, 1.1, False, 44.909),
]

SA4X4_ROWS = [
    ("velocity_raptor_at", 34.73), ("bfg_ko2", 35.02),
    ("dunlop_at3m", 35.32), ("conti_crosscontact_at", 35.38),
    ("firestone_destination_at", 35.88), ("yokohama_geolandar", 36.01),
    ("michelin_ltx_at2", 36.34), ("bridgestone_dueler_694", 36.50),
    ("goodyear_wrangler_at", 36.67), ("kumho_at51", 36.69),
    ("dunlop_at3g", 36.77), ("general_grabber_at3", 37.01),
    ("hankook_dynapro_atm", 37.26), ("pirelli_scorpion_atr", 37.46),
    ("gtradial_adventuro_at3", 37.77), ("nexen_roadian_ra8", 38.07),
    ("cooper_discoverer_at3", 38.31),
]

# --- [ESV98] otse mõõdetud aeglustused, mitte pidurdusmaad ----------------
# Neid ei saa Anchor-ina kasutada (pidurdusmaad on autospetsiifilised ja
# rehve ei avaldatud), aga need on RISTKONTROLL mudeli kruusa-mu jaoks.
ESV98_DECEL_G = {
    "abs_off": (0.59, 0.66),
    "abs_on": (0.37, 0.52),
}
# [NHTSA99] sõltumatu kinnitus samale suhtele, 9 autot, 56 km/h
NHTSA99_ABS_PENALTY = (0.246, 0.300)   # täiskoormaga, kergelt koormatuna
