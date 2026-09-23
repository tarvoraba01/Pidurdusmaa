"""PÄRITOLUREGISTER: iga kalibratsioonikonstandi tõendus.

MIKS SEE FAIL OLEMAS ON
-----------------------
Mudelis on 62 konstanti. Osa on sobitatud mõõdetud ankrute vastu, osa
tuleb kirjandusest, osa on definitsioon, osa on ohutusklamber -- ja osa
oli lihtsalt kirjutatud, ilma et keegi oleks kunagi küsinud, kust nad
tulid. Need viimased ei tulnud välja arvustuses, vaid juhuslikult:
lumel oli kaks oletust vale suunaga, lahtisel lumel oli kordaja vale
märgiga, kruusal oli ABS tagurpidi. Iga kord leiti viga õnne, mitte
protsessiga.

See fail teeb sellest protsessi. REEGEL: iga Calibration-i väli PEAB
siin kirjas olema. audit.py kukub läbi, kui mõni väli on puudu või kui
mõni on märgitud UNSOURCED. Nii ei saa uus konstant enam vaikselt
sisse tulla.

LIIGID
------
  FITTED      numbriliselt sobitatud nimetatud ankrute vastu
  LITERATURE  nimetatud avaldatud allikast, EI OLE sobitatud
  DERIVED     definitsioon või arvutus teistest suurustest
  RESIDUAL    tuletatud mudeli enda jääkvigadest (audit kontrollib)
  CLAMP       teadlik ohutuspiir, mitte mõõtmine -- tohib olla
              ainult siis, kui ta EI MÕJUTA tavapärast vastust
  UNSOURCED   tõendus puudub -> audit kukub läbi

`anchors` väli ütleb, MITU ankrut seda konstanti kitsendavad. audit.py
kontrollib seda sõltumatult tundlikkusanalüüsiga: kui konstant liigutab
vastust, aga ükski ankur ei reageeri tema muutmisele, on ta praktikas
sobitamata, ükskõik mida see tabel väidab.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Origin:
    kind: str
    source: str
    note: str = ""
    anchors: int = 0


F, L, D, R, C, U = ("FITTED", "LITERATURE", "DERIVED",
                    "RESIDUAL", "CLAMP", "UNSOURCED")

ORIGINS: dict[str, Origin] = {

    # ---------------- Layer 2: rehv ----------------
    "k_g": Origin(
        F, "[ADAC25]+[ADACA25]+[ADACS25]+[UT25]+[TM25]",
        "mu_marg = k_G * G. Sobitatud 85 marja ankru vastu. "
        "Ristkontroll: kaks soltumatut testi (TM25, UT25) annavad sama "
        "k_G ainult uhe klassieeldusega -- vt calibrate.py VALIDEERIMINE 3.",
        anchors=85),

    "mu_dry_base": Origin(
        F, "[ADACS25] suvi / [UT25] tavasuvi / [ADACA25] lamell / "
           "[ADAC25] talv / [TM25] Pohjamaa ja naast",
        "Kategooria kohta eraldi sobitatud. Kuiv pidurdus EI OLE EL-i "
        "margisel ega tuubikinnituses -- vt standardid.md 4. jagu. "
        "Seetottu ei saa siin kunagi rehvimudeli kaupa arve olla.",
        anchors=93),

    "mu_snow_base": Origin(
        F, "[ADACA25] lamell / [ADAC25] talv / [UTAC25N] Pohjamaa / "
           "[ZR24] naast / [ADAC25]+[ADACA25] suverehvid",
        "Suverehvide lumebaas on tuletatud samade testide suverehvi "
        "ridadest; Pohjamaa ja naast said oma esimesed motmised 2026-09 "
        "(vt anchors_snow_nordic.py) ja neil on laiem veapiir.",
        anchors=56),

    "mu_ice_base": Origin(
        F, "[ADACA25] lamell / [ADAC25] talv / [TM25] Pohjamaa ja naast",
        "Suverehvi jaad keegi ei moda -- vt selle valja erikasitlust "
        "allpool failis ja mudeli enda hoiatust.",
        anchors=61),

    "mu_gravel_base": Origin(
        F, "[SATC19]", "18 motmist, VW Polo Vivo, tallatud kruus, "
        "kolm kiirust x kolm mustrit x ABS sees/valjas.", anchors=18),

    # ---------------- kiiruse mõju ----------------
    "v_ref_ms": Origin(
        D, "definitsioon", "80 km/h = 22,222 m/s. Normeerimispunkt, "
        "mille suhtes koik mu(v) avaldised on kirjutatud."),

    "k_speed_dry": Origin(
        F, "[ADACA25] 100->0 vs [ADAC25]/[ADACS25] 80->0",
        "ADACA25 marg pidurdus on 100 -> 0 km/h, teistes 80 -> 0. "
        "See on ainus koht, kus kiirusesoltuvust saab ankrutest lugeda.",
        anchors=32),

    "k_speed_snow": Origin(
        L, "Chalmers 2022; Ichihara & Mizoguchi (TRB SR115); FAA/NASA",
        "Kolm soltumatut motmistraditsiooni utlevad, et lumel ja jaal "
        "on haare kiirusest peaaegu soltumatu. Vaartus on nullilahedane "
        "just sellepairast. Ankrud on uhel kiirusel (30 km/h), seega "
        "neid ei saa selle vastu sobitada."),

    "k_speed_ice": Origin(
        L, "Chalmers 2022 (35 ja 55 km/h, vahe -0,02...+0,02 mu); "
           "Ichihara & Mizoguchi 20-60 km/h; FAA/NASA 32-95 km/h",
        "Sama pohjus mis lumel. 0,001 on praktiliselt null."),

    "wet_lift_b": Origin(
        L, "DEKRA mustrisugavus + kirjanduse mu-langus 40->100 km/h",
        "Sobitatud korraga kolme teadaoleva seose vastu, mitte ankrute "
        "vastu: DEKRA +17 % marjal, mu langus 24 % (kirjandus 20-30 %) "
        "ja realistlikud akvaplaneerimise lavid."),

    "temp_curves": Origin(
        L, "kummisegude kirjandus + [TESTWORLD] jarjestuskontroll",
        "Kujud on kirjandusest. Talverehvide kulmavoitu on VAHENDATUD, "
        "kuni mudel labis Test Worldi tunnelitesti jarjestuskontrolli "
        "(+2 C marjal peatub lamellrehv luhemalt kui talverehv). "
        "Vt calibrate_temp.py. HOIATUS: 369-st ankrust on 215 tapselt "
        "+10 C juures ja kokku on ainult 6 erinevat temperatuuri, "
        "seega ankrud neid kover praktiliselt ei kitsenda."),

    # ---------------- rõhk ----------------
    "press_opt_offset_dry": Origin(
        F, "[PASSAT]", "30 modetud suhtarvu, viga 1,3 %.", anchors=30),
    "press_k_dry": Origin(F, "[PASSAT]", "sama sobitus.", anchors=30),
    "press_k_wet_under": Origin(
        F, "[PASSAT]", "Peaaegu null: marja rohumoju kannab v_hp, mitte "
        "see liige. Kahekordset arvestamist valditakse teadlikult.",
        anchors=30),
    "press_k_wet_over": Origin(F, "[PASSAT]", "sama sobitus.", anchors=30),

    "press_abs_scale": Origin(
        L, "[MDPI25]",
        "MUDELI KOIGE JULGEM UKSIKARV: NONE = 9,16. Uks allikas, mis on "
        "osalt simulatsioon. EARLY/MODERN/LATEST = 1,0 on definitsioon "
        "(PASSAT-i sobitus tehti ABS-iga autol). Vt audit.py hoiatust."),

    # ---------------- muster ----------------
    "tread_loss_gravel": Origin(
        F, "[SATC19]", "ABS-iga haru, proportsionaalne.", anchors=9),
    "tread_loss_gravel_locked": Origin(
        F, "[SATC19]", "Lukus ratas, kullastuv.", anchors=9),
    "tread_gravel_sat_frac": Origin(
        F, "[SATC19]", "Kullastuspunkt. Leave-one-out: 1 parameeter "
        "3,83 %, 2 parameetrit 3,06 % -- ei ole ulesobitamine.",
        anchors=18),

    "tread_loss_wet_residual": Origin(
        L, "[DEKRA] + mudeli struktuur",
        "Marjal kaib mustri POHIMOJU v_hp kaudu (akvaplaneerimine). "
        "See liige on ainult JAAK -- kontaktpinna ja lamellide kadu, mis "
        "ei ole veearajuhtimine. Suurus on valitud nii, et v_hp + jaak "
        "kokku annaks DEKRA modetud +16...18 % (7-8 mm -> 2-3 mm, "
        "100 km/h). Jaagu ja v_hp jaotust eraldi ei ole modetud."),

    "tread_loss_dry_full": Origin(
        L, "[DEKRA]", "DEKRA modis kuival 7-8 mm -> 2-3 mm juures "
        "+2,4...8,5 %. 0,055 tapselt kulunud rehvi kohta annab selle "
        "vahemiku keskosa."),

    # ---------------- vanus ----------------
    "age_free_years": Origin(
        L, "ADAC/Continental vananemisuuringud",
        "Esimesed u 5 aastat ei anna modetavat kadu. "
        "HOIATUS: mudelis ei ole uhtegi vanuseankrut -- koik 369 on "
        "uued voi 1-aastased rehvid. Vt audit.py."),
    "age_loss_per_year": Origin(
        L, "ADAC/Continental vananemisuuringud", "Sama piirang."),
    "age_loss_max": Origin(
        L, "ADAC/Continental vananemisuuringud", "Sama piirang."),

    # ---------------- koormus ----------------
    "load_exp": Origin(
        F, "[ADAC25]+[ADACS25]+[ADACA25]+[UT25] koormusvariatsioon",
        "Sobitatud -0,070. SOLTUMATU RISTKONTROLL: kummi hoorde "
        "kirjandus annab mu ~ N^-0,107. Sama suurusjarku ja sama "
        "margiga, mudel on pisut konservatiivsem.", anchors=369),
    "load_ref_ratio": Origin(
        D, "definitsioon",
        "Normeerimispunkt: koormus rehvi kandevoime suhtes, mille "
        "juures load_exp-i kordaja on 1,0. Ei ole vaba parameeter."),

    # ---------------- Layer 3: tee ----------------
    # TEKSTUUR. Siin oli enne kaks lamedat kordajat ilma ühegi
    # mõõtmiseta. Audit näitas 10 % hooba nulli peal; kirjandusest
    # otsides selgus, et vale oli MUDELI KUJU, mitte arvud.
    "texture_mpd_mm": Origin(
        D, "FHWA Pavement Friction for Road Safety (tüüpvahemikud)",
        "Tasemenimede vastendus MPD-le. AUS HOIATUS: just SEE VASTENDUS "
        "on oletus -- keegi ei ole motnud, mis MPD on 'kulunud siledal' "
        "Eesti maanteel. Kuju on toendatud, vastendus mitte, ja "
        "sigma_texture kannab seda."),
    "texture_micro": Origin(
        L, "Wehner/Schulze poleerimiskatse",
        "MODETUD: enne 0,431 -> 90 000 poleerimiskaigu jarel 0,393, "
        "ehk x0,912. Liivapritsiga mikrotekstuur tagasi -> 0,679 "
        "(+73 %), mis kinnitab, et tegu on MIKRO-, mitte "
        "makrotekstuuriga. Varem oli mudelis poleerituse kaoks 0,76 -- "
        "see oli valja moeldud ja veel vales mehhanismis."),
    "ifi_sp_a": Origin(
        L, "PIARC rahvusvaheline hoordeindeks (IFI)",
        "Sp = a + b*MPD. Kuju toetavad kolm soltumatut allikat: NCHRP "
        "('macro-texture impacts the friction-speed gradient'), PIARC "
        "IFI ja TRL 367 (133 katseloiku). HOIATUS: koefitsiendid ise on "
        "norgemad kui kuju -- seadmepohised ulesobitused annavad R^2 "
        "0,05-0,39. Kuju on kindel, kalle mitte."),
    "ifi_sp_b": Origin(L, "PIARC IFI", "Sama piirang mis ifi_sp_a."),
    "ifi_ref_speed_kmh": Origin(
        D, "IFI definitsioon",
        "60 km/h on IFI poordepunkt. NORMAL-tekstuur annab siin "
        "kordajaks tapselt 1,000 IGAL kiirusel, sest ta on vordluspunkt "
        "-- nii ei muutnud kogu umberehitus uhtegi 369-st ankrust."),
    "concrete_factor": Origin(
        F, "[ADAC25]+[ADACS25]+[ADACA25] marg betoon",
        "65 punkti kolmes testis. Kategooriapohist jaotust katsetati "
        "(talv 0,870 vs muud 0,853), aga vahe oli nii vaike, et uks "
        "vaartus on ausam.", anchors=65),

    "water_k_deep": Origin(
        L, "veekile ja hoorde kirjandus + mudeli struktuur",
        "Sugavama vee STAATILINE osa. Kiirusest soltuv osa -- see, mis "
        "pairiselt loeb -- kaib v_hp kaudu. Nende kahe jaotust eraldi "
        "modetud ei ole; ankrutes on ainult uks veekile paksus (1 mm)."),
    "water_k_shallow": Origin(
        L, "veekile ja hoorde kirjandus",
        "Niiske tee on margast paremas haardes. Sama piirang: ankrutes "
        "on ainult 1 mm."),

    # ---------------- jää ja lumi temperatuur ----------------
    "ice_temp_curve": Origin(
        L, "Kandeva & Dishovsky; Balmer (TRB SR115); Hodgkinson HRR477; "
           "Martin",
        "Ehitatud kirjandusest, kontrollitud kuue avaldatud motmise "
        "vastu: viis kuuest klapib. Kalle on votetud SOIDUKI skaalalt "
        "(3,5-6 %/K), mitte labori omalt (11-14 %/K). "
        "ISO 19447 lubab jaad katsetada ainult -15...-5 C juures, "
        "seega valjaspool seda on kover ekstrapolatsioon. "
        "NB: tsiteeritud valitood on TAVAREHVIGA -- naastrehvi kohta "
        "vt ice_temp_exp."),
    "ice_temp_exp": Origin(
        F, "[VIB10D] Vi Bilagare 2010 naastrehvitest",
        "Jaa temperatuuritundlikkus kategooria kaupa. Sobitatud PAARIS-"
        "mootmiste vastu: sama 9 rehvi jaal kahel temperatuuril samal "
        "paeval (-3...-2 C ja +0,5...+1 C), nii et rehvi enda jaahaare "
        "taandub suhtest valja. Moodetud pidurdusmaa suhe soe/kulm: "
        "naastrehv 1,23 (n=7, 1,10-1,33), hoordrehv 1,69 (n=2). Vana "
        "mudel andis koigile 1,41-1,46. Ainult naastrehv sai oma astme "
        "(0,545); hoordrehvi pool n=2 pealt nouaks ohutusklambri "
        "lodvendamist ja jai tegemata. Aste mojub AINULT kaopoolel "
        "(f < 1), sest toend katab -2,5...+0,75 C. Koik 14 Pohjamaa ja "
        "naastrehvi jaaankrut on -5 C juures, kus f = 1,0 -- aste ei "
        "liiguta neid, seega mu_ice_base jarelesobitust ei olnud vaja.",
        anchors=9),
    "ice_temp_min": Origin(
        C, "ohutusklamber", "Ei ole modetud. Audit kontrollib, et ta ei "
        "aktiveeru mudeli lubatud temperatuurivahemikus."),
    "ice_temp_max": Origin(C, "ohutusklamber", "Sama."),

    "snow_temp_curve": Origin(
        L, "FAA AC 25-31; Lu/WSDOT; Transport Canada AC 300-019; "
           "Virginia Tech ASTM F1805 regressioon",
        "Allikad on omavahel VASTUOLUS ja kover istub nende vahel. "
        "Vt calibrate_snow_temp.py -- seal on kirjas, mida iga allikas "
        "utleb ja kumb kahest katmata vaitest kummale poole osutab."),
    "snow_temp_min": Origin(C, "ohutusklamber", "Ei ole modetud."),
    "snow_temp_max": Origin(C, "ohutusklamber", "Ei ole modetud."),
    "snow_warm_from_c": Origin(
        L, "Transport Canada AC 300-019",
        "-3 C ja soojemal hoiatab regulaator eraldi, et pind voib olla "
        "libedam kui kood naitab. Siit algab lisaebamairasus."),
    "sigma_snow_warm": Origin(
        L, "allikate lahknevusest tuletatud",
        "Laius on valitud nii, et mudeli veapiir kataks nii FAA kui "
        "Lu/WSDOT vaite, mis osutavad VASTASSUUNDA."),

    "snow_loose_factor": Origin(
        L, "Ichihara & Mizoguchi (TRB SR115) tabel 1; FAA AC 25-31 tabel 2 "
           "EI KINNITA",
        "Varem oli siin 1,12 ehk VALE MARGIGA oletus. 2026-09 loeti "
        "molemad allikad uuesti ja varasem vaide 'kaks soltumatut allikat' "
        "EI PIDANUD PAIKA. SR115 (auto, 30-40 km/h) annab uus lumi 0,20-0,25 "
        "vs vana lumi 0,25-0,30 -> 0,82, aga see telg on lume VANUS, mitte "
        "sugavus; sama too annab tallatud lumeks 0,2-0,3, mis katab uue lume "
        "tervenisti. FAA (lennuk) annab siinsel temperatuuril suhteks 1,00 "
        "ja 0,80 alles alla -15 °C, ning tema koefitsient on tahtlikult ilma "
        "lume lukkamise takistuseta. Number 0,85 on seega VALITUD auto-"
        "allika jargi, mitte kinnitatud. Kontrollitud, et sigma katab "
        "lahkarvamuse: FAA 1,00 tulemus mahub meie vahemikku."),

    # ---------------- akvaplaneering ----------------
    "hp_category_factor": Origin(
        F, "[TV25]", "Teknikens Varld 2025, 20 rehvi samas modus "
        "(235/45 R18) koos iga rehvi modetud mustrisugavusega. "
        "Naitab, et lavi soltub mustri KUJUST, mitte ainult sugavusest.",
        anchors=20),
    "hp_c": Origin(
        L, "Horne & Dreher (NASA), v_hp = C*sqrt(p)",
        "Klassikaline valem sileda rehvi ja sugava vee kohta."),
    "hp_tread_gain": Origin(
        F, "[TV25]+[ADAC25] ujumiskiirused",
        "85 modetud ujumiskiirust kahes soltumatus testis.", anchors=85),
    "hp_width_ref_mm": Origin(
        D, "ankrute keskmine", "225 ja 235 keskmine -- normeerimispunkt, "
        "mitte vaba parameeter."),
    "hp_width_exp": Origin(
        L, "[ADAC18]", "Ainus leitud puhas laiusevordlus, kus auto ja "
        "rehvimudel on samad ja muutub ainult mot. 1,0 on selle "
        "KONSERVATIIVNE ots ja uhtlasi fusikaliselt lihtsaim kuju."),
    "hp_water_ref_mm": Origin(
        F, "[TV25]+[ADAC25]", "Normeeritud modetud lavede vastu.",
        anchors=85),
    "mu_hydroplane": Origin(
        L, "NASA/FAA akvaplaneerimise motmised",
        "Taieliku akvaplaneerimise jaakhoore. Mudelis on see UHELDUSE "
        "otspunkt, mitte iseseisev ennustus -- audit motab, kui palju ta "
        "tavapairaseid vastuseid uldse liigutab."),

    # ---------------- Layer 4: auto ----------------
    "abs_eff": Origin(
        F, "[ADAC25]+[ADACS25]+[ADACA25]+[UT25]+[TM25] kaudu autoklassi",
        "LATEST on sobitatud otse (koik asfaldiankrud on LATEST-autod). "
        "NONE/EARLY/MODERN on ekstrapolatsioon ABS-i polvkondade "
        "kirjandusest ja neid ei kitsenda uhtegi asfaldiankur. "
        "Vt audit.py -- see on teadaolev nork koht.", anchors=210),
    "abs_eff_gravel": Origin(
        F, "[ESV98]+[NHTSA99]+[SATC19]",
        "Kruus on ainus pind, kus ABS pidurdusmaad PIKENDAB. Kolm "
        "soltumatut allikat, kokku 22 autot.", anchors=18),
    "brake_buildup_s": Origin(
        L, "piduriseadmete reageerimisaja kirjandus",
        "Pidurdusjou ulesehitusaeg. Mojutab peamiselt luhikesi "
        "pidurdusi; audit motab tegeliku moju."),
    "crr": Origin(
        L, "veeretakistuse standardvaartus soiduautorehvile asfaldil",
        "0,011. Mojutab tulemust alla promilli -- audit kinnitab."),

    # ---------------- ebamäärasus ----------------
    "sigma_base": Origin(
        R, "mudeli enda jaakvead pinna kaupa",
        "EI OLE vaba parameeter: peab olema vahemalt sama suur kui "
        "selle pinna ankrute tegelik jaakhajuvus. audit.py kontrollib "
        "seda igal jooksul ja kukub labi, kui sigma on jaagist vaiksem "
        "ehk mudel lubab rohkem tapsust, kui ta suudab.", anchors=369),
    "speed_range": Origin(
        D, "ankrute tegelik kiirusekate + kirjanduse kiirusesoltuvus",
        "Kus mudelit tohib usaldada. audit.py kontrollib, et iga pinna "
        "vahemik oleks ankrutega kaetud."),
    "sigma_speed_extrap": Origin(
        D, "struktuurne", "Kui palju veapiir kasvab valideeritud "
        "kiirusevahemikust valjas. Konservatiivne konstruktsioon."),
    "sigma_speed_extrap_max": Origin(C, "lagi", "Et veapiir ei plahvataks."),
    "sigma_wet_extra": Origin(
        R, "marja ja kuiva jaakvea vahe",
        "Marg asfalt 4,34 % vs kuiv 2,86 % -- lisaebamairasus katab "
        "selle vahe."),
    "sigma_label_only": Origin(
        D, "EL 2020/740 klassilaius; JARELKONTROLLITUD [EPREL26]",
        "Kui G tuleb ainult margise klassist, on ta teada ainult "
        "+-0,07 tapsusega (klassi laius). See kandub otse veapiiri. "
        "JARELKONTROLL 2026-09: kytus_katse.py sidus 41 moodetud rehvi "
        "EPREL-i ridadega ja mootis, kui lai on moodetud G hajuvus UHE "
        "EPREL-i marghaardeklassi sees: 2,4-3,9 % (5 kategooriat, 23 "
        "rehvi, ainult uheselt maaratud klassiga). Meie 4,5 % on seega "
        "KONSERVATIIVNE, mis on ohutusnumbri juures oige suund. Ja "
        "mootmine ULEhindab hajuvust, sest EPREL-i klass tuli TEISTEST "
        "mootudest kui ADAC-i test -- vt kytus_katse.py piirang 1."),
    "sigma_size_rim_inch": Origin(
        L, "EL 2020/740 klassid on MODUPOHISED",
        "Sama rehvimudel voib olla uhes modus A ja teises B. "
        "HOIATUS: ei ole ankrute vastu sobitatud -- sama rehvi "
        "motmisi eri modus ei ole olemas."),
    "sigma_size_max": Origin(C, "lagi", "Et veapiir ei plahvataks."),
    "size_warn_inch": Origin(
        D, "kasutajaliidese lavi",
        "Millal oelda ka sonadega -- JA millal keelata taht 'korge'. "
        "Sellest tollivahest alates on rehvi haardenumber ulekanne "
        "teiselt modult, mitte selle modu mootmine, ja usaldus "
        "kaetakse 'keskmise' peale. Pidurdusmaad ennast see ei muuda; "
        "pohjus on see, et sigma_size_rim_inch ise ei ole ankrute vastu "
        "sobitatud, nii et 'korge' tuleks valideerimata liikme pealt."),
    "sigma_extrapolation": Origin(
        D, "struktuurne", "Uldine lisand valideeritud alast valjas."),
    "sigma_texture": Origin(
        D, "[FHWA/Jackson 2008] modetud kollineaarsusest",
        "Kaks piirangut korraga: MPD-vastendus on oletus, ja Jacksoni "
        "motmistes on tekstuuri moju SILEDA rehviga suur (suhe 1,03-1,44) "
        "ning mustriga rehviga vaike (0,79-0,82) -- muster teeb sama "
        "tood mis makrotekstuur, seega need kaks liiget on osaliselt "
        "kollineaarsed."),
    "sigma_snow_single_source": Origin(
        D, "[UTAC25N] ja [ZR24] testisisesest hajuvusest",
        "Pohjamaade naelutu ja naastrehvi lumebaas tuleb UHEST testist "
        "kummalgi. Testisisene hajuvus oli 4 % ja 6 %; 6 % on sellest "
        "konservatiivne ots."),
}
