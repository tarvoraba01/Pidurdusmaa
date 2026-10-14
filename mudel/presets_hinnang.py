# -*- coding: utf-8 -*-
"""GENEREERITUD — mudel/naastud_hinnang.py. ÄRA MUUDA KÄSITSI.

Testimata naastrehvid: haare on HINNANG (kaksik, tootja naastrehvide keskmine
või hinnaklassi keskmine), mitte mõõtmine. Vt naastud_hinnang.py.
"""
from .model import Tyre, TyreCategory as C

TYRES_HINNANG = {
    'h_continental_icecontact_8': Tyre('Continental IceContact 8', C.WINTER_STUDDED, 1.2779, mu_dry_override=0.8279, mu_snow_override=0.3821, mu_ice_override=0.2313, studded=True, size='205/55 R16', g_source="hinnang"),
    'h_sailun_ice_blazer_spike': Tyre('Sailun Ice Blazer Spike', C.WINTER_STUDDED, 1.245, mu_dry_override=0.812, mu_snow_override=0.3736, mu_ice_override=0.1829, studded=True, size='205/55 R16', g_source="hinnang"),
    'h_sailun_ice_blazer_wst2': Tyre('Sailun Ice Blazer WST2', C.WINTER_STUDDED, 1.245, mu_dry_override=0.812, mu_snow_override=0.3736, mu_ice_override=0.1829, studded=True, size='215/65 R16', g_source="hinnang"),
    'h_barum_polaris_ice_6': Tyre('Barum Polaris Ice 6', C.WINTER_STUDDED, 1.2558, mu_dry_override=0.8298, mu_snow_override=0.3688, mu_ice_override=0.1968, studded=True, size='205/55 R16', g_source="hinnang"),
    'h_fortune_polaro_ice': Tyre('Fortune Polaro Ice', C.WINTER_STUDDED, 1.2723, mu_dry_override=0.8263, mu_snow_override=0.3781, mu_ice_override=0.1921, studded=True, size='205/55 R16', g_source="hinnang"),
    'h_gt_radial_icepro_3_evo': Tyre('GT Radial IcePro 3 EVO', C.WINTER_STUDDED, 1.2623, mu_dry_override=0.8262, mu_snow_override=0.3743, mu_ice_override=0.1939, studded=True, size='205/55 R16', g_source="hinnang"),
    'h_gt_radial_icepro_suv_3': Tyre('GT Radial IcePro SUV 3', C.WINTER_STUDDED, 1.2623, mu_dry_override=0.8262, mu_snow_override=0.3743, mu_ice_override=0.1939, studded=True, size='215/65 R16', g_source="hinnang"),
    'h_gt_radial_icepro_suv_3_evo': Tyre('GT Radial IcePro SUV 3 EVO', C.WINTER_STUDDED, 1.2623, mu_dry_override=0.8262, mu_snow_override=0.3743, mu_ice_override=0.1939, studded=True, size='215/65 R16', g_source="hinnang"),
    'h_dynamo_nordic_ice': Tyre('Dynamo Nordic Ice', C.WINTER_STUDDED, 1.2723, mu_dry_override=0.8263, mu_snow_override=0.3781, mu_ice_override=0.1921, studded=True, size='205/55 R16', g_source="hinnang"),
    'h_dynamo_snow_h_mwh02': Tyre('Dynamo Snow-H MWH02', C.WINTER_STUDDED, 1.2723, mu_dry_override=0.8263, mu_snow_override=0.3781, mu_ice_override=0.1921, studded=True, size='205/55 R16', g_source="hinnang"),
    'h_dynamo_snow_h_mwh03': Tyre('Dynamo Snow-H MWH03', C.WINTER_STUDDED, 1.2723, mu_dry_override=0.8263, mu_snow_override=0.3781, mu_ice_override=0.1921, studded=True, size='205/55 R16', g_source="hinnang"),
    'h_dynamo_snow_h_mws01': Tyre('Dynamo Snow-H MWS01', C.WINTER_STUDDED, 1.2723, mu_dry_override=0.8263, mu_snow_override=0.3781, mu_ice_override=0.1921, studded=True, size='215/65 R16', g_source="hinnang"),
    'h_maxxis_premitra_ice_nord_np5': Tyre('Maxxis Premitra Ice Nord NP5', C.WINTER_STUDDED, 1.334, mu_dry_override=0.886, mu_snow_override=0.3419, mu_ice_override=0.1992, studded=True, size='205/55 R16', g_source="hinnang"),
    'h_kumho_wintercraft_ice_wi31_plus': Tyre('Kumho WinterCraft Ice WI31+', C.WINTER_STUDDED, 1.23, mu_dry_override=0.8373, mu_snow_override=0.3581, mu_ice_override=0.1892, studded=True, size='205/55 R16', g_source="hinnang"),
    'h_kumho_wintercraft_suv_ice_ws31': Tyre('Kumho WinterCraft SUV Ice WS31', C.WINTER_STUDDED, 1.23, mu_dry_override=0.8373, mu_snow_override=0.3581, mu_ice_override=0.1892, studded=True, size='215/65 R16', g_source="hinnang"),
    'h_goodride_sw606': Tyre('Goodride SW606', C.WINTER_STUDDED, 1.2818, mu_dry_override=0.8252, mu_snow_override=0.3794, mu_ice_override=0.203, studded=True, size='205/55 R16', g_source="hinnang"),
    'h_westlake_sw606': Tyre('Westlake SW606', C.WINTER_STUDDED, 1.2818, mu_dry_override=0.8252, mu_snow_override=0.3794, mu_ice_override=0.203, studded=True, size='205/55 R16', g_source="hinnang"),
    'h_westlake_z506': Tyre('Westlake Z506', C.WINTER_STUDDED, 1.296, mu_dry_override=0.8237, mu_snow_override=0.3814, mu_ice_override=0.2195, studded=True, size='235/60 R18', g_source="hinnang"),
    'h_zeta_antarctica_sport': Tyre('Zeta Antarctica Sport', C.WINTER_STUDDED, 1.2723, mu_dry_override=0.8263, mu_snow_override=0.3781, mu_ice_override=0.1921, studded=True, size='205/55 R16', g_source="hinnang"),
    'h_tigar_sigurastud': Tyre('Tigar SiguraStud', C.WINTER_STUDDED, 1.3356, mu_dry_override=0.85, mu_snow_override=0.3629, mu_ice_override=0.1873, studded=True, size='205/55 R16', g_source="hinnang"),
    'h_rotalla_setula_w_race_s500': Tyre('Rotalla Setula W-Race S500', C.WINTER_STUDDED, 1.2723, mu_dry_override=0.8263, mu_snow_override=0.3781, mu_ice_override=0.1921, studded=True, size='205/55 R16', g_source="hinnang"),
    'h_tracmax_ice_plus_sr1': Tyre('Tracmax Ice-Plus SR1', C.WINTER_STUDDED, 1.2723, mu_dry_override=0.8263, mu_snow_override=0.3781, mu_ice_override=0.1921, studded=True, size='205/55 R16', g_source="hinnang"),
    'h_nankang_sw_9': Tyre('Nankang SW-9', C.WINTER_STUDDED, 1.2254, mu_dry_override=0.8139, mu_snow_override=0.3867, mu_ice_override=0.2092, studded=True, size='205/55 R16', g_source="hinnang"),
    'h_nankang_sw_8': Tyre('Nankang SW-8', C.WINTER_STUDDED, 1.2254, mu_dry_override=0.8139, mu_snow_override=0.3867, mu_ice_override=0.2092, studded=True, size='205/55 R16', g_source="hinnang"),
    'h_laufenn_i_fit_ice_lw71': Tyre('Laufenn I Fit Ice LW71', C.WINTER_STUDDED, 1.2558, mu_dry_override=0.8298, mu_snow_override=0.3688, mu_ice_override=0.1968, studded=True, size='205/55 R16', g_source="hinnang"),
    'h_leao_winter_defender_grip': Tyre('Leao Winter Defender Grip', C.WINTER_STUDDED, 1.2723, mu_dry_override=0.8263, mu_snow_override=0.3781, mu_ice_override=0.1921, studded=True, size='205/55 R16', g_source="hinnang"),
    'h_continental_vancontact_ice': Tyre('Continental VanContact Ice', C.WINTER_STUDDED, 1.2779, mu_dry_override=0.8279, mu_snow_override=0.3821, mu_ice_override=0.2313, studded=True, size='215/65 R16 C', g_source="hinnang"),
    'h_sailun_commercio_ice': Tyre('Sailun Commercio Ice', C.WINTER_STUDDED, 1.245, mu_dry_override=0.812, mu_snow_override=0.3736, mu_ice_override=0.1829, studded=True, size='215/65 R16 C', g_source="hinnang"),
    'h_barum_snovanis_ice': Tyre('Barum SnoVanis Ice', C.WINTER_STUDDED, 1.2558, mu_dry_override=0.8298, mu_snow_override=0.3688, mu_ice_override=0.1968, studded=True, size='215/65 R16 C', g_source="hinnang"),
    'h_gislaved_nord_frost_van_2': Tyre('Gislaved Nord Frost Van 2', C.WINTER_STUDDED, 1.2813, mu_dry_override=0.8396, mu_snow_override=0.3781, mu_ice_override=0.2012, studded=True, size='215/65 R16 C', g_source="hinnang"),
    'h_hankook_winter_ipike_lv_rw15': Tyre('Hankook Winter i*Pike LV RW15', C.WINTER_STUDDED, 1.2435, mu_dry_override=0.8212, mu_snow_override=0.3746, mu_ice_override=0.2026, studded=True, size='215/65 R16 C', g_source="hinnang"),
    'h_nokian_hakkapeliitta_c4': Tyre('Nokian Hakkapeliitta C4', C.WINTER_STUDDED, 1.2467, mu_dry_override=0.8156, mu_snow_override=0.3849, mu_ice_override=0.2471, studded=True, size='215/65 R16 C', g_source="hinnang"),
    'h_nokian_hakkapeliitta_lt3': Tyre('Nokian Hakkapeliitta LT3', C.WINTER_STUDDED, 1.2467, mu_dry_override=0.8156, mu_snow_override=0.3849, mu_ice_override=0.2471, studded=True, size='245/75 R16 C', g_source="hinnang"),
    'h_michelin_agilis_x_ice_north': Tyre('Michelin Agilis X-Ice North', C.WINTER_STUDDED, 1.2357, mu_dry_override=0.8174, mu_snow_override=0.3786, mu_ice_override=0.2216, studded=True, size='215/65 R16 C', g_source="hinnang"),
}

HINNANG = {
 "h_continental_icecontact_8": {
  "nimi": "Continental IceContact 8",
  "size": "205/55 R16",
  "viis": "tootja",
  "klass": "premium",
  "n": {
   "ice": 3,
   "snow": 2,
   "wet": 3,
   "dry": 3
  }
 },
 "h_sailun_ice_blazer_spike": {
  "nimi": "Sailun Ice Blazer Spike",
  "size": "205/55 R16",
  "viis": "tootja",
  "klass": "soodne",
  "n": {
   "ice": 1,
   "snow": 1,
   "wet": 1,
   "dry": 1
  }
 },
 "h_sailun_ice_blazer_wst2": {
  "nimi": "Sailun Ice Blazer WST2",
  "size": "215/65 R16",
  "viis": "tootja",
  "klass": "soodne",
  "n": {
   "ice": 1,
   "snow": 1,
   "wet": 1,
   "dry": 1
  }
 },
 "h_barum_polaris_ice_6": {
  "nimi": "Barum Polaris Ice 6",
  "size": "205/55 R16",
  "viis": "klass",
  "klass": "kesk",
  "n": {
   "ice": 0,
   "snow": 0,
   "wet": 0,
   "dry": 0
  }
 },
 "h_fortune_polaro_ice": {
  "nimi": "Fortune Polaro Ice",
  "size": "205/55 R16",
  "viis": "klass",
  "klass": "soodne",
  "n": {
   "ice": 0,
   "snow": 0,
   "wet": 0,
   "dry": 0
  }
 },
 "h_gt_radial_icepro_3_evo": {
  "nimi": "GT Radial IcePro 3 EVO",
  "size": "205/55 R16",
  "viis": "tootja",
  "klass": "kesk",
  "n": {
   "ice": 1,
   "snow": 1,
   "wet": 1,
   "dry": 1
  }
 },
 "h_gt_radial_icepro_suv_3": {
  "nimi": "GT Radial IcePro SUV 3",
  "size": "215/65 R16",
  "viis": "tootja",
  "klass": "kesk",
  "n": {
   "ice": 1,
   "snow": 1,
   "wet": 1,
   "dry": 1
  }
 },
 "h_gt_radial_icepro_suv_3_evo": {
  "nimi": "GT Radial IcePro SUV 3 EVO",
  "size": "215/65 R16",
  "viis": "tootja",
  "klass": "kesk",
  "n": {
   "ice": 1,
   "snow": 1,
   "wet": 1,
   "dry": 1
  }
 },
 "h_dynamo_nordic_ice": {
  "nimi": "Dynamo Nordic Ice",
  "size": "205/55 R16",
  "viis": "klass",
  "klass": "soodne",
  "n": {
   "ice": 0,
   "snow": 0,
   "wet": 0,
   "dry": 0
  }
 },
 "h_dynamo_snow_h_mwh02": {
  "nimi": "Dynamo Snow-H MWH02",
  "size": "205/55 R16",
  "viis": "klass",
  "klass": "soodne",
  "n": {
   "ice": 0,
   "snow": 0,
   "wet": 0,
   "dry": 0
  }
 },
 "h_dynamo_snow_h_mwh03": {
  "nimi": "Dynamo Snow-H MWH03",
  "size": "205/55 R16",
  "viis": "klass",
  "klass": "soodne",
  "n": {
   "ice": 0,
   "snow": 0,
   "wet": 0,
   "dry": 0
  }
 },
 "h_dynamo_snow_h_mws01": {
  "nimi": "Dynamo Snow-H MWS01",
  "size": "215/65 R16",
  "viis": "klass",
  "klass": "soodne",
  "n": {
   "ice": 0,
   "snow": 0,
   "wet": 0,
   "dry": 0
  }
 },
 "h_maxxis_premitra_ice_nord_np5": {
  "nimi": "Maxxis Premitra Ice Nord NP5",
  "size": "205/55 R16",
  "viis": "kaksik",
  "kaksik": "Maxxis Premitra Ice Nord 5 SUV"
 },
 "h_kumho_wintercraft_ice_wi31_plus": {
  "nimi": "Kumho WinterCraft Ice WI31+",
  "size": "205/55 R16",
  "viis": "kaksik",
  "kaksik": "Kumho WinterCraft Ice WI31"
 },
 "h_kumho_wintercraft_suv_ice_ws31": {
  "nimi": "Kumho WinterCraft SUV Ice WS31",
  "size": "215/65 R16",
  "viis": "kaksik",
  "kaksik": "Kumho WinterCraft Ice WI31"
 },
 "h_goodride_sw606": {
  "nimi": "Goodride SW606",
  "size": "205/55 R16",
  "viis": "tootja",
  "klass": "soodne",
  "n": {
   "ice": 1,
   "snow": 1,
   "wet": 1,
   "dry": 1
  }
 },
 "h_westlake_sw606": {
  "nimi": "Westlake SW606",
  "size": "205/55 R16",
  "viis": "kaksik",
  "kaksik": "Goodride SW606"
 },
 "h_westlake_z506": {
  "nimi": "Westlake Z506",
  "size": "235/60 R18",
  "viis": "kaksik",
  "kaksik": "Goodride IceMaster Spike Z-506"
 },
 "h_zeta_antarctica_sport": {
  "nimi": "Zeta Antarctica Sport",
  "size": "205/55 R16",
  "viis": "klass",
  "klass": "soodne",
  "n": {
   "ice": 0,
   "snow": 0,
   "wet": 0,
   "dry": 0
  }
 },
 "h_tigar_sigurastud": {
  "nimi": "Tigar SiguraStud",
  "size": "205/55 R16",
  "viis": "tootja",
  "klass": "kesk",
  "n": {
   "ice": 2,
   "snow": 2,
   "wet": 2,
   "dry": 2
  }
 },
 "h_rotalla_setula_w_race_s500": {
  "nimi": "Rotalla Setula W-Race S500",
  "size": "205/55 R16",
  "viis": "klass",
  "klass": "soodne",
  "n": {
   "ice": 0,
   "snow": 0,
   "wet": 0,
   "dry": 0
  }
 },
 "h_tracmax_ice_plus_sr1": {
  "nimi": "Tracmax Ice-Plus SR1",
  "size": "205/55 R16",
  "viis": "klass",
  "klass": "soodne",
  "n": {
   "ice": 0,
   "snow": 0,
   "wet": 0,
   "dry": 0
  }
 },
 "h_nankang_sw_9": {
  "nimi": "Nankang SW-9",
  "size": "205/55 R16",
  "viis": "tootja",
  "klass": "soodne",
  "n": {
   "ice": 1,
   "snow": 1,
   "wet": 1,
   "dry": 1
  }
 },
 "h_nankang_sw_8": {
  "nimi": "Nankang SW-8",
  "size": "205/55 R16",
  "viis": "tootja",
  "klass": "soodne",
  "n": {
   "ice": 1,
   "snow": 1,
   "wet": 1,
   "dry": 1
  }
 },
 "h_laufenn_i_fit_ice_lw71": {
  "nimi": "Laufenn I Fit Ice LW71",
  "size": "205/55 R16",
  "viis": "klass",
  "klass": "kesk",
  "n": {
   "ice": 0,
   "snow": 0,
   "wet": 0,
   "dry": 0
  }
 },
 "h_leao_winter_defender_grip": {
  "nimi": "Leao Winter Defender Grip",
  "size": "205/55 R16",
  "viis": "klass",
  "klass": "soodne",
  "n": {
   "ice": 0,
   "snow": 0,
   "wet": 0,
   "dry": 0
  }
 },
 "h_continental_vancontact_ice": {
  "nimi": "Continental VanContact Ice",
  "size": "215/65 R16 C",
  "viis": "tootja",
  "klass": "premium",
  "n": {
   "ice": 3,
   "snow": 2,
   "wet": 3,
   "dry": 3
  }
 },
 "h_sailun_commercio_ice": {
  "nimi": "Sailun Commercio Ice",
  "size": "215/65 R16 C",
  "viis": "tootja",
  "klass": "soodne",
  "n": {
   "ice": 1,
   "snow": 1,
   "wet": 1,
   "dry": 1
  }
 },
 "h_barum_snovanis_ice": {
  "nimi": "Barum SnoVanis Ice",
  "size": "215/65 R16 C",
  "viis": "klass",
  "klass": "kesk",
  "n": {
   "ice": 0,
   "snow": 0,
   "wet": 0,
   "dry": 0
  }
 },
 "h_gislaved_nord_frost_van_2": {
  "nimi": "Gislaved Nord Frost Van 2",
  "size": "215/65 R16 C",
  "viis": "tootja",
  "klass": "kesk",
  "n": {
   "ice": 2,
   "snow": 2,
   "wet": 2,
   "dry": 2
  }
 },
 "h_hankook_winter_ipike_lv_rw15": {
  "nimi": "Hankook Winter i*Pike LV RW15",
  "size": "215/65 R16 C",
  "viis": "tootja",
  "klass": "kesk",
  "n": {
   "ice": 3,
   "snow": 3,
   "wet": 3,
   "dry": 3
  }
 },
 "h_nokian_hakkapeliitta_c4": {
  "nimi": "Nokian Hakkapeliitta C4",
  "size": "215/65 R16 C",
  "viis": "tootja",
  "klass": "premium",
  "n": {
   "ice": 16,
   "snow": 15,
   "wet": 16,
   "dry": 16
  }
 },
 "h_nokian_hakkapeliitta_lt3": {
  "nimi": "Nokian Hakkapeliitta LT3",
  "size": "245/75 R16 C",
  "viis": "tootja",
  "klass": "premium",
  "n": {
   "ice": 16,
   "snow": 15,
   "wet": 16,
   "dry": 16
  }
 },
 "h_michelin_agilis_x_ice_north": {
  "nimi": "Michelin Agilis X-Ice North",
  "size": "215/65 R16 C",
  "viis": "tootja",
  "klass": "premium",
  "n": {
   "ice": 4,
   "snow": 3,
   "wet": 4,
   "dry": 4
  }
 }
}
