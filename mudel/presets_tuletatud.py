# -*- coding: utf-8 -*-
"""GENEREERITUD — mudel/naastud_tuleta.py. ÄRA MUUDA KÄSITSI.

Ajakirjatestidest (testid_ext/*.json) tuletatud rehvid: mu on lahendatud
sama testi sees mõõdetud rehvide suhtes (d ∝ 1/mu). Vt naastud_tuleta.py.
"""
from .model import Tyre, TyreCategory as C

TYRES_TULETATUD = {
    "t_bfgoodrich_g_force_stud": Tyre('BFGoodrich g-Force Stud', C.WINTER_STUDDED, 1.256, mu_dry_override=0.876, mu_snow_override=0.3873, mu_ice_override=0.1835, studded=True, size='205/55 R16', g_source="test"),
    "t_bridgestone_blizzak_dm_v3": Tyre('Bridgestone Blizzak DM-V3', C.WINTER_NORDIC, 1.217, mu_dry_override=0.8678, mu_snow_override=0.3753, mu_ice_override=0.1924, size='235/55 R18', g_source="test"),
    "t_bridgestone_blizzak_ice": Tyre('Bridgestone Blizzak Ice', C.WINTER_NORDIC, 1.129, mu_dry_override=0.8643, mu_snow_override=0.3673, mu_ice_override=0.1919, size='225/45 R17', g_source="test"),
    "t_bridgestone_blizzak_revo_gz": Tyre('Bridgestone Blizzak Revo GZ', C.WINTER_NORDIC, 1.108, mu_dry_override=0.8463, mu_snow_override=0.3597, mu_ice_override=0.1721, size='205/55 R16', g_source="test"),
    "t_bridgestone_blizzak_spike_01": Tyre('Bridgestone Blizzak Spike-01', C.WINTER_STUDDED, 1.188, mu_dry_override=0.8302, mu_snow_override=0.3669, mu_ice_override=0.1845, studded=True, size='205/55 R16', g_source="test"),
    "t_bridgestone_blizzak_spike_02": Tyre('Bridgestone Blizzak Spike-02', C.WINTER_STUDDED, 1.185, mu_dry_override=0.7619, mu_snow_override=0.3755, mu_ice_override=0.2265, studded=True, size='195/65 R15', g_source="test"),
    "t_bridgestone_blizzak_vrx": Tyre('Bridgestone Blizzak VRX', C.WINTER_NORDIC, 1.142, mu_dry_override=0.8508, mu_snow_override=0.3526, mu_ice_override=0.1791, size='205/55 R16', g_source="test"),
    "t_bridgestone_blizzak_ws70": Tyre('Bridgestone Blizzak WS70', C.WINTER_NORDIC, 1.139, mu_dry_override=0.889, mu_snow_override=0.3588, mu_ice_override=0.1703, size='205/55 R16', g_source="test"),
    "t_bridgestone_blizzak_ws80": Tyre('Bridgestone Blizzak WS80', C.WINTER_NORDIC, 1.118, mu_dry_override=0.864, mu_snow_override=0.3625, mu_ice_override=0.1712, size='205/55 R16', g_source="test"),
    "t_bridgestone_noranza_001": Tyre('Bridgestone Noranza 001', C.WINTER_STUDDED, 1.223, mu_dry_override=0.8088, mu_snow_override=0.3786, mu_ice_override=0.2302, studded=True, size='205/55 R16', g_source="test"),
    "t_continental_contiicecontact": Tyre('Continental ContiIceContact', C.WINTER_STUDDED, 1.117, mu_dry_override=0.8633, mu_snow_override=0.371, mu_ice_override=0.2002, studded=True, size='205/55 R16', g_source="test"),
    "t_continental_icecontact_2": Tyre('Continental IceContact 2', C.WINTER_STUDDED, 1.297, mu_dry_override=0.8287, mu_snow_override=0.3838, mu_ice_override=0.2199, studded=True, size='205/55 R16', g_source="test"),
    "t_continental_icecontact_2_suv": Tyre('Continental IceContact 2 SUV', C.WINTER_STUDDED, 1.258, mu_dry_override=0.8309, mu_snow_override=0.3804, mu_ice_override=0.2316, studded=True, size='215/65 R16', g_source="test"),
    "t_continental_contivikingcontact_5": Tyre('Continental ContiVikingContact 5', C.WINTER_NORDIC, 1.152, mu_dry_override=0.8571, mu_snow_override=0.3556, mu_ice_override=0.1586, size='205/55 R16', g_source="test"),
    "t_continental_contivikingcontact_6": Tyre('Continental ContiVikingContact 6', C.WINTER_NORDIC, 1.222, mu_dry_override=0.842, mu_snow_override=0.3646, mu_ice_override=0.1742, size='205/55 R16', g_source="test"),
    "t_continental_vikingcontact_7": Tyre('Continental VikingContact 7', C.WINTER_NORDIC, 1.17, mu_dry_override=0.8483, mu_snow_override=0.376, mu_ice_override=0.2115, size='225/45 R17', g_source="test"),
    "t_dunlop_grandtrek_ice_02": Tyre('Dunlop Grandtrek Ice 02', C.WINTER_STUDDED, 1.213, mu_dry_override=0.804, mu_snow_override=0.3599, mu_ice_override=0.1975, studded=True, size='235/65 R17', g_source="test"),
    "t_dunlop_ice_touch": Tyre('Dunlop Ice Touch', C.WINTER_STUDDED, 1.274, mu_dry_override=0.9151, mu_snow_override=0.3683, mu_ice_override=0.2139, studded=True, size='205/55 R16', g_source="test"),
    "t_dunlop_winter_maxx_wm01": Tyre('Dunlop Winter Maxx WM01', C.WINTER_NORDIC, 1.091, mu_dry_override=0.7915, mu_snow_override=0.3605, mu_ice_override=0.1859, size='225/45 R17', g_source="test"),
    "t_dunlop_winter_maxx_wm02": Tyre('Dunlop Winter Maxx WM02', C.WINTER_NORDIC, 1.117, mu_dry_override=0.7956, mu_snow_override=0.3632, mu_ice_override=0.1923, size='205/55 R16', g_source="test"),
    "t_dunlop_sp_winter_ice_02": Tyre('Dunlop SP Winter Ice 02', C.WINTER_STUDDED, 1.223, mu_dry_override=0.7968, mu_snow_override=0.3769, mu_ice_override=0.2143, studded=True, size='185/65 R15', g_source="test"),
    "t_falken_winterpeak_f_ice_1": Tyre('Falken Winterpeak F-Ice 1', C.WINTER_STUDDED, 1.252, mu_dry_override=0.7986, mu_snow_override=0.3856, mu_ice_override=0.258, studded=True, size='225/45 R17', g_source="test"),
    "t_firestone_ice_cruiser_7": Tyre('Firestone Ice Cruiser 7', C.WINTER_STUDDED, 1.167, mu_dry_override=0.8103, mu_snow_override=0.348, mu_ice_override=0.1962, studded=True, size='195/65 R15', g_source="test"),
    "t_gislaved_nord_frost_100": Tyre('Gislaved Nord Frost 100', C.WINTER_STUDDED, 1.351, mu_dry_override=0.8743, mu_snow_override=0.3711, mu_ice_override=0.172, studded=True, size='205/55 R16', g_source="test"),
    "t_gislaved_nord_frost_200": Tyre('Gislaved Nord Frost 200', C.WINTER_STUDDED, 1.223, mu_dry_override=0.8301, mu_snow_override=0.3855, mu_ice_override=0.2036, studded=True, size='205/55 R16', g_source="test"),
    "t_gislaved_nord_frost_200_suv": Tyre('Gislaved Nord Frost 200 SUV', C.WINTER_STUDDED, 1.378, mu_dry_override=0.8639, mu_snow_override=0.3846, mu_ice_override=0.2055, studded=True, size='215/65 R16', g_source="test"),
    "t_gislaved_soft_frost_200": Tyre('Gislaved Soft Frost 200', C.WINTER_NORDIC, 1.106, mu_dry_override=0.8624, mu_snow_override=0.362, mu_ice_override=0.1848, size='205/55 R16', g_source="test"),
    "t_goodride_icemaster_spike_z_506": Tyre('Goodride IceMaster Spike Z-506', C.WINTER_STUDDED, 1.296, mu_dry_override=0.8237, mu_snow_override=0.3814, mu_ice_override=0.2195, studded=True, size='235/60 R18', g_source="test"),
    "t_goodyear_ultragrip_600": Tyre('Goodyear UltraGrip 600', C.WINTER_STUDDED, 1.276, mu_dry_override=0.8346, mu_snow_override=0.3726, mu_ice_override=0.1821, studded=True, size='205/55 R16', g_source="test"),
    "t_goodyear_ultragrip_arctic_2_suv": Tyre('Goodyear UltraGrip Arctic 2 SUV', C.WINTER_STUDDED, 1.312, mu_dry_override=0.8044, mu_snow_override=0.3865, mu_ice_override=0.2972, studded=True, size='235/60 R18', g_source="test"),
    "t_goodyear_ultragrip_ice_2": Tyre('Goodyear UltraGrip Ice 2', C.WINTER_NORDIC, 1.267, mu_dry_override=0.8534, mu_snow_override=0.3721, mu_ice_override=0.2049, size='195/65 R15', g_source="test"),
    "t_goodyear_ultragrip_ice_arctic": Tyre('Goodyear UltraGrip Ice Arctic', C.WINTER_STUDDED, 1.264, mu_dry_override=0.8314, mu_snow_override=0.3819, mu_ice_override=0.2173, studded=True, size='225/50 R17', g_source="test"),
    "t_goodyear_ultragrip_ice_arctic_suv_4x4": Tyre('Goodyear UltraGrip Ice Arctic SUV 4x4', C.WINTER_STUDDED, 1.297, mu_dry_override=0.8234, mu_snow_override=0.3722, mu_ice_override=0.2158, studded=True, size='235/65 R17', g_source="test"),
    "t_gt_radial_champiro_ice_pro": Tyre('GT Radial Champiro Ice Pro', C.WINTER_STUDDED, 1.233, mu_dry_override=0.8957, mu_snow_override=0.3316, mu_ice_override=0.1555, studded=True, size='205/55 R16', g_source="test"),
    "t_gt_radial_ice_pro_3": Tyre('GT Radial Ice Pro 3', C.WINTER_STUDDED, 1.272, mu_dry_override=0.8207, mu_snow_override=0.3825, mu_ice_override=0.1895, studded=True, size='195/65 R15', g_source="test"),
    "t_hankook_winter_i_cept_iz2": Tyre('Hankook Winter i*cept iZ2', C.WINTER_NORDIC, 1.14, mu_dry_override=0.82, mu_snow_override=0.369, mu_ice_override=0.1908, size='225/45 R17', g_source="test"),
    "t_hankook_winter_i_cept_iz3_x": Tyre('Hankook Winter i*cept iZ3 X', C.WINTER_NORDIC, 1.11, mu_dry_override=0.8286, mu_snow_override=0.3779, mu_ice_override=0.1801, size='235/60 R18', g_source="test"),
    "t_hankook_winter_i_pike_rs": Tyre('Hankook Winter i*Pike RS', C.WINTER_STUDDED, 1.248, mu_dry_override=0.8466, mu_snow_override=0.369, mu_ice_override=0.2115, studded=True, size='205/55 R16', g_source="test"),
    "t_hankook_winter_i_pike_rs2": Tyre('Hankook Winter i*Pike RS2', C.WINTER_STUDDED, 1.245, mu_dry_override=0.8087, mu_snow_override=0.387, mu_ice_override=0.2377, studded=True, size='225/45 R17', g_source="test"),
    "t_hankook_winter_i_pike_rs": Tyre('Hankook Winter i*Pike RS+', C.WINTER_STUDDED, 1.213, mu_dry_override=0.7853, mu_snow_override=0.3769, mu_ice_override=0.2005, studded=True, size='205/55 R16', g_source="test"),
    "t_hankook_winter_i_pike_x": Tyre('Hankook Winter i*Pike X', C.WINTER_STUDDED, 1.254, mu_dry_override=0.8567, mu_snow_override=0.3685, mu_ice_override=0.1782, studded=True, size='235/60 R18', g_source="test"),
    "t_kormoran_stud_2": Tyre('Kormoran Stud 2', C.WINTER_STUDDED, 1.368, mu_dry_override=0.8346, mu_snow_override=0.3575, mu_ice_override=0.1887, studded=True, size='195/65 R15', g_source="test"),
    "t_kumho_wintercraft_ice_wi31": Tyre('Kumho WinterCraft ice Wi31', C.WINTER_STUDDED, 1.229, mu_dry_override=0.8344, mu_snow_override=0.373, mu_ice_override=0.18, studded=True, size='225/45 R17', g_source="test"),
    "t_kumho_wintercraft_ice_wi51": Tyre('Kumho WinterCraft Ice Wi51', C.WINTER_NORDIC, 1.304, mu_dry_override=0.82, mu_snow_override=0.3771, mu_ice_override=0.2021, size='205/55 R16', g_source="test"),
    "t_kumho_wintercraft_ws51": Tyre('Kumho WinterCraft WS51', C.WINTER_NORDIC, 1.235, mu_dry_override=0.8225, mu_snow_override=0.3702, mu_ice_override=0.1793, size='235/55 R18', g_source="test"),
    "t_linglong_greenmax_winter_grip": Tyre('Linglong GreenMax Winter Grip', C.WINTER_STUDDED, 1.245, mu_dry_override=0.9238, mu_snow_override=0.3607, mu_ice_override=0.1609, studded=True, size='205/55 R16', g_source="test"),
    "t_linglong_green_max_winter_grip_2": Tyre('Linglong Green-Max Winter Grip 2', C.WINTER_STUDDED, 1.171, mu_dry_override=0.8514, mu_snow_override=0.3855, mu_ice_override=0.2302, studded=True, size='205/55 R16', g_source="test"),
    "t_linglong_winter_unicorn": Tyre('Linglong Winter Unicorn', C.WINTER_NORDIC, 1.081, mu_dry_override=0.84, mu_snow_override=0.3817, mu_ice_override=0.2031, size='205/55 R16', g_source="test"),
    "t_marshal_i_zen_kw31": Tyre("Marshal I'Zen KW31", C.WINTER_NORDIC, 1.04, mu_dry_override=0.8463, mu_snow_override=0.3552, mu_ice_override=0.1868, size='205/55 R16', g_source="test"),
    "t_kumho_wintercraft_ice_wi31": Tyre('Kumho WinterCraft Ice Wi31', C.WINTER_STUDDED, 1.23, mu_dry_override=0.8373, mu_snow_override=0.3581, mu_ice_override=0.1892, studded=True, size='205/55 R16', g_source="test"),
    "t_matador_mp_30_sibir_ice_2": Tyre('Matador MP 30 Sibir Ice 2', C.WINTER_STUDDED, 1.286, mu_dry_override=0.8209, mu_snow_override=0.3744, mu_ice_override=0.1791, studded=True, size='205/55 R16', g_source="test"),
    "t_maxxis_premitra_ice_nord_5_suv": Tyre('Maxxis Premitra Ice Nord 5 SUV', C.WINTER_STUDDED, 1.334, mu_dry_override=0.886, mu_snow_override=0.3419, mu_ice_override=0.1992, studded=True, size='235/55 R18', g_source="test"),
    "t_michelin_latitude_x_ice_north_2": Tyre('Michelin Latitude X-Ice North 2+', C.WINTER_STUDDED, 1.272, mu_dry_override=0.8259, mu_snow_override=0.3701, mu_ice_override=0.1629, studded=True, size='235/65 R17', g_source="test"),
    "t_michelin_x_ice_3": Tyre('Michelin X-Ice 3', C.WINTER_NORDIC, 1.153, mu_dry_override=0.8392, mu_snow_override=0.356, mu_ice_override=0.1986, size='225/45 R17', g_source="test"),
    "t_michelin_x_ice_north_3": Tyre('Michelin X-Ice North 3', C.WINTER_STUDDED, 1.176, mu_dry_override=0.8211, mu_snow_override=0.3739, mu_ice_override=0.1757, studded=True, size='215/65 R16', g_source="test"),
    "t_michelin_x_ice_north_4_suv": Tyre('Michelin X-Ice North 4 SUV', C.WINTER_STUDDED, 1.239, mu_dry_override=0.8007, mu_snow_override=0.3862, mu_ice_override=0.2593, studded=True, size='235/60 R18', g_source="test"),
    "t_michelin_x_ice_snow_suv": Tyre('Michelin X-Ice Snow SUV', C.WINTER_NORDIC, 1.111, mu_dry_override=0.7951, mu_snow_override=0.3782, mu_ice_override=0.1978, size='235/60 R18', g_source="test"),
    "t_michelin_x_ice_xi3": Tyre('Michelin X-Ice XI3', C.WINTER_NORDIC, 1.171, mu_dry_override=0.8252, mu_snow_override=0.3625, mu_ice_override=0.1692, size='205/55 R16', g_source="test"),
    "t_nankang_ice_activa_2": Tyre('Nankang Ice Activa 2', C.WINTER_NORDIC, 1.144, mu_dry_override=0.7923, mu_snow_override=0.378, mu_ice_override=0.1924, size='205/55 R16', g_source="test"),
    "t_nankang_ice_activa_grip_2_suv": Tyre('Nankang Ice Activa Grip 2 SUV', C.WINTER_STUDDED, 1.155, mu_dry_override=0.7954, mu_snow_override=0.3995, mu_ice_override=0.2349, studded=True, size='215/65 R17', g_source="test"),
    "t_nankang_ice_activa_ice_1": Tyre('Nankang Ice Activa Ice-1', C.WINTER_NORDIC, 1.245, mu_dry_override=0.8361, mu_snow_override=0.3648, mu_ice_override=0.1466, size='195/65 R15', g_source="test"),
    "t_nexen_winguard_ice": Tyre('Nexen WinGuard ice', C.WINTER_NORDIC, 1.01, mu_dry_override=0.7988, mu_snow_override=0.3543, mu_ice_override=0.1708, size='195/65 R15', g_source="test"),
    "t_nexen_winguard_ice_plus": Tyre('Nexen WinGuard Ice Plus', C.WINTER_NORDIC, 1.048, mu_dry_override=0.7897, mu_snow_override=0.3574, mu_ice_override=0.1725, size='205/55 R16', g_source="test"),
    "t_nexen_winguard_ice_plus_wh43": Tyre('Nexen Winguard Ice Plus WH43', C.WINTER_NORDIC, 1.117, mu_dry_override=0.8024, mu_snow_override=0.3788, mu_ice_override=0.1932, size='205/55 R16', g_source="test"),
    "t_nexen_winguard_winspike": Tyre('Nexen WinGuard WinSpike', C.WINTER_STUDDED, 1.164, mu_dry_override=0.8157, mu_snow_override=0.3697, mu_ice_override=0.1449, studded=True, size='205/55 R16', g_source="test"),
    "t_nexen_winguard_winspike_3": Tyre('Nexen WinGuard WinSpike 3', C.WINTER_STUDDED, 1.35, mu_dry_override=0.8352, mu_snow_override=0.3672, mu_ice_override=0.2197, studded=True, size='235/60 R18', g_source="test"),
    "t_nexen_winguard_winspike_wh62": Tyre('Nexen Winguard winSpike WH62', C.WINTER_STUDDED, 1.152, mu_dry_override=0.8337, mu_snow_override=0.3345, mu_ice_override=0.1432, studded=True, size='205/55 R16', g_source="test"),
    "t_nokian_hakkapeliitta_01": Tyre('Nokian Hakkapeliitta 01', C.WINTER_STUDDED, 1.29, mu_dry_override=0.8452, mu_snow_override=0.3936, mu_ice_override=0.2518, studded=True, size='205/55 R16', g_source="test"),
    "t_nokian_hakkapeliitta_10p": Tyre('Nokian Hakkapeliitta 10P', C.WINTER_STUDDED, 1.241, mu_dry_override=0.8003, mu_snow_override=0.3951, mu_ice_override=0.2824, studded=True, size='195/65 R15', g_source="test"),
    "t_nokian_hakkapeliitta_10p_suv": Tyre('Nokian Hakkapeliitta 10P SUV', C.WINTER_STUDDED, 1.301, mu_dry_override=0.8483, mu_snow_override=0.3811, mu_ice_override=0.2399, studded=True, size='235/60 R18', g_source="test"),
    "t_nokian_hakkapeliitta_10_suv": Tyre('Nokian Hakkapeliitta 10 SUV', C.WINTER_STUDDED, 1.265, mu_dry_override=0.8198, mu_snow_override=0.3824, mu_ice_override=0.3203, studded=True, size='235/60 R18', g_source="test"),
    "t_nokian_hakkapeliitta_8": Tyre('Nokian Hakkapeliitta 8', C.WINTER_STUDDED, 1.25, mu_dry_override=0.8474, mu_snow_override=0.3773, mu_ice_override=0.2327, studded=True, size='225/45 R17', g_source="test"),
    "t_nokian_hakkapeliitta_8_suv": Tyre('Nokian Hakkapeliitta 8 SUV', C.WINTER_STUDDED, 1.297, mu_dry_override=0.8284, mu_snow_override=0.3765, mu_ice_override=0.2263, studded=True, size='235/65 R17', g_source="test"),
    "t_nokian_hakkapeliitta_9": Tyre('Nokian Hakkapeliitta 9', C.WINTER_STUDDED, 1.26, mu_dry_override=0.8129, mu_snow_override=0.387, mu_ice_override=0.2417, studded=True, size='205/60 R16', g_source="test"),
    "t_nokian_hakkapeliitta_9_suv": Tyre('Nokian Hakkapeliitta 9 SUV', C.WINTER_STUDDED, 1.251, mu_dry_override=0.8044, mu_snow_override=0.3846, mu_ice_override=0.2481, studded=True, size='255/55 R19', g_source="test"),
    "t_nokian_hakkapeliitta_r2": Tyre('Nokian Hakkapeliitta R2', C.WINTER_NORDIC, 1.125, mu_dry_override=0.8346, mu_snow_override=0.3616, mu_ice_override=0.1806, size='225/45 R17', g_source="test"),
    "t_nokian_hakkapeliitta_r3": Tyre('Nokian Hakkapeliitta R3', C.WINTER_NORDIC, 1.178, mu_dry_override=0.8505, mu_snow_override=0.3832, mu_ice_override=0.1993, size='205/55 R16', g_source="test"),
    "t_nokian_hakkapeliitta_r3_suv": Tyre('Nokian Hakkapeliitta R3 SUV', C.WINTER_NORDIC, 1.239, mu_dry_override=0.8497, mu_snow_override=0.382, mu_ice_override=0.2154, size='215/65 R16', g_source="test"),
    "t_nokian_hakkapeliitta_r5_suv": Tyre('Nokian Hakkapeliitta R5 SUV', C.WINTER_NORDIC, 1.26, mu_dry_override=0.8197, mu_snow_override=0.3801, mu_ice_override=0.1933, size='235/60 R18', g_source="test"),
    "t_nokian_nordman_5": Tyre('Nokian Nordman 5', C.WINTER_STUDDED, 1.22, mu_dry_override=0.8114, mu_snow_override=0.3747, mu_ice_override=0.1784, studded=True, size='195/65 R15', g_source="test"),
    "t_nokian_nordman_7": Tyre('Nokian Nordman 7', C.WINTER_STUDDED, 1.173, mu_dry_override=0.7891, mu_snow_override=0.3799, mu_ice_override=0.2185, studded=True, size='205/60 R16', g_source="test"),
    "t_nokian_nordman_7_suv": Tyre('Nokian Nordman 7 SUV', C.WINTER_STUDDED, 1.239, mu_dry_override=0.8053, mu_snow_override=0.3873, mu_ice_override=0.2233, studded=True, size='215/65 R16', g_source="test"),
    "t_nokian_nordman_8": Tyre('Nokian Nordman 8', C.WINTER_STUDDED, 1.192, mu_dry_override=0.7978, mu_snow_override=0.3875, mu_ice_override=0.2562, studded=True, size='195/65 R15', g_source="test"),
    "t_nokian_nordman_8_suv": Tyre('Nokian Nordman 8 SUV', C.WINTER_STUDDED, 1.235, mu_dry_override=0.8165, mu_snow_override=0.3811, mu_ice_override=0.2581, studded=True, size='235/60 R18', g_source="test"),
    "t_nokian_nordman_north_9": Tyre('Nokian Nordman North 9', C.WINTER_STUDDED, 1.253, mu_dry_override=0.8051, mu_snow_override=0.3932, mu_ice_override=0.2513, studded=True, size='225/45 R17', g_source="test"),
    "t_nokian_nordman_north_9_suv": Tyre('Nokian Nordman North 9 SUV', C.WINTER_STUDDED, 1.224, mu_dry_override=0.8012, mu_snow_override=0.3961, mu_ice_override=0.2425, studded=True, size='215/65 R17', g_source="test"),
    "t_nokian_nordman_north_rs3_suv": Tyre('Nokian Nordman North RS3 SUV', C.WINTER_NORDIC, 1.1, mu_dry_override=0.8317, mu_snow_override=0.3739, mu_ice_override=0.1966, size='235/60 R18', g_source="test"),
    "t_nokian_nordman_rs": Tyre('Nokian Nordman RS', C.WINTER_NORDIC, 0.972, mu_dry_override=0.7813, mu_snow_override=0.3499, mu_ice_override=0.147, size='205/55 R16', g_source="test"),
    "t_nokian_nordman_rs_2": Tyre('Nokian Nordman RS 2', C.WINTER_NORDIC, 1.088, mu_dry_override=0.8317, mu_snow_override=0.3627, mu_ice_override=0.1896, size='195/65 R15', g_source="test"),
    "t_nokian_nordman_rs2_suv": Tyre('Nokian Nordman RS2 SUV', C.WINTER_NORDIC, 1.15, mu_dry_override=0.8148, mu_snow_override=0.377, mu_ice_override=0.2086, size='215/65 R16', g_source="test"),
    "t_pirelli_ice_friction": Tyre('Pirelli Ice Friction', C.WINTER_NORDIC, 1.2, mu_dry_override=0.8571, mu_snow_override=0.3811, mu_ice_override=0.195, size='235/60 R18', g_source="test"),
    "t_pirelli_winter_icecontrol": Tyre('Pirelli Winter IceControl', C.WINTER_NORDIC, 1.143, mu_dry_override=0.8449, mu_snow_override=0.355, mu_ice_override=0.176, size='205/55 R16', g_source="test"),
    "t_pirelli_ice_zero": Tyre('Pirelli Ice Zero', C.WINTER_STUDDED, 1.266, mu_dry_override=0.8234, mu_snow_override=0.3696, mu_ice_override=0.2163, studded=True, size='195/65 R15', g_source="test"),
    "t_pirelli_ice_zero_asimmetrico": Tyre('Pirelli Ice Zero Asimmetrico', C.WINTER_NORDIC, 1.061, mu_dry_override=0.825, mu_snow_override=0.3752, mu_ice_override=0.1916, size='225/45 R17', g_source="test"),
    "t_pirelli_ice_zero_fr": Tyre('Pirelli Ice Zero FR', C.WINTER_NORDIC, 1.183, mu_dry_override=0.8483, mu_snow_override=0.3697, mu_ice_override=0.1948, size='195/65 R15', g_source="test"),
    "t_pirelli_scorpion_icezero_2": Tyre('Pirelli Scorpion IceZero 2', C.WINTER_STUDDED, 1.338, mu_dry_override=0.8262, mu_snow_override=0.3879, mu_ice_override=0.2072, studded=True, size='235/60 R18', g_source="test"),
    "t_radar_dimax_ice": Tyre('Radar Dimax Ice', C.WINTER_NORDIC, 1.078, mu_dry_override=0.8056, mu_snow_override=0.367, mu_ice_override=0.1483, size='225/45 R17', g_source="test"),
    "t_sailun_ice_blazer_wsl2": Tyre('Sailun Ice Blazer WSL2', C.WINTER_NORDIC, 1.158, mu_dry_override=0.8013, mu_snow_override=0.3443, mu_ice_override=0.1674, size='195/65 R15', g_source="test"),
    "t_sailun_ice_blazer_wst3": Tyre('Sailun Ice Blazer WST3', C.WINTER_STUDDED, 1.204, mu_dry_override=0.7906, mu_snow_override=0.3669, mu_ice_override=0.1691, studded=True, size='215/65 R16', g_source="test"),
    "t_sailun_winterpro_sw61": Tyre('Sailun Winterpro SW61', C.WINTER_NORDIC, 1.273, mu_dry_override=0.8543, mu_snow_override=0.3444, mu_ice_override=0.1799, size='205/55 R16', g_source="test"),
    "t_sava_eskimo_ice": Tyre('Sava Eskimo Ice', C.WINTER_NORDIC, 1.132, mu_dry_override=0.7824, mu_snow_override=0.3773, mu_ice_override=0.2105, size='205/55 R16', g_source="test"),
    "t_sava_eskimo_stud": Tyre('Sava Eskimo Stud', C.WINTER_STUDDED, 1.272, mu_dry_override=0.846, mu_snow_override=0.3752, mu_ice_override=0.186, studded=True, size='205/55 R16', g_source="test"),
    "t_tigar_ice": Tyre('Tigar Ice', C.WINTER_STUDDED, 1.384, mu_dry_override=0.8321, mu_snow_override=0.3545, mu_ice_override=0.1894, studded=True, size='205/55 R16', g_source="test"),
    "t_tigar_suv_ice": Tyre('Tigar SUV Ice', C.WINTER_STUDDED, 1.406, mu_dry_override=0.8983, mu_snow_override=0.3624, mu_ice_override=0.1709, studded=True, size='235/60 R18', g_source="test"),
    "t_toyo_observe_g3_ice": Tyre('Toyo Observe G3-Ice', C.WINTER_STUDDED, 1.207, mu_dry_override=0.8064, mu_snow_override=0.3672, mu_ice_override=0.1811, studded=True, size='185/65 R15', g_source="test"),
    "t_toyo_observe_gsi_5": Tyre('Toyo Observe GSi-5', C.WINTER_NORDIC, 0.98, mu_dry_override=0.781, mu_snow_override=0.365, mu_ice_override=0.1903, size='205/55 R16', g_source="test"),
    "t_toyo_observe_gsi_6": Tyre('Toyo Observe GSi-6', C.WINTER_NORDIC, 1.099, mu_dry_override=0.8347, mu_snow_override=0.367, mu_ice_override=0.1983, size='195/65 R15', g_source="test"),
    "t_toyo_observe_gsi_6_hp": Tyre('Toyo Observe GSi-6 HP', C.WINTER_NORDIC, 1.194, mu_dry_override=0.8428, mu_snow_override=0.369, mu_ice_override=0.19, size='205/55 R16', g_source="test"),
    "t_toyo_observe_ice_freezer": Tyre('Toyo Observe Ice-Freezer', C.WINTER_STUDDED, 1.202, mu_dry_override=0.8134, mu_snow_override=0.3627, mu_ice_override=0.1655, studded=True, size='205/60 R16', g_source="test"),
    "t_toyo_observe_ice_freezer_suv": Tyre('Toyo Observe Ice-Freezer SUV', C.WINTER_STUDDED, 1.177, mu_dry_override=0.8029, mu_snow_override=0.3768, mu_ice_override=0.1851, studded=True, size='215/65 R16', g_source="test"),
    "t_triangle_icelink": Tyre('Triangle IceLink', C.WINTER_STUDDED, 1.271, mu_dry_override=0.8549, mu_snow_override=0.3597, mu_ice_override=0.1767, studded=True, size='195/65 R15', g_source="test"),
    "t_triangle_icelink_sport_utility": Tyre('Triangle Icelink Sport Utility', C.WINTER_STUDDED, 1.315, mu_dry_override=0.8639, mu_snow_override=0.3718, mu_ice_override=0.1634, studded=True, size='215/65 R16', g_source="test"),
    "t_triangle_icelynx_ti501": Tyre('Triangle IceLynx TI501', C.WINTER_STUDDED, 1.453, mu_dry_override=0.8533, mu_snow_override=0.3821, mu_ice_override=0.1444, studded=True, size='235/60 R18', g_source="test"),
    "t_triangle_snowlink_pl01": Tyre('Triangle Snowlink PL01', C.WINTER_NORDIC, 1.09, mu_dry_override=0.8547, mu_snow_override=0.361, mu_ice_override=0.182, size='225/45 R17', g_source="test"),
    "t_vredestein_nord_trac_2": Tyre('Vredestein Nord-Trac 2', C.WINTER_NORDIC, 1.159, mu_dry_override=0.8696, mu_snow_override=0.3543, mu_ice_override=0.1605, size='205/55 R16', g_source="test"),
    "t_yokohama_iceguard_ig50_plus": Tyre('Yokohama iceGUARD iG50 Plus', C.WINTER_NORDIC, 1.17, mu_snow_override=0.3618, mu_ice_override=0.1578, size='205/55 R16', g_source="test"),
    "t_yokohama_iceguard_ig55": Tyre('Yokohama iceGUARD iG55', C.WINTER_STUDDED, 1.152, mu_dry_override=0.7905, mu_snow_override=0.359, mu_ice_override=0.182, studded=True, size='175/65 R14', g_source="test"),
    "t_yokohama_iceguard_ig60": Tyre('Yokohama IceGuard IG60', C.WINTER_NORDIC, 1.122, mu_dry_override=0.7972, mu_snow_override=0.377, mu_ice_override=0.2073, size='215/65 R16', g_source="test"),
    "t_yokohama_iceguard_ig65": Tyre('Yokohama iceGUARD iG65', C.WINTER_STUDDED, 1.297, mu_dry_override=0.842, mu_snow_override=0.375, mu_ice_override=0.2072, studded=True, size='235/60 R18', g_source="test"),
}

# mis testidest ja mitme vaatlusega iga väärtus tuli (leht näitab)
TULETUS = {
 "t_bfgoodrich_g_force_stud": {
  "nimi": "BFGoodrich g-Force Stud",
  "pinnad": {
   "ice": {
    "mu": 0.1835,
    "n": 3,
    "testid": [
     "MOOTTORI-2021-W-STUDDED-205-55R16",
     "TM-2013-W-205-55R16",
     "ZaRulem-2020-W-215-65R16-studded"
    ],
    "kaal": 0.69
   },
   "snow": {
    "mu": 0.3873,
    "n": 3,
    "testid": [
     "MOOTTORI-2021-W-STUDDED-205-55R16",
     "TM-2013-W-205-55R16",
     "ZaRulem-2020-W-215-65R16-studded"
    ],
    "kaal": 0.57
   },
   "dry": {
    "mu": 0.876,
    "n": 3,
    "testid": [
     "MOOTTORI-2021-W-STUDDED-205-55R16",
     "TM-2013-W-205-55R16",
     "ZaRulem-2020-W-215-65R16-studded"
    ],
    "kaal": 0.82
   },
   "wet": {
    "mu": 1.2561,
    "n": 3,
    "testid": [
     "MOOTTORI-2021-W-STUDDED-205-55R16",
     "TM-2013-W-205-55R16",
     "ZaRulem-2020-W-215-65R16-studded"
    ],
    "kaal": 0.82
   }
  },
  "testid": [
   "MOOTTORI-2021-W-STUDDED-205-55R16",
   "TM-2013-W-205-55R16",
   "ZaRulem-2020-W-215-65R16-studded"
  ],
  "viimane": 2021,
  "g_allikas": "test"
 },
 "t_bridgestone_blizzak_dm_v3": {
  "nimi": "Bridgestone Blizzak DM-V3",
  "pinnad": {
   "ice": {
    "mu": 0.1924,
    "n": 1,
    "testid": [
     "VIBILAGARE-2022-W-NORDIC-235-55R18"
    ],
    "kaal": 0.18
   },
   "snow": {
    "mu": 0.3753,
    "n": 1,
    "testid": [
     "VIBILAGARE-2022-W-NORDIC-235-55R18"
    ],
    "kaal": 0.3
   },
   "dry": {
    "mu": 0.8678,
    "n": 1,
    "testid": [
     "VIBILAGARE-2022-W-NORDIC-235-55R18"
    ],
    "kaal": 0.36
   },
   "wet": {
    "mu": 1.2168,
    "n": 1,
    "testid": [
     "VIBILAGARE-2022-W-NORDIC-235-55R18"
    ],
    "kaal": 0.36
   }
  },
  "testid": [
   "VIBILAGARE-2022-W-NORDIC-235-55R18"
  ],
  "viimane": 2022,
  "g_allikas": "test"
 },
 "t_bridgestone_blizzak_ice": {
  "nimi": "Bridgestone Blizzak Ice",
  "pinnad": {
   "ice": {
    "mu": 0.1919,
    "n": 3,
    "testid": [
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2023-W-NORDIC-225-45R17",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 0.72
   },
   "snow": {
    "mu": 0.3673,
    "n": 3,
    "testid": [
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2023-W-NORDIC-225-45R17",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 0.82
   },
   "dry": {
    "mu": 0.8643,
    "n": 4,
    "testid": [
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2023-W-NORDIC-225-45R17",
     "ViBilagare-2020-W-205-60R16",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 1.44
   },
   "wet": {
    "mu": 1.1291,
    "n": 4,
    "testid": [
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2023-W-NORDIC-225-45R17",
     "ViBilagare-2020-W-205-60R16",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 1.44
   }
  },
  "testid": [
   "TM-2020-W-205-55R16-mixed",
   "VIBILAGARE-2023-W-NORDIC-225-45R17",
   "ViBilagare-2020-W-205-60R16",
   "ZaRulem-2022-W-195-65R15-friction"
  ],
  "viimane": 2023,
  "g_allikas": "test"
 },
 "t_bridgestone_blizzak_revo_gz": {
  "nimi": "Bridgestone Blizzak Revo GZ",
  "pinnad": {
   "ice": {
    "mu": 0.1721,
    "n": 1,
    "testid": [
     "ZaRulem-2017-W-205-55R16-friction"
    ],
    "kaal": 0.09
   },
   "snow": {
    "mu": 0.3597,
    "n": 1,
    "testid": [
     "ZaRulem-2017-W-205-55R16-friction"
    ],
    "kaal": 0.18
   },
   "dry": {
    "mu": 0.8463,
    "n": 1,
    "testid": [
     "ZaRulem-2017-W-205-55R16-friction"
    ],
    "kaal": 0.18
   },
   "wet": {
    "mu": 1.1077,
    "n": 1,
    "testid": [
     "ZaRulem-2017-W-205-55R16-friction"
    ],
    "kaal": 0.18
   }
  },
  "testid": [
   "ZaRulem-2017-W-205-55R16-friction"
  ],
  "viimane": 2017,
  "g_allikas": "test"
 },
 "t_bridgestone_blizzak_spike_01": {
  "nimi": "Bridgestone Blizzak Spike-01",
  "pinnad": {
   "ice": {
    "mu": 0.1845,
    "n": 3,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "ZaRulem-2015-W-175-65R14-studded"
    ],
    "kaal": 0.32
   },
   "snow": {
    "mu": 0.3669,
    "n": 3,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "ZaRulem-2015-W-175-65R14-studded"
    ],
    "kaal": 0.39
   },
   "dry": {
    "mu": 0.8302,
    "n": 3,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "ZaRulem-2015-W-175-65R14-studded"
    ],
    "kaal": 0.39
   },
   "wet": {
    "mu": 1.1876,
    "n": 3,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "ZaRulem-2015-W-175-65R14-studded"
    ],
    "kaal": 0.39
   }
  },
  "testid": [
   "TM-2013-W-205-55R16",
   "TM-2015-W-205-55R16",
   "ZaRulem-2015-W-175-65R14-studded"
  ],
  "viimane": 2015,
  "g_allikas": "test"
 },
 "t_bridgestone_blizzak_spike_02": {
  "nimi": "Bridgestone Blizzak Spike-02",
  "pinnad": {
   "ice": {
    "mu": 0.2265,
    "n": 1,
    "testid": [
     "ZaRulem-2018-W-195-65R15-studded"
    ],
    "kaal": 0.1
   },
   "snow": {
    "mu": 0.3755,
    "n": 1,
    "testid": [
     "ZaRulem-2018-W-195-65R15-studded"
    ],
    "kaal": 0.2
   },
   "dry": {
    "mu": 0.7619,
    "n": 1,
    "testid": [
     "ZaRulem-2018-W-195-65R15-studded"
    ],
    "kaal": 0.2
   },
   "wet": {
    "mu": 1.1846,
    "n": 1,
    "testid": [
     "ZaRulem-2018-W-195-65R15-studded"
    ],
    "kaal": 0.2
   }
  },
  "testid": [
   "ZaRulem-2018-W-195-65R15-studded"
  ],
  "viimane": 2018,
  "g_allikas": "test"
 },
 "t_bridgestone_blizzak_vrx": {
  "nimi": "Bridgestone Blizzak VRX",
  "pinnad": {
   "ice": {
    "mu": 0.1791,
    "n": 3,
    "testid": [
     "ZaRulem-2015-W-175-65R14-friction",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2018-W-205-55R16-friction"
    ],
    "kaal": 0.25
   },
   "snow": {
    "mu": 0.3526,
    "n": 3,
    "testid": [
     "ZaRulem-2015-W-175-65R14-friction",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2018-W-205-55R16-friction"
    ],
    "kaal": 0.5
   },
   "dry": {
    "mu": 0.8508,
    "n": 3,
    "testid": [
     "ZaRulem-2015-W-175-65R14-friction",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2018-W-205-55R16-friction"
    ],
    "kaal": 0.5
   },
   "wet": {
    "mu": 1.1421,
    "n": 3,
    "testid": [
     "ZaRulem-2015-W-175-65R14-friction",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2018-W-205-55R16-friction"
    ],
    "kaal": 0.5
   }
  },
  "testid": [
   "ZaRulem-2015-W-175-65R14-friction",
   "ZaRulem-2016-W-225-45R17-friction",
   "ZaRulem-2018-W-205-55R16-friction"
  ],
  "viimane": 2018,
  "g_allikas": "test"
 },
 "t_bridgestone_blizzak_ws70": {
  "nimi": "Bridgestone Blizzak WS70",
  "pinnad": {
   "ice": {
    "mu": 0.1703,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   },
   "snow": {
    "mu": 0.3588,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   },
   "dry": {
    "mu": 0.889,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   },
   "wet": {
    "mu": 1.1394,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   }
  },
  "testid": [
   "TM-2013-W-205-55R16"
  ],
  "viimane": 2013,
  "g_allikas": "test"
 },
 "t_bridgestone_blizzak_ws80": {
  "nimi": "Bridgestone Blizzak WS80",
  "pinnad": {
   "ice": {
    "mu": 0.1712,
    "n": 2,
    "testid": [
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-friction"
    ],
    "kaal": 0.31
   },
   "snow": {
    "mu": 0.3625,
    "n": 2,
    "testid": [
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-friction"
    ],
    "kaal": 0.31
   },
   "dry": {
    "mu": 0.864,
    "n": 1,
    "testid": [
     "TM-2015-W-205-55R16"
    ],
    "kaal": 0.14
   },
   "wet": {
    "mu": 1.1175,
    "n": 1,
    "testid": [
     "TM-2015-W-205-55R16"
    ],
    "kaal": 0.14
   }
  },
  "testid": [
   "TM-2015-W-205-55R16",
   "TM-2016-W-205-55R16-friction"
  ],
  "viimane": 2016,
  "g_allikas": "test"
 },
 "t_bridgestone_noranza_001": {
  "nimi": "Bridgestone Noranza 001",
  "pinnad": {
   "ice": {
    "mu": 0.2302,
    "n": 5,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2016-W-205-55R16-studded",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ViBilagare-2019-W-225-50R17"
    ],
    "kaal": 1.19
   },
   "snow": {
    "mu": 0.3786,
    "n": 5,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2016-W-205-55R16-studded",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ViBilagare-2019-W-225-50R17"
    ],
    "kaal": 1.02
   },
   "dry": {
    "mu": 0.8088,
    "n": 3,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2018-W-STUDDED-205-55R16"
    ],
    "kaal": 0.89
   },
   "wet": {
    "mu": 1.2231,
    "n": 4,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ViBilagare-2019-W-225-50R17"
    ],
    "kaal": 1.18
   }
  },
  "testid": [
   "TEKNIKENSVARLD-2021-W-205-55R16",
   "TM-2016-W-205-55R16-studded",
   "TM-2020-W-205-55R16-mixed",
   "VIBILAGARE-2018-W-STUDDED-205-55R16",
   "ViBilagare-2019-W-225-50R17"
  ],
  "viimane": 2021,
  "g_allikas": "test"
 },
 "t_continental_contiicecontact": {
  "nimi": "Continental ContiIceContact",
  "pinnad": {
   "ice": {
    "mu": 0.2002,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   },
   "snow": {
    "mu": 0.371,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   },
   "dry": {
    "mu": 0.8633,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   },
   "wet": {
    "mu": 1.1173,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   }
  },
  "testid": [
   "TM-2013-W-205-55R16"
  ],
  "viimane": 2013,
  "g_allikas": "test"
 },
 "t_continental_icecontact_2": {
  "nimi": "Continental IceContact 2",
  "pinnad": {
   "ice": {
    "mu": 0.2199,
    "n": 8,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded",
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-studded",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ZaRulem-2015-W-175-65R14-studded",
     "ZaRulem-2016-W-195-65R15-studded",
     "ZaRulem-2017-W-185-65R15-studded",
     "ZaRulem-2018-W-195-65R15-studded"
    ],
    "kaal": 1.01
   },
   "snow": {
    "mu": 0.3838,
    "n": 8,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded",
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-studded",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ZaRulem-2015-W-175-65R14-studded",
     "ZaRulem-2016-W-195-65R15-studded",
     "ZaRulem-2017-W-185-65R15-studded",
     "ZaRulem-2018-W-195-65R15-studded"
    ],
    "kaal": 1.35
   },
   "dry": {
    "mu": 0.8287,
    "n": 7,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded",
     "TM-2015-W-205-55R16",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ZaRulem-2015-W-175-65R14-studded",
     "ZaRulem-2016-W-195-65R15-studded",
     "ZaRulem-2017-W-185-65R15-studded",
     "ZaRulem-2018-W-195-65R15-studded"
    ],
    "kaal": 1.19
   },
   "wet": {
    "mu": 1.2966,
    "n": 7,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded",
     "TM-2015-W-205-55R16",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ZaRulem-2015-W-175-65R14-studded",
     "ZaRulem-2016-W-195-65R15-studded",
     "ZaRulem-2017-W-185-65R15-studded",
     "ZaRulem-2018-W-195-65R15-studded"
    ],
    "kaal": 1.19
   }
  },
  "testid": [
   "AUTOCENTRE-2017-W-205-55R16-studded",
   "TM-2015-W-205-55R16",
   "TM-2016-W-205-55R16-studded",
   "VIBILAGARE-2018-W-STUDDED-205-55R16",
   "ZaRulem-2015-W-175-65R14-studded",
   "ZaRulem-2016-W-195-65R15-studded",
   "ZaRulem-2017-W-185-65R15-studded",
   "ZaRulem-2018-W-195-65R15-studded"
  ],
  "viimane": 2018,
  "g_allikas": "test"
 },
 "t_continental_icecontact_2_suv": {
  "nimi": "Continental IceContact 2 SUV",
  "pinnad": {
   "ice": {
    "mu": 0.2316,
    "n": 2,
    "testid": [
     "ZaRulem-2016-W-235-65R17-studded",
     "ZaRulem-2018-W-215-65R16-studded"
    ],
    "kaal": 0.18
   },
   "snow": {
    "mu": 0.3804,
    "n": 2,
    "testid": [
     "ZaRulem-2016-W-235-65R17-studded",
     "ZaRulem-2018-W-215-65R16-studded"
    ],
    "kaal": 0.36
   },
   "dry": {
    "mu": 0.8309,
    "n": 2,
    "testid": [
     "ZaRulem-2016-W-235-65R17-studded",
     "ZaRulem-2018-W-215-65R16-studded"
    ],
    "kaal": 0.36
   },
   "wet": {
    "mu": 1.2579,
    "n": 2,
    "testid": [
     "ZaRulem-2016-W-235-65R17-studded",
     "ZaRulem-2018-W-215-65R16-studded"
    ],
    "kaal": 0.36
   }
  },
  "testid": [
   "ZaRulem-2016-W-235-65R17-studded",
   "ZaRulem-2018-W-215-65R16-studded"
  ],
  "viimane": 2018,
  "g_allikas": "test"
 },
 "t_continental_contivikingcontact_5": {
  "nimi": "Continental ContiVikingContact 5",
  "pinnad": {
   "ice": {
    "mu": 0.1586,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   },
   "snow": {
    "mu": 0.3556,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   },
   "dry": {
    "mu": 0.8571,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   },
   "wet": {
    "mu": 1.1523,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   }
  },
  "testid": [
   "TM-2013-W-205-55R16"
  ],
  "viimane": 2013,
  "g_allikas": "test"
 },
 "t_continental_contivikingcontact_6": {
  "nimi": "Continental ContiVikingContact 6",
  "pinnad": {
   "ice": {
    "mu": 0.1742,
    "n": 5,
    "testid": [
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-friction",
     "ZaRulem-2015-W-175-65R14-friction",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction"
    ],
    "kaal": 0.55
   },
   "snow": {
    "mu": 0.3646,
    "n": 5,
    "testid": [
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-friction",
     "ZaRulem-2015-W-175-65R14-friction",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction"
    ],
    "kaal": 0.79
   },
   "dry": {
    "mu": 0.842,
    "n": 4,
    "testid": [
     "TM-2015-W-205-55R16",
     "ZaRulem-2015-W-175-65R14-friction",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction"
    ],
    "kaal": 0.61
   },
   "wet": {
    "mu": 1.2222,
    "n": 4,
    "testid": [
     "TM-2015-W-205-55R16",
     "ZaRulem-2015-W-175-65R14-friction",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction"
    ],
    "kaal": 0.61
   }
  },
  "testid": [
   "TM-2015-W-205-55R16",
   "TM-2016-W-205-55R16-friction",
   "ZaRulem-2015-W-175-65R14-friction",
   "ZaRulem-2016-W-225-45R17-friction",
   "ZaRulem-2017-W-205-55R16-friction"
  ],
  "viimane": 2017,
  "g_allikas": "test"
 },
 "t_continental_vikingcontact_7": {
  "nimi": "Continental VikingContact 7",
  "pinnad": {
   "ice": {
    "mu": 0.2115,
    "n": 12,
    "testid": [
     "MOOTTORI-2018-W-NORDIC-205-55R16-PARTIAL",
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2020-W-205-55R16-mixed",
     "TUULILASI-2018-W-NORDIC-205-55R16-PARTIAL",
     "VIBILAGARE-2022-W-NORDIC-235-55R18",
     "VIBILAGARE-2023-W-NORDIC-225-45R17",
     "ViBilagare-2019-W-225-50R17",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2021-W-215-65R16-friction",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 2.14
   },
   "snow": {
    "mu": 0.376,
    "n": 9,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2022-W-NORDIC-235-55R18",
     "VIBILAGARE-2023-W-NORDIC-225-45R17",
     "ViBilagare-2019-W-225-50R17",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2021-W-215-65R16-friction",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 2.23
   },
   "dry": {
    "mu": 0.8483,
    "n": 10,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2022-W-NORDIC-235-55R18",
     "VIBILAGARE-2023-W-NORDIC-225-45R17",
     "ViBilagare-2020-W-205-60R16",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2021-W-215-65R16-friction",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 3.2
   },
   "wet": {
    "mu": 1.1702,
    "n": 11,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2022-W-NORDIC-235-55R18",
     "VIBILAGARE-2023-W-NORDIC-225-45R17",
     "ViBilagare-2019-W-225-50R17",
     "ViBilagare-2020-W-205-60R16",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2021-W-215-65R16-friction",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 3.49
   }
  },
  "testid": [
   "MOOTTORI-2018-W-NORDIC-205-55R16-PARTIAL",
   "TEKNIKENSVARLD-2021-W-205-55R16",
   "TM-2020-W-205-55R16-mixed",
   "TUULILASI-2018-W-NORDIC-205-55R16-PARTIAL",
   "VIBILAGARE-2022-W-NORDIC-235-55R18",
   "VIBILAGARE-2023-W-NORDIC-225-45R17",
   "ViBilagare-2019-W-225-50R17",
   "ViBilagare-2020-W-205-60R16",
   "ZaRulem-2018-W-205-55R16-friction",
   "ZaRulem-2019-W-195-65R15-friction",
   "ZaRulem-2020-W-205-55R16-friction",
   "ZaRulem-2021-W-215-65R16-friction",
   "ZaRulem-2022-W-195-65R15-friction"
  ],
  "viimane": 2023,
  "g_allikas": "test"
 },
 "t_dunlop_grandtrek_ice_02": {
  "nimi": "Dunlop Grandtrek Ice 02",
  "pinnad": {
   "ice": {
    "mu": 0.1975,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-235-65R17-studded"
    ],
    "kaal": 0.08
   },
   "snow": {
    "mu": 0.3599,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-235-65R17-studded"
    ],
    "kaal": 0.16
   },
   "dry": {
    "mu": 0.804,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-235-65R17-studded"
    ],
    "kaal": 0.16
   },
   "wet": {
    "mu": 1.2127,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-235-65R17-studded"
    ],
    "kaal": 0.16
   }
  },
  "testid": [
   "ZaRulem-2016-W-235-65R17-studded"
  ],
  "viimane": 2016,
  "g_allikas": "test"
 },
 "t_dunlop_ice_touch": {
  "nimi": "Dunlop Ice Touch",
  "pinnad": {
   "ice": {
    "mu": 0.2139,
    "n": 1,
    "testid": [
     "TM-2015-W-205-55R16"
    ],
    "kaal": 0.14
   },
   "snow": {
    "mu": 0.3683,
    "n": 1,
    "testid": [
     "TM-2015-W-205-55R16"
    ],
    "kaal": 0.14
   },
   "dry": {
    "mu": 0.9151,
    "n": 1,
    "testid": [
     "TM-2015-W-205-55R16"
    ],
    "kaal": 0.14
   },
   "wet": {
    "mu": 1.2743,
    "n": 1,
    "testid": [
     "TM-2015-W-205-55R16"
    ],
    "kaal": 0.14
   }
  },
  "testid": [
   "TM-2015-W-205-55R16"
  ],
  "viimane": 2015,
  "g_allikas": "test"
 },
 "t_dunlop_winter_maxx_wm01": {
  "nimi": "Dunlop Winter Maxx WM01",
  "pinnad": {
   "ice": {
    "mu": 0.1859,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-225-45R17-friction"
    ],
    "kaal": 0.08
   },
   "snow": {
    "mu": 0.3605,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-225-45R17-friction"
    ],
    "kaal": 0.16
   },
   "dry": {
    "mu": 0.7915,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-225-45R17-friction"
    ],
    "kaal": 0.16
   },
   "wet": {
    "mu": 1.0911,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-225-45R17-friction"
    ],
    "kaal": 0.16
   }
  },
  "testid": [
   "ZaRulem-2016-W-225-45R17-friction"
  ],
  "viimane": 2016,
  "g_allikas": "test"
 },
 "t_dunlop_winter_maxx_wm02": {
  "nimi": "Dunlop Winter Maxx WM02",
  "pinnad": {
   "ice": {
    "mu": 0.1923,
    "n": 1,
    "testid": [
     "ZaRulem-2018-W-205-55R16-friction"
    ],
    "kaal": 0.1
   },
   "snow": {
    "mu": 0.3632,
    "n": 1,
    "testid": [
     "ZaRulem-2018-W-205-55R16-friction"
    ],
    "kaal": 0.2
   },
   "dry": {
    "mu": 0.7956,
    "n": 1,
    "testid": [
     "ZaRulem-2018-W-205-55R16-friction"
    ],
    "kaal": 0.2
   },
   "wet": {
    "mu": 1.1175,
    "n": 1,
    "testid": [
     "ZaRulem-2018-W-205-55R16-friction"
    ],
    "kaal": 0.2
   }
  },
  "testid": [
   "ZaRulem-2018-W-205-55R16-friction"
  ],
  "viimane": 2018,
  "g_allikas": "test"
 },
 "t_dunlop_sp_winter_ice_02": {
  "nimi": "Dunlop SP Winter Ice 02",
  "pinnad": {
   "ice": {
    "mu": 0.2143,
    "n": 2,
    "testid": [
     "ZaRulem-2016-W-195-65R15-studded",
     "ZaRulem-2017-W-185-65R15-studded"
    ],
    "kaal": 0.17
   },
   "snow": {
    "mu": 0.3769,
    "n": 2,
    "testid": [
     "ZaRulem-2016-W-195-65R15-studded",
     "ZaRulem-2017-W-185-65R15-studded"
    ],
    "kaal": 0.33
   },
   "dry": {
    "mu": 0.7968,
    "n": 2,
    "testid": [
     "ZaRulem-2016-W-195-65R15-studded",
     "ZaRulem-2017-W-185-65R15-studded"
    ],
    "kaal": 0.33
   },
   "wet": {
    "mu": 1.2232,
    "n": 2,
    "testid": [
     "ZaRulem-2016-W-195-65R15-studded",
     "ZaRulem-2017-W-185-65R15-studded"
    ],
    "kaal": 0.33
   }
  },
  "testid": [
   "ZaRulem-2016-W-195-65R15-studded",
   "ZaRulem-2017-W-185-65R15-studded"
  ],
  "viimane": 2017,
  "g_allikas": "test"
 },
 "t_falken_winterpeak_f_ice_1": {
  "nimi": "Falken Winterpeak F-Ice 1",
  "pinnad": {
   "ice": {
    "mu": 0.258,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18",
     "VIBILAGARE-2023-W-STUDDED-225-45R17"
    ],
    "kaal": 0.48
   },
   "snow": {
    "mu": 0.3856,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18",
     "VIBILAGARE-2023-W-STUDDED-225-45R17"
    ],
    "kaal": 0.55
   },
   "dry": {
    "mu": 0.7986,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18",
     "VIBILAGARE-2023-W-STUDDED-225-45R17"
    ],
    "kaal": 0.96
   },
   "wet": {
    "mu": 1.2518,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18",
     "VIBILAGARE-2023-W-STUDDED-225-45R17"
    ],
    "kaal": 0.96
   }
  },
  "testid": [
   "VIBILAGARE-2022-W-STUDDED-235-55R18",
   "VIBILAGARE-2023-W-STUDDED-225-45R17"
  ],
  "viimane": 2023,
  "g_allikas": "test"
 },
 "t_firestone_ice_cruiser_7": {
  "nimi": "Firestone Ice Cruiser 7",
  "pinnad": {
   "ice": {
    "mu": 0.1962,
    "n": 1,
    "testid": [
     "ZaRulem-2018-W-195-65R15-studded"
    ],
    "kaal": 0.1
   },
   "snow": {
    "mu": 0.348,
    "n": 1,
    "testid": [
     "ZaRulem-2018-W-195-65R15-studded"
    ],
    "kaal": 0.2
   },
   "dry": {
    "mu": 0.8103,
    "n": 1,
    "testid": [
     "ZaRulem-2018-W-195-65R15-studded"
    ],
    "kaal": 0.2
   },
   "wet": {
    "mu": 1.1674,
    "n": 1,
    "testid": [
     "ZaRulem-2018-W-195-65R15-studded"
    ],
    "kaal": 0.2
   }
  },
  "testid": [
   "ZaRulem-2018-W-195-65R15-studded"
  ],
  "viimane": 2018,
  "g_allikas": "test"
 },
 "t_gislaved_nord_frost_100": {
  "nimi": "Gislaved Nord Frost 100",
  "pinnad": {
   "ice": {
    "mu": 0.172,
    "n": 2,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16"
    ],
    "kaal": 0.25
   },
   "snow": {
    "mu": 0.3711,
    "n": 2,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16"
    ],
    "kaal": 0.25
   },
   "dry": {
    "mu": 0.8743,
    "n": 2,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16"
    ],
    "kaal": 0.25
   },
   "wet": {
    "mu": 1.3515,
    "n": 2,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16"
    ],
    "kaal": 0.25
   }
  },
  "testid": [
   "TM-2013-W-205-55R16",
   "TM-2015-W-205-55R16"
  ],
  "viimane": 2015,
  "g_allikas": "test"
 },
 "t_gislaved_nord_frost_200": {
  "nimi": "Gislaved Nord Frost 200",
  "pinnad": {
   "ice": {
    "mu": 0.2036,
    "n": 7,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded",
     "MOOTTORI-2021-W-STUDDED-205-55R16",
     "TM-2016-W-205-55R16-studded",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ZaRulem-2017-W-185-65R15-studded",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2019-W-205-55R16-studded"
    ],
    "kaal": 1.29
   },
   "snow": {
    "mu": 0.3855,
    "n": 7,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded",
     "MOOTTORI-2021-W-STUDDED-205-55R16",
     "TM-2016-W-205-55R16-studded",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ZaRulem-2017-W-185-65R15-studded",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2019-W-205-55R16-studded"
    ],
    "kaal": 1.33
   },
   "dry": {
    "mu": 0.8301,
    "n": 6,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded",
     "MOOTTORI-2021-W-STUDDED-205-55R16",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ZaRulem-2017-W-185-65R15-studded",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2019-W-205-55R16-studded"
    ],
    "kaal": 1.45
   },
   "wet": {
    "mu": 1.2232,
    "n": 6,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded",
     "MOOTTORI-2021-W-STUDDED-205-55R16",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ZaRulem-2017-W-185-65R15-studded",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2019-W-205-55R16-studded"
    ],
    "kaal": 1.45
   }
  },
  "testid": [
   "AUTOCENTRE-2017-W-205-55R16-studded",
   "MOOTTORI-2021-W-STUDDED-205-55R16",
   "TM-2016-W-205-55R16-studded",
   "VIBILAGARE-2018-W-STUDDED-205-55R16",
   "ZaRulem-2017-W-185-65R15-studded",
   "ZaRulem-2018-W-195-65R15-studded",
   "ZaRulem-2019-W-205-55R16-studded"
  ],
  "viimane": 2021,
  "g_allikas": "test"
 },
 "t_gislaved_nord_frost_200_suv": {
  "nimi": "Gislaved Nord Frost 200 SUV",
  "pinnad": {
   "ice": {
    "mu": 0.2055,
    "n": 2,
    "testid": [
     "ZaRulem-2018-W-215-65R16-studded",
     "ZaRulem-2020-W-215-65R16-studded"
    ],
    "kaal": 0.23
   },
   "snow": {
    "mu": 0.3846,
    "n": 2,
    "testid": [
     "ZaRulem-2018-W-215-65R16-studded",
     "ZaRulem-2020-W-215-65R16-studded"
    ],
    "kaal": 0.44
   },
   "dry": {
    "mu": 0.8639,
    "n": 2,
    "testid": [
     "ZaRulem-2018-W-215-65R16-studded",
     "ZaRulem-2020-W-215-65R16-studded"
    ],
    "kaal": 0.47
   },
   "wet": {
    "mu": 1.3776,
    "n": 2,
    "testid": [
     "ZaRulem-2018-W-215-65R16-studded",
     "ZaRulem-2020-W-215-65R16-studded"
    ],
    "kaal": 0.47
   }
  },
  "testid": [
   "ZaRulem-2018-W-215-65R16-studded",
   "ZaRulem-2020-W-215-65R16-studded"
  ],
  "viimane": 2020,
  "g_allikas": "test"
 },
 "t_gislaved_soft_frost_200": {
  "nimi": "Gislaved Soft Frost 200",
  "pinnad": {
   "ice": {
    "mu": 0.1848,
    "n": 2,
    "testid": [
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 0.24
   },
   "snow": {
    "mu": 0.362,
    "n": 2,
    "testid": [
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 0.47
   },
   "dry": {
    "mu": 0.8624,
    "n": 2,
    "testid": [
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 0.47
   },
   "wet": {
    "mu": 1.1057,
    "n": 2,
    "testid": [
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 0.47
   }
  },
  "testid": [
   "ZaRulem-2019-W-195-65R15-friction",
   "ZaRulem-2020-W-205-55R16-friction"
  ],
  "viimane": 2020,
  "g_allikas": "test"
 },
 "t_goodride_icemaster_spike_z_506": {
  "nimi": "Goodride IceMaster Spike Z-506",
  "pinnad": {
   "ice": {
    "mu": 0.2195,
    "n": 3,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "VIBILAGARE-2023-W-STUDDED-225-45R17",
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.93
   },
   "snow": {
    "mu": 0.3814,
    "n": 3,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "VIBILAGARE-2023-W-STUDDED-225-45R17",
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.93
   },
   "dry": {
    "mu": 0.8237,
    "n": 3,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "VIBILAGARE-2023-W-STUDDED-225-45R17",
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 1.47
   },
   "wet": {
    "mu": 1.2956,
    "n": 3,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "VIBILAGARE-2023-W-STUDDED-225-45R17",
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 1.47
   }
  },
  "testid": [
   "TEKNIKENSVARLD-2021-W-205-55R16",
   "VIBILAGARE-2023-W-STUDDED-225-45R17",
   "VIBILAGARE-2025-W-STUDDED-235-60R18"
  ],
  "viimane": 2025,
  "g_allikas": "test"
 },
 "t_goodyear_ultragrip_600": {
  "nimi": "Goodyear UltraGrip 600",
  "pinnad": {
   "ice": {
    "mu": 0.1821,
    "n": 1,
    "testid": [
     "ZaRulem-2021-W-205-55R16-studded"
    ],
    "kaal": 0.16
   },
   "snow": {
    "mu": 0.3726,
    "n": 1,
    "testid": [
     "ZaRulem-2021-W-205-55R16-studded"
    ],
    "kaal": 0.26
   },
   "dry": {
    "mu": 0.8346,
    "n": 1,
    "testid": [
     "ZaRulem-2021-W-205-55R16-studded"
    ],
    "kaal": 0.32
   },
   "wet": {
    "mu": 1.2759,
    "n": 1,
    "testid": [
     "ZaRulem-2021-W-205-55R16-studded"
    ],
    "kaal": 0.32
   }
  },
  "testid": [
   "ZaRulem-2021-W-205-55R16-studded"
  ],
  "viimane": 2021,
  "g_allikas": "test"
 },
 "t_goodyear_ultragrip_arctic_2_suv": {
  "nimi": "Goodyear UltraGrip Arctic 2 SUV",
  "pinnad": {
   "ice": {
    "mu": 0.2972,
    "n": 2,
    "testid": [
     "VIBILAGARE-2025-W-STUDDED-235-60R18",
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 0.43
   },
   "snow": {
    "mu": 0.3865,
    "n": 2,
    "testid": [
     "VIBILAGARE-2025-W-STUDDED-235-60R18",
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 0.72
   },
   "dry": {
    "mu": 0.8044,
    "n": 2,
    "testid": [
     "VIBILAGARE-2025-W-STUDDED-235-60R18",
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 0.87
   },
   "wet": {
    "mu": 1.3118,
    "n": 2,
    "testid": [
     "VIBILAGARE-2025-W-STUDDED-235-60R18",
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 0.87
   }
  },
  "testid": [
   "VIBILAGARE-2025-W-STUDDED-235-60R18",
   "ZaRulem-2022-W-235-60R18-studded"
  ],
  "viimane": 2025,
  "g_allikas": "test"
 },
 "t_goodyear_ultragrip_ice_2": {
  "nimi": "Goodyear UltraGrip Ice 2",
  "pinnad": {
   "ice": {
    "mu": 0.2049,
    "n": 11,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-friction",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2022-W-NORDIC-235-55R18",
     "ZaRulem-2015-W-175-65R14-friction",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 1.83
   },
   "snow": {
    "mu": 0.3721,
    "n": 10,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-friction",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2022-W-NORDIC-235-55R18",
     "ZaRulem-2015-W-175-65R14-friction",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 2.05
   },
   "dry": {
    "mu": 0.8534,
    "n": 11,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2015-W-205-55R16",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2022-W-NORDIC-235-55R18",
     "ViBilagare-2020-W-205-60R16",
     "ZaRulem-2015-W-175-65R14-friction",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 2.76
   },
   "wet": {
    "mu": 1.2667,
    "n": 11,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2015-W-205-55R16",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2022-W-NORDIC-235-55R18",
     "ViBilagare-2020-W-205-60R16",
     "ZaRulem-2015-W-175-65R14-friction",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 2.76
   }
  },
  "testid": [
   "TEKNIKENSVARLD-2021-W-205-55R16",
   "TM-2015-W-205-55R16",
   "TM-2016-W-205-55R16-friction",
   "TM-2020-W-205-55R16-mixed",
   "VIBILAGARE-2022-W-NORDIC-235-55R18",
   "ViBilagare-2020-W-205-60R16",
   "ZaRulem-2015-W-175-65R14-friction",
   "ZaRulem-2016-W-225-45R17-friction",
   "ZaRulem-2017-W-205-55R16-friction",
   "ZaRulem-2018-W-205-55R16-friction",
   "ZaRulem-2020-W-205-55R16-friction",
   "ZaRulem-2022-W-195-65R15-friction"
  ],
  "viimane": 2022,
  "g_allikas": "test"
 },
 "t_goodyear_ultragrip_ice_arctic": {
  "nimi": "Goodyear UltraGrip Ice Arctic",
  "pinnad": {
   "ice": {
    "mu": 0.2173,
    "n": 10,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded",
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-studded",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ViBilagare-2019-W-225-50R17",
     "ZaRulem-2016-W-195-65R15-studded",
     "ZaRulem-2017-W-185-65R15-studded",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2018-W-215-65R16-studded"
    ],
    "kaal": 1.29
   },
   "snow": {
    "mu": 0.3819,
    "n": 10,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded",
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-studded",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ViBilagare-2019-W-225-50R17",
     "ZaRulem-2016-W-195-65R15-studded",
     "ZaRulem-2017-W-185-65R15-studded",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2018-W-215-65R16-studded"
    ],
    "kaal": 1.71
   },
   "dry": {
    "mu": 0.8314,
    "n": 8,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded",
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ZaRulem-2016-W-195-65R15-studded",
     "ZaRulem-2017-W-185-65R15-studded",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2018-W-215-65R16-studded"
    ],
    "kaal": 1.36
   },
   "wet": {
    "mu": 1.2641,
    "n": 9,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded",
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ViBilagare-2019-W-225-50R17",
     "ZaRulem-2016-W-195-65R15-studded",
     "ZaRulem-2017-W-185-65R15-studded",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2018-W-215-65R16-studded"
    ],
    "kaal": 1.64
   }
  },
  "testid": [
   "AUTOCENTRE-2017-W-205-55R16-studded",
   "TM-2013-W-205-55R16",
   "TM-2015-W-205-55R16",
   "TM-2016-W-205-55R16-studded",
   "VIBILAGARE-2018-W-STUDDED-205-55R16",
   "ViBilagare-2019-W-225-50R17",
   "ZaRulem-2016-W-195-65R15-studded",
   "ZaRulem-2017-W-185-65R15-studded",
   "ZaRulem-2018-W-195-65R15-studded",
   "ZaRulem-2018-W-215-65R16-studded"
  ],
  "viimane": 2019,
  "g_allikas": "test"
 },
 "t_goodyear_ultragrip_ice_arctic_suv_4x4": {
  "nimi": "Goodyear UltraGrip Ice Arctic SUV 4x4",
  "pinnad": {
   "ice": {
    "mu": 0.2158,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-235-65R17-studded"
    ],
    "kaal": 0.08
   },
   "snow": {
    "mu": 0.3722,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-235-65R17-studded"
    ],
    "kaal": 0.16
   },
   "dry": {
    "mu": 0.8234,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-235-65R17-studded"
    ],
    "kaal": 0.16
   },
   "wet": {
    "mu": 1.2972,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-235-65R17-studded"
    ],
    "kaal": 0.16
   }
  },
  "testid": [
   "ZaRulem-2016-W-235-65R17-studded"
  ],
  "viimane": 2016,
  "g_allikas": "test"
 },
 "t_gt_radial_champiro_ice_pro": {
  "nimi": "GT Radial Champiro Ice Pro",
  "pinnad": {
   "ice": {
    "mu": 0.1555,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   },
   "snow": {
    "mu": 0.3316,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   },
   "dry": {
    "mu": 0.8957,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   },
   "wet": {
    "mu": 1.2331,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   }
  },
  "testid": [
   "TM-2013-W-205-55R16"
  ],
  "viimane": 2013,
  "g_allikas": "test"
 },
 "t_gt_radial_ice_pro_3": {
  "nimi": "GT Radial Ice Pro 3",
  "pinnad": {
   "ice": {
    "mu": 0.1895,
    "n": 2,
    "testid": [
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2022-W-195-65R15-studded"
    ],
    "kaal": 0.28
   },
   "snow": {
    "mu": 0.3825,
    "n": 2,
    "testid": [
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2022-W-195-65R15-studded"
    ],
    "kaal": 0.5
   },
   "dry": {
    "mu": 0.8207,
    "n": 3,
    "testid": [
     "VIBILAGARE-2020-W-STUDDED-205-60R16",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2022-W-195-65R15-studded"
    ],
    "kaal": 0.92
   },
   "wet": {
    "mu": 1.2724,
    "n": 3,
    "testid": [
     "VIBILAGARE-2020-W-STUDDED-205-60R16",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2022-W-195-65R15-studded"
    ],
    "kaal": 0.92
   }
  },
  "testid": [
   "VIBILAGARE-2020-W-STUDDED-205-60R16",
   "ZaRulem-2018-W-195-65R15-studded",
   "ZaRulem-2022-W-195-65R15-studded"
  ],
  "viimane": 2022,
  "g_allikas": "test"
 },
 "t_hankook_winter_i_cept_iz2": {
  "nimi": "Hankook Winter i*cept iZ2",
  "pinnad": {
   "ice": {
    "mu": 0.1908,
    "n": 9,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2016-W-205-55R16-friction",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2024-W-NORDIC-225-45R17",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2021-W-215-65R16-friction"
    ],
    "kaal": 1.76
   },
   "snow": {
    "mu": 0.369,
    "n": 9,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2016-W-205-55R16-friction",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2024-W-NORDIC-225-45R17",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2021-W-215-65R16-friction"
    ],
    "kaal": 2.0
   },
   "dry": {
    "mu": 0.82,
    "n": 8,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2024-W-NORDIC-225-45R17",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2021-W-215-65R16-friction"
    ],
    "kaal": 2.49
   },
   "wet": {
    "mu": 1.1397,
    "n": 8,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2024-W-NORDIC-225-45R17",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2021-W-215-65R16-friction"
    ],
    "kaal": 2.49
   }
  },
  "testid": [
   "TEKNIKENSVARLD-2021-W-205-55R16",
   "TM-2016-W-205-55R16-friction",
   "TM-2020-W-205-55R16-mixed",
   "VIBILAGARE-2024-W-NORDIC-225-45R17",
   "ZaRulem-2016-W-225-45R17-friction",
   "ZaRulem-2017-W-205-55R16-friction",
   "ZaRulem-2019-W-195-65R15-friction",
   "ZaRulem-2020-W-205-55R16-friction",
   "ZaRulem-2021-W-215-65R16-friction"
  ],
  "viimane": 2024,
  "g_allikas": "test"
 },
 "t_hankook_winter_i_cept_iz3_x": {
  "nimi": "Hankook Winter i*cept iZ3 X",
  "pinnad": {
   "ice": {
    "mu": 0.1801,
    "n": 1,
    "testid": [
     "VIBILAGARE-2025-W-NORDIC-235-60R18"
    ],
    "kaal": 0.29
   },
   "snow": {
    "mu": 0.3779,
    "n": 1,
    "testid": [
     "VIBILAGARE-2025-W-NORDIC-235-60R18"
    ],
    "kaal": 0.39
   },
   "dry": {
    "mu": 0.8286,
    "n": 1,
    "testid": [
     "VIBILAGARE-2025-W-NORDIC-235-60R18"
    ],
    "kaal": 0.57
   },
   "wet": {
    "mu": 1.1096,
    "n": 1,
    "testid": [
     "VIBILAGARE-2025-W-NORDIC-235-60R18"
    ],
    "kaal": 0.57
   }
  },
  "testid": [
   "VIBILAGARE-2025-W-NORDIC-235-60R18"
  ],
  "viimane": 2025,
  "g_allikas": "test"
 },
 "t_hankook_winter_i_pike_rs": {
  "nimi": "Hankook Winter i*Pike RS+",
  "pinnad": {
   "ice": {
    "mu": 0.2005,
    "n": 2,
    "testid": [
     "TM-2016-W-205-55R16-studded",
     "ZaRulem-2016-W-195-65R15-studded"
    ],
    "kaal": 0.24
   },
   "snow": {
    "mu": 0.3769,
    "n": 2,
    "testid": [
     "TM-2016-W-205-55R16-studded",
     "ZaRulem-2016-W-195-65R15-studded"
    ],
    "kaal": 0.31
   },
   "dry": {
    "mu": 0.7853,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-195-65R15-studded"
    ],
    "kaal": 0.16
   },
   "wet": {
    "mu": 1.2127,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-195-65R15-studded"
    ],
    "kaal": 0.16
   }
  },
  "testid": [
   "TM-2016-W-205-55R16-studded",
   "ZaRulem-2016-W-195-65R15-studded"
  ],
  "viimane": 2016,
  "g_allikas": "test"
 },
 "t_hankook_winter_i_pike_rs2": {
  "nimi": "Hankook Winter i*Pike RS2",
  "pinnad": {
   "ice": {
    "mu": 0.2377,
    "n": 9,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2023-W-STUDDED-225-45R17",
     "ViBilagare-2019-W-225-50R17",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2019-W-205-55R16-studded",
     "ZaRulem-2020-W-215-65R16-studded",
     "ZaRulem-2020-W-225-45R17-studded",
     "ZaRulem-2021-W-205-55R16-studded"
    ],
    "kaal": 1.78
   },
   "snow": {
    "mu": 0.387,
    "n": 9,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2023-W-STUDDED-225-45R17",
     "ViBilagare-2019-W-225-50R17",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2019-W-205-55R16-studded",
     "ZaRulem-2020-W-215-65R16-studded",
     "ZaRulem-2020-W-225-45R17-studded",
     "ZaRulem-2021-W-205-55R16-studded"
    ],
    "kaal": 2.08
   },
   "dry": {
    "mu": 0.8087,
    "n": 9,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2020-W-STUDDED-205-60R16",
     "VIBILAGARE-2023-W-STUDDED-225-45R17",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2019-W-205-55R16-studded",
     "ZaRulem-2020-W-215-65R16-studded",
     "ZaRulem-2020-W-225-45R17-studded",
     "ZaRulem-2021-W-205-55R16-studded"
    ],
    "kaal": 2.95
   },
   "wet": {
    "mu": 1.2452,
    "n": 10,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2020-W-STUDDED-205-60R16",
     "VIBILAGARE-2023-W-STUDDED-225-45R17",
     "ViBilagare-2019-W-225-50R17",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2019-W-205-55R16-studded",
     "ZaRulem-2020-W-215-65R16-studded",
     "ZaRulem-2020-W-225-45R17-studded",
     "ZaRulem-2021-W-205-55R16-studded"
    ],
    "kaal": 3.23
   }
  },
  "testid": [
   "TEKNIKENSVARLD-2021-W-205-55R16",
   "TM-2020-W-205-55R16-mixed",
   "VIBILAGARE-2020-W-STUDDED-205-60R16",
   "VIBILAGARE-2023-W-STUDDED-225-45R17",
   "ViBilagare-2019-W-225-50R17",
   "ZaRulem-2018-W-195-65R15-studded",
   "ZaRulem-2019-W-205-55R16-studded",
   "ZaRulem-2020-W-215-65R16-studded",
   "ZaRulem-2020-W-225-45R17-studded",
   "ZaRulem-2021-W-205-55R16-studded"
  ],
  "viimane": 2023,
  "g_allikas": "test"
 },
 "t_hankook_winter_i_pike_x": {
  "nimi": "Hankook Winter i*Pike X",
  "pinnad": {
   "ice": {
    "mu": 0.1782,
    "n": 1,
    "testid": [
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 0.18
   },
   "snow": {
    "mu": 0.3685,
    "n": 1,
    "testid": [
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 0.3
   },
   "dry": {
    "mu": 0.8567,
    "n": 1,
    "testid": [
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 0.36
   },
   "wet": {
    "mu": 1.2541,
    "n": 1,
    "testid": [
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 0.36
   }
  },
  "testid": [
   "ZaRulem-2022-W-235-60R18-studded"
  ],
  "viimane": 2022,
  "g_allikas": "test"
 },
 "t_kormoran_stud_2": {
  "nimi": "Kormoran Stud 2",
  "pinnad": {
   "ice": {
    "mu": 0.1887,
    "n": 1,
    "testid": [
     "ZaRulem-2022-W-195-65R15-studded"
    ],
    "kaal": 0.18
   },
   "snow": {
    "mu": 0.3575,
    "n": 1,
    "testid": [
     "ZaRulem-2022-W-195-65R15-studded"
    ],
    "kaal": 0.3
   },
   "dry": {
    "mu": 0.8346,
    "n": 1,
    "testid": [
     "ZaRulem-2022-W-195-65R15-studded"
    ],
    "kaal": 0.36
   },
   "wet": {
    "mu": 1.3678,
    "n": 1,
    "testid": [
     "ZaRulem-2022-W-195-65R15-studded"
    ],
    "kaal": 0.36
   }
  },
  "testid": [
   "ZaRulem-2022-W-195-65R15-studded"
  ],
  "viimane": 2022,
  "g_allikas": "test"
 },
 "t_kumho_wintercraft_ice_wi31": {
  "nimi": "Kumho WinterCraft Ice Wi31",
  "pinnad": {
   "ice": {
    "mu": 0.1892,
    "n": 1,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded"
    ],
    "kaal": 0.18
   },
   "snow": {
    "mu": 0.3581,
    "n": 1,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded"
    ],
    "kaal": 0.18
   },
   "dry": {
    "mu": 0.8373,
    "n": 1,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded"
    ],
    "kaal": 0.18
   },
   "wet": {
    "mu": 1.2302,
    "n": 1,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded"
    ],
    "kaal": 0.18
   }
  },
  "testid": [
   "AUTOCENTRE-2017-W-205-55R16-studded"
  ],
  "viimane": 2017,
  "g_allikas": "test"
 },
 "t_kumho_wintercraft_ice_wi51": {
  "nimi": "Kumho WinterCraft Ice Wi51",
  "pinnad": {
   "ice": {
    "mu": 0.2021,
    "n": 1,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16"
    ],
    "kaal": 0.4
   },
   "snow": {
    "mu": 0.3771,
    "n": 1,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16"
    ],
    "kaal": 0.23
   },
   "dry": {
    "mu": 0.82,
    "n": 1,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16"
    ],
    "kaal": 0.4
   },
   "wet": {
    "mu": 1.3041,
    "n": 1,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16"
    ],
    "kaal": 0.4
   }
  },
  "testid": [
   "TEKNIKENSVARLD-2021-W-205-55R16"
  ],
  "viimane": 2021,
  "g_allikas": "test"
 },
 "t_kumho_wintercraft_ws51": {
  "nimi": "Kumho WinterCraft WS51",
  "pinnad": {
   "ice": {
    "mu": 0.1793,
    "n": 1,
    "testid": [
     "VIBILAGARE-2022-W-NORDIC-235-55R18"
    ],
    "kaal": 0.18
   },
   "snow": {
    "mu": 0.3702,
    "n": 1,
    "testid": [
     "VIBILAGARE-2022-W-NORDIC-235-55R18"
    ],
    "kaal": 0.3
   },
   "dry": {
    "mu": 0.8225,
    "n": 1,
    "testid": [
     "VIBILAGARE-2022-W-NORDIC-235-55R18"
    ],
    "kaal": 0.36
   },
   "wet": {
    "mu": 1.2349,
    "n": 1,
    "testid": [
     "VIBILAGARE-2022-W-NORDIC-235-55R18"
    ],
    "kaal": 0.36
   }
  },
  "testid": [
   "VIBILAGARE-2022-W-NORDIC-235-55R18"
  ],
  "viimane": 2022,
  "g_allikas": "test"
 },
 "t_linglong_greenmax_winter_grip": {
  "nimi": "Linglong GreenMax Winter Grip",
  "pinnad": {
   "ice": {
    "mu": 0.1609,
    "n": 1,
    "testid": [
     "TM-2015-W-205-55R16"
    ],
    "kaal": 0.14
   },
   "snow": {
    "mu": 0.3607,
    "n": 1,
    "testid": [
     "TM-2015-W-205-55R16"
    ],
    "kaal": 0.14
   },
   "dry": {
    "mu": 0.9238,
    "n": 1,
    "testid": [
     "TM-2015-W-205-55R16"
    ],
    "kaal": 0.14
   },
   "wet": {
    "mu": 1.2452,
    "n": 1,
    "testid": [
     "TM-2015-W-205-55R16"
    ],
    "kaal": 0.14
   }
  },
  "testid": [
   "TM-2015-W-205-55R16"
  ],
  "viimane": 2015,
  "g_allikas": "test"
 },
 "t_linglong_green_max_winter_grip_2": {
  "nimi": "Linglong Green-Max Winter Grip 2",
  "pinnad": {
   "ice": {
    "mu": 0.2302,
    "n": 1,
    "testid": [
     "TM-2020-W-205-55R16-mixed"
    ],
    "kaal": 0.29
   },
   "snow": {
    "mu": 0.3855,
    "n": 1,
    "testid": [
     "TM-2020-W-205-55R16-mixed"
    ],
    "kaal": 0.23
   },
   "dry": {
    "mu": 0.8514,
    "n": 1,
    "testid": [
     "TM-2020-W-205-55R16-mixed"
    ],
    "kaal": 0.29
   },
   "wet": {
    "mu": 1.1712,
    "n": 1,
    "testid": [
     "TM-2020-W-205-55R16-mixed"
    ],
    "kaal": 0.29
   }
  },
  "testid": [
   "TM-2020-W-205-55R16-mixed"
  ],
  "viimane": 2020,
  "g_allikas": "test"
 },
 "t_linglong_winter_unicorn": {
  "nimi": "Linglong Winter Unicorn",
  "pinnad": {
   "ice": {
    "mu": 0.2031,
    "n": 1,
    "testid": [
     "TM-2020-W-205-55R16-mixed"
    ],
    "kaal": 0.29
   },
   "snow": {
    "mu": 0.3817,
    "n": 1,
    "testid": [
     "TM-2020-W-205-55R16-mixed"
    ],
    "kaal": 0.23
   },
   "dry": {
    "mu": 0.84,
    "n": 1,
    "testid": [
     "TM-2020-W-205-55R16-mixed"
    ],
    "kaal": 0.29
   },
   "wet": {
    "mu": 1.0814,
    "n": 1,
    "testid": [
     "TM-2020-W-205-55R16-mixed"
    ],
    "kaal": 0.29
   }
  },
  "testid": [
   "TM-2020-W-205-55R16-mixed"
  ],
  "viimane": 2020,
  "g_allikas": "test"
 },
 "t_marshal_i_zen_kw31": {
  "nimi": "Marshal I'Zen KW31",
  "pinnad": {
   "ice": {
    "mu": 0.1868,
    "n": 1,
    "testid": [
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 0.12
   },
   "snow": {
    "mu": 0.3552,
    "n": 1,
    "testid": [
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 0.25
   },
   "dry": {
    "mu": 0.8463,
    "n": 1,
    "testid": [
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 0.25
   },
   "wet": {
    "mu": 1.0396,
    "n": 1,
    "testid": [
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 0.25
   }
  },
  "testid": [
   "ZaRulem-2020-W-205-55R16-friction"
  ],
  "viimane": 2020,
  "g_allikas": "test"
 },
 "t_matador_mp_30_sibir_ice_2": {
  "nimi": "Matador MP 30 Sibir Ice 2",
  "pinnad": {
   "ice": {
    "mu": 0.1791,
    "n": 2,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded",
     "ZaRulem-2016-W-195-65R15-studded"
    ],
    "kaal": 0.26
   },
   "snow": {
    "mu": 0.3744,
    "n": 2,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded",
     "ZaRulem-2016-W-195-65R15-studded"
    ],
    "kaal": 0.33
   },
   "dry": {
    "mu": 0.8209,
    "n": 2,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded",
     "ZaRulem-2016-W-195-65R15-studded"
    ],
    "kaal": 0.33
   },
   "wet": {
    "mu": 1.2858,
    "n": 2,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded",
     "ZaRulem-2016-W-195-65R15-studded"
    ],
    "kaal": 0.33
   }
  },
  "testid": [
   "AUTOCENTRE-2017-W-205-55R16-studded",
   "ZaRulem-2016-W-195-65R15-studded"
  ],
  "viimane": 2017,
  "g_allikas": "test"
 },
 "t_maxxis_premitra_ice_nord_5_suv": {
  "nimi": "Maxxis Premitra Ice Nord 5 SUV",
  "pinnad": {
   "ice": {
    "mu": 0.1992,
    "n": 1,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18"
    ],
    "kaal": 0.2
   },
   "snow": {
    "mu": 0.3419,
    "n": 1,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18"
    ],
    "kaal": 0.28
   },
   "dry": {
    "mu": 0.886,
    "n": 1,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18"
    ],
    "kaal": 0.4
   },
   "wet": {
    "mu": 1.3341,
    "n": 1,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18"
    ],
    "kaal": 0.4
   }
  },
  "testid": [
   "VIBILAGARE-2022-W-STUDDED-235-55R18"
  ],
  "viimane": 2022,
  "g_allikas": "test"
 },
 "t_michelin_latitude_x_ice_north_2": {
  "nimi": "Michelin Latitude X-Ice North 2+",
  "pinnad": {
   "ice": {
    "mu": 0.1629,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-235-65R17-studded"
    ],
    "kaal": 0.08
   },
   "snow": {
    "mu": 0.3701,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-235-65R17-studded"
    ],
    "kaal": 0.16
   },
   "dry": {
    "mu": 0.8259,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-235-65R17-studded"
    ],
    "kaal": 0.16
   },
   "wet": {
    "mu": 1.2719,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-235-65R17-studded"
    ],
    "kaal": 0.16
   }
  },
  "testid": [
   "ZaRulem-2016-W-235-65R17-studded"
  ],
  "viimane": 2016,
  "g_allikas": "test"
 },
 "t_michelin_x_ice_3": {
  "nimi": "Michelin X-Ice 3",
  "pinnad": {
   "ice": {
    "mu": 0.1986,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-225-45R17-friction"
    ],
    "kaal": 0.08
   },
   "snow": {
    "mu": 0.356,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-225-45R17-friction"
    ],
    "kaal": 0.16
   },
   "dry": {
    "mu": 0.8392,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-225-45R17-friction"
    ],
    "kaal": 0.16
   },
   "wet": {
    "mu": 1.1529,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-225-45R17-friction"
    ],
    "kaal": 0.16
   }
  },
  "testid": [
   "ZaRulem-2016-W-225-45R17-friction"
  ],
  "viimane": 2016,
  "g_allikas": "test"
 },
 "t_michelin_x_ice_north_3": {
  "nimi": "Michelin X-Ice North 3",
  "pinnad": {
   "ice": {
    "mu": 0.1757,
    "n": 5,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-studded",
     "ZaRulem-2016-W-195-65R15-studded",
     "ZaRulem-2018-W-215-65R16-studded"
    ],
    "kaal": 0.59
   },
   "snow": {
    "mu": 0.3739,
    "n": 5,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-studded",
     "ZaRulem-2016-W-195-65R15-studded",
     "ZaRulem-2018-W-215-65R16-studded"
    ],
    "kaal": 0.77
   },
   "dry": {
    "mu": 0.8211,
    "n": 4,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "ZaRulem-2016-W-195-65R15-studded",
     "ZaRulem-2018-W-215-65R16-studded"
    ],
    "kaal": 0.61
   },
   "wet": {
    "mu": 1.1758,
    "n": 4,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "ZaRulem-2016-W-195-65R15-studded",
     "ZaRulem-2018-W-215-65R16-studded"
    ],
    "kaal": 0.61
   }
  },
  "testid": [
   "TM-2013-W-205-55R16",
   "TM-2015-W-205-55R16",
   "TM-2016-W-205-55R16-studded",
   "ZaRulem-2016-W-195-65R15-studded",
   "ZaRulem-2018-W-215-65R16-studded"
  ],
  "viimane": 2018,
  "g_allikas": "test"
 },
 "t_michelin_x_ice_north_4_suv": {
  "nimi": "Michelin X-Ice North 4 SUV",
  "pinnad": {
   "ice": {
    "mu": 0.2593,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18",
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.46
   },
   "snow": {
    "mu": 0.3862,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18",
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.7
   },
   "dry": {
    "mu": 0.8007,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18",
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.91
   },
   "wet": {
    "mu": 1.2386,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18",
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.91
   }
  },
  "testid": [
   "VIBILAGARE-2022-W-STUDDED-235-55R18",
   "VIBILAGARE-2025-W-STUDDED-235-60R18"
  ],
  "viimane": 2025,
  "g_allikas": "test"
 },
 "t_michelin_x_ice_snow_suv": {
  "nimi": "Michelin X-Ice Snow SUV",
  "pinnad": {
   "ice": {
    "mu": 0.1978,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-NORDIC-235-55R18",
     "VIBILAGARE-2025-W-NORDIC-235-60R18"
    ],
    "kaal": 0.47
   },
   "snow": {
    "mu": 0.3782,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-NORDIC-235-55R18",
     "VIBILAGARE-2025-W-NORDIC-235-60R18"
    ],
    "kaal": 0.69
   },
   "dry": {
    "mu": 0.7951,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-NORDIC-235-55R18",
     "VIBILAGARE-2025-W-NORDIC-235-60R18"
    ],
    "kaal": 0.93
   },
   "wet": {
    "mu": 1.1107,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-NORDIC-235-55R18",
     "VIBILAGARE-2025-W-NORDIC-235-60R18"
    ],
    "kaal": 0.93
   }
  },
  "testid": [
   "VIBILAGARE-2022-W-NORDIC-235-55R18",
   "VIBILAGARE-2025-W-NORDIC-235-60R18"
  ],
  "viimane": 2025,
  "g_allikas": "test"
 },
 "t_michelin_x_ice_xi3": {
  "nimi": "Michelin X-Ice XI3",
  "pinnad": {
   "ice": {
    "mu": 0.1692,
    "n": 3,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-friction"
    ],
    "kaal": 0.42
   },
   "snow": {
    "mu": 0.3625,
    "n": 3,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-friction"
    ],
    "kaal": 0.42
   },
   "dry": {
    "mu": 0.8252,
    "n": 2,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16"
    ],
    "kaal": 0.25
   },
   "wet": {
    "mu": 1.1709,
    "n": 2,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16"
    ],
    "kaal": 0.25
   }
  },
  "testid": [
   "TM-2013-W-205-55R16",
   "TM-2015-W-205-55R16",
   "TM-2016-W-205-55R16-friction"
  ],
  "viimane": 2016,
  "g_allikas": "test"
 },
 "t_nankang_ice_activa_2": {
  "nimi": "Nankang Ice Activa 2",
  "pinnad": {
   "ice": {
    "mu": 0.1924,
    "n": 1,
    "testid": [
     "TM-2020-W-205-55R16-mixed"
    ],
    "kaal": 0.29
   },
   "snow": {
    "mu": 0.378,
    "n": 1,
    "testid": [
     "TM-2020-W-205-55R16-mixed"
    ],
    "kaal": 0.23
   },
   "dry": {
    "mu": 0.7923,
    "n": 1,
    "testid": [
     "TM-2020-W-205-55R16-mixed"
    ],
    "kaal": 0.29
   },
   "wet": {
    "mu": 1.1436,
    "n": 1,
    "testid": [
     "TM-2020-W-205-55R16-mixed"
    ],
    "kaal": 0.29
   }
  },
  "testid": [
   "TM-2020-W-205-55R16-mixed"
  ],
  "viimane": 2020,
  "g_allikas": "test"
 },
 "t_nankang_ice_activa_grip_2_suv": {
  "nimi": "Nankang Ice Activa Grip 2 SUV",
  "pinnad": {
   "ice": {
    "mu": 0.2349,
    "n": 1,
    "testid": [
     "VIBILAGARE-2026-W-STUDDED-215-65R17"
    ],
    "kaal": 0.43
   },
   "snow": {
    "mu": 0.3995,
    "n": 1,
    "testid": [
     "VIBILAGARE-2026-W-STUDDED-215-65R17"
    ],
    "kaal": 0.36
   },
   "dry": {
    "mu": 0.7954,
    "n": 1,
    "testid": [
     "VIBILAGARE-2026-W-STUDDED-215-65R17"
    ],
    "kaal": 0.86
   },
   "wet": {
    "mu": 1.1549,
    "n": 1,
    "testid": [
     "VIBILAGARE-2026-W-STUDDED-215-65R17"
    ],
    "kaal": 0.86
   }
  },
  "testid": [
   "VIBILAGARE-2026-W-STUDDED-215-65R17"
  ],
  "viimane": 2026,
  "g_allikas": "test"
 },
 "t_nankang_ice_activa_ice_1": {
  "nimi": "Nankang Ice Activa Ice-1",
  "pinnad": {
   "ice": {
    "mu": 0.1466,
    "n": 3,
    "testid": [
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-friction",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 0.49
   },
   "snow": {
    "mu": 0.3648,
    "n": 3,
    "testid": [
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-friction",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 0.61
   },
   "dry": {
    "mu": 0.8361,
    "n": 2,
    "testid": [
     "TM-2015-W-205-55R16",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 0.5
   },
   "wet": {
    "mu": 1.2451,
    "n": 2,
    "testid": [
     "TM-2015-W-205-55R16",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 0.5
   }
  },
  "testid": [
   "TM-2015-W-205-55R16",
   "TM-2016-W-205-55R16-friction",
   "ZaRulem-2022-W-195-65R15-friction"
  ],
  "viimane": 2022,
  "g_allikas": "test"
 },
 "t_nexen_winguard_ice": {
  "nimi": "Nexen WinGuard ice",
  "pinnad": {
   "ice": {
    "mu": 0.1708,
    "n": 1,
    "testid": [
     "ZaRulem-2019-W-195-65R15-friction"
    ],
    "kaal": 0.11
   },
   "snow": {
    "mu": 0.3543,
    "n": 1,
    "testid": [
     "ZaRulem-2019-W-195-65R15-friction"
    ],
    "kaal": 0.22
   },
   "dry": {
    "mu": 0.7988,
    "n": 1,
    "testid": [
     "ZaRulem-2019-W-195-65R15-friction"
    ],
    "kaal": 0.22
   },
   "wet": {
    "mu": 1.0101,
    "n": 1,
    "testid": [
     "ZaRulem-2019-W-195-65R15-friction"
    ],
    "kaal": 0.22
   }
  },
  "testid": [
   "ZaRulem-2019-W-195-65R15-friction"
  ],
  "viimane": 2019,
  "g_allikas": "test"
 },
 "t_nexen_winguard_ice_plus": {
  "nimi": "Nexen WinGuard Ice Plus",
  "pinnad": {
   "ice": {
    "mu": 0.1725,
    "n": 1,
    "testid": [
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 0.12
   },
   "snow": {
    "mu": 0.3574,
    "n": 1,
    "testid": [
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 0.25
   },
   "dry": {
    "mu": 0.7897,
    "n": 1,
    "testid": [
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 0.25
   },
   "wet": {
    "mu": 1.048,
    "n": 1,
    "testid": [
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 0.25
   }
  },
  "testid": [
   "ZaRulem-2020-W-205-55R16-friction"
  ],
  "viimane": 2020,
  "g_allikas": "test"
 },
 "t_nexen_winguard_ice_plus_wh43": {
  "nimi": "Nexen Winguard Ice Plus WH43",
  "pinnad": {
   "ice": {
    "mu": 0.1932,
    "n": 1,
    "testid": [
     "TM-2020-W-205-55R16-mixed"
    ],
    "kaal": 0.29
   },
   "snow": {
    "mu": 0.3788,
    "n": 1,
    "testid": [
     "TM-2020-W-205-55R16-mixed"
    ],
    "kaal": 0.23
   },
   "dry": {
    "mu": 0.8024,
    "n": 2,
    "testid": [
     "TM-2020-W-205-55R16-mixed",
     "ViBilagare-2020-W-205-60R16"
    ],
    "kaal": 0.58
   },
   "wet": {
    "mu": 1.1173,
    "n": 2,
    "testid": [
     "TM-2020-W-205-55R16-mixed",
     "ViBilagare-2020-W-205-60R16"
    ],
    "kaal": 0.58
   }
  },
  "testid": [
   "TM-2020-W-205-55R16-mixed",
   "ViBilagare-2020-W-205-60R16"
  ],
  "viimane": 2020,
  "g_allikas": "test"
 },
 "t_nexen_winguard_winspike": {
  "nimi": "Nexen WinGuard WinSpike",
  "pinnad": {
   "ice": {
    "mu": 0.1449,
    "n": 1,
    "testid": [
     "ZaRulem-2019-W-205-55R16-studded"
    ],
    "kaal": 0.13
   },
   "snow": {
    "mu": 0.3697,
    "n": 1,
    "testid": [
     "ZaRulem-2019-W-205-55R16-studded"
    ],
    "kaal": 0.21
   },
   "dry": {
    "mu": 0.8157,
    "n": 1,
    "testid": [
     "ZaRulem-2019-W-205-55R16-studded"
    ],
    "kaal": 0.26
   },
   "wet": {
    "mu": 1.164,
    "n": 1,
    "testid": [
     "ZaRulem-2019-W-205-55R16-studded"
    ],
    "kaal": 0.26
   }
  },
  "testid": [
   "ZaRulem-2019-W-205-55R16-studded"
  ],
  "viimane": 2019,
  "g_allikas": "test"
 },
 "t_nexen_winguard_winspike_3": {
  "nimi": "Nexen WinGuard WinSpike 3",
  "pinnad": {
   "ice": {
    "mu": 0.2197,
    "n": 1,
    "testid": [
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.25
   },
   "snow": {
    "mu": 0.3672,
    "n": 1,
    "testid": [
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.42
   },
   "dry": {
    "mu": 0.8352,
    "n": 1,
    "testid": [
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.51
   },
   "wet": {
    "mu": 1.3502,
    "n": 1,
    "testid": [
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.51
   }
  },
  "testid": [
   "VIBILAGARE-2025-W-STUDDED-235-60R18"
  ],
  "viimane": 2025,
  "g_allikas": "test"
 },
 "t_nexen_winguard_winspike_wh62": {
  "nimi": "Nexen Winguard winSpike WH62",
  "pinnad": {
   "ice": {
    "mu": 0.1432,
    "n": 2,
    "testid": [
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ZaRulem-2018-W-215-65R16-studded"
    ],
    "kaal": 0.3
   },
   "snow": {
    "mu": 0.3345,
    "n": 2,
    "testid": [
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ZaRulem-2018-W-215-65R16-studded"
    ],
    "kaal": 0.4
   },
   "dry": {
    "mu": 0.8337,
    "n": 2,
    "testid": [
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ZaRulem-2018-W-215-65R16-studded"
    ],
    "kaal": 0.4
   },
   "wet": {
    "mu": 1.152,
    "n": 2,
    "testid": [
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ZaRulem-2018-W-215-65R16-studded"
    ],
    "kaal": 0.4
   }
  },
  "testid": [
   "VIBILAGARE-2018-W-STUDDED-205-55R16",
   "ZaRulem-2018-W-215-65R16-studded"
  ],
  "viimane": 2018,
  "g_allikas": "test"
 },
 "t_nokian_hakkapeliitta_01": {
  "nimi": "Nokian Hakkapeliitta 01",
  "pinnad": {
   "ice": {
    "mu": 0.2518,
    "n": 2,
    "testid": [
     "AFTONBLADET-2026-W-205-55R16-PARTIAL",
     "VIBILAGARE-2026-W-STUDDED-215-65R17"
    ],
    "kaal": 1.43
   },
   "snow": {
    "mu": 0.3936,
    "n": 2,
    "testid": [
     "AFTONBLADET-2026-W-205-55R16-PARTIAL",
     "VIBILAGARE-2026-W-STUDDED-215-65R17"
    ],
    "kaal": 0.66
   },
   "dry": {
    "mu": 0.8452,
    "n": 2,
    "testid": [
     "AFTONBLADET-2026-W-205-55R16-PARTIAL",
     "VIBILAGARE-2026-W-STUDDED-215-65R17"
    ],
    "kaal": 1.86
   },
   "wet": {
    "mu": 1.2897,
    "n": 2,
    "testid": [
     "AFTONBLADET-2026-W-205-55R16-PARTIAL",
     "VIBILAGARE-2026-W-STUDDED-215-65R17"
    ],
    "kaal": 1.86
   }
  },
  "testid": [
   "AFTONBLADET-2026-W-205-55R16-PARTIAL",
   "VIBILAGARE-2026-W-STUDDED-215-65R17"
  ],
  "viimane": 2026,
  "g_allikas": "test"
 },
 "t_nokian_hakkapeliitta_10p": {
  "nimi": "Nokian Hakkapeliitta 10P",
  "pinnad": {
   "ice": {
    "mu": 0.2824,
    "n": 2,
    "testid": [
     "ZaRulem-2021-W-205-55R16-studded",
     "ZaRulem-2022-W-195-65R15-studded"
    ],
    "kaal": 0.34
   },
   "snow": {
    "mu": 0.3951,
    "n": 2,
    "testid": [
     "ZaRulem-2021-W-205-55R16-studded",
     "ZaRulem-2022-W-195-65R15-studded"
    ],
    "kaal": 0.56
   },
   "dry": {
    "mu": 0.8003,
    "n": 2,
    "testid": [
     "ZaRulem-2021-W-205-55R16-studded",
     "ZaRulem-2022-W-195-65R15-studded"
    ],
    "kaal": 0.68
   },
   "wet": {
    "mu": 1.2409,
    "n": 2,
    "testid": [
     "ZaRulem-2021-W-205-55R16-studded",
     "ZaRulem-2022-W-195-65R15-studded"
    ],
    "kaal": 0.68
   }
  },
  "testid": [
   "ZaRulem-2021-W-205-55R16-studded",
   "ZaRulem-2022-W-195-65R15-studded"
  ],
  "viimane": 2022,
  "g_allikas": "test"
 },
 "t_nokian_hakkapeliitta_10p_suv": {
  "nimi": "Nokian Hakkapeliitta 10P SUV",
  "pinnad": {
   "ice": {
    "mu": 0.2399,
    "n": 1,
    "testid": [
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 0.18
   },
   "snow": {
    "mu": 0.3811,
    "n": 1,
    "testid": [
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 0.3
   },
   "dry": {
    "mu": 0.8483,
    "n": 1,
    "testid": [
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 0.36
   },
   "wet": {
    "mu": 1.301,
    "n": 1,
    "testid": [
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 0.36
   }
  },
  "testid": [
   "ZaRulem-2022-W-235-60R18-studded"
  ],
  "viimane": 2022,
  "g_allikas": "test"
 },
 "t_nokian_hakkapeliitta_10_suv": {
  "nimi": "Nokian Hakkapeliitta 10 SUV",
  "pinnad": {
   "ice": {
    "mu": 0.3203,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18",
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.46
   },
   "snow": {
    "mu": 0.3824,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18",
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.7
   },
   "dry": {
    "mu": 0.8198,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18",
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.91
   },
   "wet": {
    "mu": 1.2646,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18",
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.91
   }
  },
  "testid": [
   "VIBILAGARE-2022-W-STUDDED-235-55R18",
   "VIBILAGARE-2025-W-STUDDED-235-60R18"
  ],
  "viimane": 2025,
  "g_allikas": "test"
 },
 "t_nokian_hakkapeliitta_8": {
  "nimi": "Nokian Hakkapeliitta 8",
  "pinnad": {
   "ice": {
    "mu": 0.2327,
    "n": 6,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-studded",
     "VIBILAGARE-2023-W-STUDDED-225-45R17",
     "ZaRulem-2015-W-175-65R14-studded",
     "ZaRulem-2016-W-195-65R15-studded"
    ],
    "kaal": 0.84
   },
   "snow": {
    "mu": 0.3773,
    "n": 6,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-studded",
     "VIBILAGARE-2023-W-STUDDED-225-45R17",
     "ZaRulem-2015-W-175-65R14-studded",
     "ZaRulem-2016-W-195-65R15-studded"
    ],
    "kaal": 0.98
   },
   "dry": {
    "mu": 0.8474,
    "n": 5,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "VIBILAGARE-2023-W-STUDDED-225-45R17",
     "ZaRulem-2015-W-175-65R14-studded",
     "ZaRulem-2016-W-195-65R15-studded"
    ],
    "kaal": 1.11
   },
   "wet": {
    "mu": 1.2504,
    "n": 5,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "VIBILAGARE-2023-W-STUDDED-225-45R17",
     "ZaRulem-2015-W-175-65R14-studded",
     "ZaRulem-2016-W-195-65R15-studded"
    ],
    "kaal": 1.11
   }
  },
  "testid": [
   "TM-2013-W-205-55R16",
   "TM-2015-W-205-55R16",
   "TM-2016-W-205-55R16-studded",
   "VIBILAGARE-2023-W-STUDDED-225-45R17",
   "ZaRulem-2015-W-175-65R14-studded",
   "ZaRulem-2016-W-195-65R15-studded"
  ],
  "viimane": 2023,
  "g_allikas": "test"
 },
 "t_nokian_hakkapeliitta_8_suv": {
  "nimi": "Nokian Hakkapeliitta 8 SUV",
  "pinnad": {
   "ice": {
    "mu": 0.2263,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-235-65R17-studded"
    ],
    "kaal": 0.08
   },
   "snow": {
    "mu": 0.3765,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-235-65R17-studded"
    ],
    "kaal": 0.16
   },
   "dry": {
    "mu": 0.8284,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-235-65R17-studded"
    ],
    "kaal": 0.16
   },
   "wet": {
    "mu": 1.2972,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-235-65R17-studded"
    ],
    "kaal": 0.16
   }
  },
  "testid": [
   "ZaRulem-2016-W-235-65R17-studded"
  ],
  "viimane": 2016,
  "g_allikas": "test"
 },
 "t_nokian_hakkapeliitta_9": {
  "nimi": "Nokian Hakkapeliitta 9",
  "pinnad": {
   "ice": {
    "mu": 0.2417,
    "n": 8,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ViBilagare-2019-W-225-50R17",
     "ZaRulem-2017-W-185-65R15-studded",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2019-W-205-55R16-studded",
     "ZaRulem-2020-W-225-45R17-studded"
    ],
    "kaal": 1.27
   },
   "snow": {
    "mu": 0.387,
    "n": 8,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ViBilagare-2019-W-225-50R17",
     "ZaRulem-2017-W-185-65R15-studded",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2019-W-205-55R16-studded",
     "ZaRulem-2020-W-225-45R17-studded"
    ],
    "kaal": 1.62
   },
   "dry": {
    "mu": 0.8129,
    "n": 8,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "VIBILAGARE-2020-W-STUDDED-205-60R16",
     "ZaRulem-2017-W-185-65R15-studded",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2019-W-205-55R16-studded",
     "ZaRulem-2020-W-225-45R17-studded"
    ],
    "kaal": 1.95
   },
   "wet": {
    "mu": 1.2599,
    "n": 9,
    "testid": [
     "AUTOCENTRE-2017-W-205-55R16-studded",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "VIBILAGARE-2020-W-STUDDED-205-60R16",
     "ViBilagare-2019-W-225-50R17",
     "ZaRulem-2017-W-185-65R15-studded",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2019-W-205-55R16-studded",
     "ZaRulem-2020-W-225-45R17-studded"
    ],
    "kaal": 2.24
   }
  },
  "testid": [
   "AUTOCENTRE-2017-W-205-55R16-studded",
   "TM-2020-W-205-55R16-mixed",
   "VIBILAGARE-2018-W-STUDDED-205-55R16",
   "VIBILAGARE-2020-W-STUDDED-205-60R16",
   "ViBilagare-2019-W-225-50R17",
   "ZaRulem-2017-W-185-65R15-studded",
   "ZaRulem-2018-W-195-65R15-studded",
   "ZaRulem-2019-W-205-55R16-studded",
   "ZaRulem-2020-W-225-45R17-studded"
  ],
  "viimane": 2020,
  "g_allikas": "test"
 },
 "t_nokian_hakkapeliitta_9_suv": {
  "nimi": "Nokian Hakkapeliitta 9 SUV",
  "pinnad": {
   "ice": {
    "mu": 0.2481,
    "n": 3,
    "testid": [
     "ZaRulem-2018-W-215-65R16-studded",
     "ZaRulem-2020-W-215-65R16-studded",
     "ZaRulem-2020-W-255-55R19-mixed"
    ],
    "kaal": 0.36
   },
   "snow": {
    "mu": 0.3846,
    "n": 3,
    "testid": [
     "ZaRulem-2018-W-215-65R16-studded",
     "ZaRulem-2020-W-215-65R16-studded",
     "ZaRulem-2020-W-255-55R19-mixed"
    ],
    "kaal": 0.69
   },
   "dry": {
    "mu": 0.8044,
    "n": 3,
    "testid": [
     "ZaRulem-2018-W-215-65R16-studded",
     "ZaRulem-2020-W-215-65R16-studded",
     "ZaRulem-2020-W-255-55R19-mixed"
    ],
    "kaal": 0.72
   },
   "wet": {
    "mu": 1.2511,
    "n": 3,
    "testid": [
     "ZaRulem-2018-W-215-65R16-studded",
     "ZaRulem-2020-W-215-65R16-studded",
     "ZaRulem-2020-W-255-55R19-mixed"
    ],
    "kaal": 0.72
   }
  },
  "testid": [
   "ZaRulem-2018-W-215-65R16-studded",
   "ZaRulem-2020-W-215-65R16-studded",
   "ZaRulem-2020-W-255-55R19-mixed"
  ],
  "viimane": 2020,
  "g_allikas": "test"
 },
 "t_nokian_hakkapeliitta_r2": {
  "nimi": "Nokian Hakkapeliitta R2",
  "pinnad": {
   "ice": {
    "mu": 0.1806,
    "n": 7,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-friction",
     "VIBILAGARE-2023-W-NORDIC-225-45R17",
     "ZaRulem-2015-W-175-65R14-friction",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction"
    ],
    "kaal": 0.91
   },
   "snow": {
    "mu": 0.3616,
    "n": 7,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-friction",
     "VIBILAGARE-2023-W-NORDIC-225-45R17",
     "ZaRulem-2015-W-175-65R14-friction",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction"
    ],
    "kaal": 1.19
   },
   "dry": {
    "mu": 0.8346,
    "n": 6,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "VIBILAGARE-2023-W-NORDIC-225-45R17",
     "ZaRulem-2015-W-175-65R14-friction",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction"
    ],
    "kaal": 1.23
   },
   "wet": {
    "mu": 1.1252,
    "n": 6,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "VIBILAGARE-2023-W-NORDIC-225-45R17",
     "ZaRulem-2015-W-175-65R14-friction",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction"
    ],
    "kaal": 1.23
   }
  },
  "testid": [
   "TM-2013-W-205-55R16",
   "TM-2015-W-205-55R16",
   "TM-2016-W-205-55R16-friction",
   "VIBILAGARE-2023-W-NORDIC-225-45R17",
   "ZaRulem-2015-W-175-65R14-friction",
   "ZaRulem-2016-W-225-45R17-friction",
   "ZaRulem-2017-W-205-55R16-friction"
  ],
  "viimane": 2023,
  "g_allikas": "test"
 },
 "t_nokian_hakkapeliitta_r3": {
  "nimi": "Nokian Hakkapeliitta R3",
  "pinnad": {
   "ice": {
    "mu": 0.1993,
    "n": 6,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 1.22
   },
   "snow": {
    "mu": 0.3832,
    "n": 5,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction"
    ],
    "kaal": 1.09
   },
   "dry": {
    "mu": 0.8505,
    "n": 7,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ViBilagare-2020-W-205-60R16",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 1.85
   },
   "wet": {
    "mu": 1.1776,
    "n": 7,
    "testid": [
     "TEKNIKENSVARLD-2021-W-205-55R16",
     "TM-2020-W-205-55R16-mixed",
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ViBilagare-2020-W-205-60R16",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 1.85
   }
  },
  "testid": [
   "TEKNIKENSVARLD-2021-W-205-55R16",
   "TM-2020-W-205-55R16-mixed",
   "VIBILAGARE-2018-W-STUDDED-205-55R16",
   "ViBilagare-2020-W-205-60R16",
   "ZaRulem-2018-W-205-55R16-friction",
   "ZaRulem-2019-W-195-65R15-friction",
   "ZaRulem-2020-W-205-55R16-friction"
  ],
  "viimane": 2021,
  "g_allikas": "test"
 },
 "t_nokian_hakkapeliitta_r3_suv": {
  "nimi": "Nokian Hakkapeliitta R3 SUV",
  "pinnad": {
   "ice": {
    "mu": 0.2154,
    "n": 2,
    "testid": [
     "ZaRulem-2020-W-255-55R19-mixed",
     "ZaRulem-2021-W-215-65R16-friction"
    ],
    "kaal": 0.29
   },
   "snow": {
    "mu": 0.382,
    "n": 2,
    "testid": [
     "ZaRulem-2020-W-255-55R19-mixed",
     "ZaRulem-2021-W-215-65R16-friction"
    ],
    "kaal": 0.51
   },
   "dry": {
    "mu": 0.8497,
    "n": 2,
    "testid": [
     "ZaRulem-2020-W-255-55R19-mixed",
     "ZaRulem-2021-W-215-65R16-friction"
    ],
    "kaal": 0.58
   },
   "wet": {
    "mu": 1.2386,
    "n": 2,
    "testid": [
     "ZaRulem-2020-W-255-55R19-mixed",
     "ZaRulem-2021-W-215-65R16-friction"
    ],
    "kaal": 0.58
   }
  },
  "testid": [
   "ZaRulem-2020-W-255-55R19-mixed",
   "ZaRulem-2021-W-215-65R16-friction"
  ],
  "viimane": 2021,
  "g_allikas": "test"
 },
 "t_nokian_hakkapeliitta_r5_suv": {
  "nimi": "Nokian Hakkapeliitta R5 SUV",
  "pinnad": {
   "ice": {
    "mu": 0.1933,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-NORDIC-235-55R18",
     "VIBILAGARE-2025-W-NORDIC-235-60R18"
    ],
    "kaal": 0.47
   },
   "snow": {
    "mu": 0.3801,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-NORDIC-235-55R18",
     "VIBILAGARE-2025-W-NORDIC-235-60R18"
    ],
    "kaal": 0.69
   },
   "dry": {
    "mu": 0.8197,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-NORDIC-235-55R18",
     "VIBILAGARE-2025-W-NORDIC-235-60R18"
    ],
    "kaal": 0.93
   },
   "wet": {
    "mu": 1.2605,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-NORDIC-235-55R18",
     "VIBILAGARE-2025-W-NORDIC-235-60R18"
    ],
    "kaal": 0.93
   }
  },
  "testid": [
   "VIBILAGARE-2022-W-NORDIC-235-55R18",
   "VIBILAGARE-2025-W-NORDIC-235-60R18"
  ],
  "viimane": 2025,
  "g_allikas": "test"
 },
 "t_nokian_nordman_5": {
  "nimi": "Nokian Nordman 5",
  "pinnad": {
   "ice": {
    "mu": 0.1784,
    "n": 3,
    "testid": [
     "TM-2015-W-205-55R16",
     "ZaRulem-2015-W-175-65R14-studded",
     "ZaRulem-2016-W-195-65R15-studded"
    ],
    "kaal": 0.29
   },
   "snow": {
    "mu": 0.3747,
    "n": 3,
    "testid": [
     "TM-2015-W-205-55R16",
     "ZaRulem-2015-W-175-65R14-studded",
     "ZaRulem-2016-W-195-65R15-studded"
    ],
    "kaal": 0.44
   },
   "dry": {
    "mu": 0.8114,
    "n": 3,
    "testid": [
     "TM-2015-W-205-55R16",
     "ZaRulem-2015-W-175-65R14-studded",
     "ZaRulem-2016-W-195-65R15-studded"
    ],
    "kaal": 0.44
   },
   "wet": {
    "mu": 1.22,
    "n": 3,
    "testid": [
     "TM-2015-W-205-55R16",
     "ZaRulem-2015-W-175-65R14-studded",
     "ZaRulem-2016-W-195-65R15-studded"
    ],
    "kaal": 0.44
   }
  },
  "testid": [
   "TM-2015-W-205-55R16",
   "ZaRulem-2015-W-175-65R14-studded",
   "ZaRulem-2016-W-195-65R15-studded"
  ],
  "viimane": 2016,
  "g_allikas": "test"
 },
 "t_nokian_nordman_7": {
  "nimi": "Nokian Nordman 7",
  "pinnad": {
   "ice": {
    "mu": 0.2185,
    "n": 4,
    "testid": [
     "ZaRulem-2017-W-185-65R15-studded",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2019-W-205-55R16-studded",
     "ZaRulem-2020-W-225-45R17-studded"
    ],
    "kaal": 0.47
   },
   "snow": {
    "mu": 0.3799,
    "n": 4,
    "testid": [
     "ZaRulem-2017-W-185-65R15-studded",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2019-W-205-55R16-studded",
     "ZaRulem-2020-W-225-45R17-studded"
    ],
    "kaal": 0.82
   },
   "dry": {
    "mu": 0.7891,
    "n": 5,
    "testid": [
     "VIBILAGARE-2020-W-STUDDED-205-60R16",
     "ZaRulem-2017-W-185-65R15-studded",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2019-W-205-55R16-studded",
     "ZaRulem-2020-W-225-45R17-studded"
    ],
    "kaal": 1.29
   },
   "wet": {
    "mu": 1.1731,
    "n": 5,
    "testid": [
     "VIBILAGARE-2020-W-STUDDED-205-60R16",
     "ZaRulem-2017-W-185-65R15-studded",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2019-W-205-55R16-studded",
     "ZaRulem-2020-W-225-45R17-studded"
    ],
    "kaal": 1.29
   }
  },
  "testid": [
   "VIBILAGARE-2020-W-STUDDED-205-60R16",
   "ZaRulem-2017-W-185-65R15-studded",
   "ZaRulem-2018-W-195-65R15-studded",
   "ZaRulem-2019-W-205-55R16-studded",
   "ZaRulem-2020-W-225-45R17-studded"
  ],
  "viimane": 2020,
  "g_allikas": "test"
 },
 "t_nokian_nordman_7_suv": {
  "nimi": "Nokian Nordman 7 SUV",
  "pinnad": {
   "ice": {
    "mu": 0.2233,
    "n": 2,
    "testid": [
     "ZaRulem-2018-W-215-65R16-studded",
     "ZaRulem-2020-W-215-65R16-studded"
    ],
    "kaal": 0.23
   },
   "snow": {
    "mu": 0.3873,
    "n": 2,
    "testid": [
     "ZaRulem-2018-W-215-65R16-studded",
     "ZaRulem-2020-W-215-65R16-studded"
    ],
    "kaal": 0.44
   },
   "dry": {
    "mu": 0.8053,
    "n": 2,
    "testid": [
     "ZaRulem-2018-W-215-65R16-studded",
     "ZaRulem-2020-W-215-65R16-studded"
    ],
    "kaal": 0.47
   },
   "wet": {
    "mu": 1.2392,
    "n": 2,
    "testid": [
     "ZaRulem-2018-W-215-65R16-studded",
     "ZaRulem-2020-W-215-65R16-studded"
    ],
    "kaal": 0.47
   }
  },
  "testid": [
   "ZaRulem-2018-W-215-65R16-studded",
   "ZaRulem-2020-W-215-65R16-studded"
  ],
  "viimane": 2020,
  "g_allikas": "test"
 },
 "t_nokian_nordman_8": {
  "nimi": "Nokian Nordman 8",
  "pinnad": {
   "ice": {
    "mu": 0.2562,
    "n": 3,
    "testid": [
     "MOOTTORI-2021-W-STUDDED-205-55R16",
     "ZaRulem-2021-W-205-55R16-studded",
     "ZaRulem-2022-W-195-65R15-studded"
    ],
    "kaal": 0.78
   },
   "snow": {
    "mu": 0.3875,
    "n": 3,
    "testid": [
     "MOOTTORI-2021-W-STUDDED-205-55R16",
     "ZaRulem-2021-W-205-55R16-studded",
     "ZaRulem-2022-W-195-65R15-studded"
    ],
    "kaal": 0.78
   },
   "dry": {
    "mu": 0.7978,
    "n": 3,
    "testid": [
     "MOOTTORI-2021-W-STUDDED-205-55R16",
     "ZaRulem-2021-W-205-55R16-studded",
     "ZaRulem-2022-W-195-65R15-studded"
    ],
    "kaal": 1.12
   },
   "wet": {
    "mu": 1.1918,
    "n": 3,
    "testid": [
     "MOOTTORI-2021-W-STUDDED-205-55R16",
     "ZaRulem-2021-W-205-55R16-studded",
     "ZaRulem-2022-W-195-65R15-studded"
    ],
    "kaal": 1.12
   }
  },
  "testid": [
   "MOOTTORI-2021-W-STUDDED-205-55R16",
   "ZaRulem-2021-W-205-55R16-studded",
   "ZaRulem-2022-W-195-65R15-studded"
  ],
  "viimane": 2022,
  "g_allikas": "test"
 },
 "t_nokian_nordman_8_suv": {
  "nimi": "Nokian Nordman 8 SUV",
  "pinnad": {
   "ice": {
    "mu": 0.2581,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18",
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 0.38
   },
   "snow": {
    "mu": 0.3811,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18",
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 0.58
   },
   "dry": {
    "mu": 0.8165,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18",
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 0.76
   },
   "wet": {
    "mu": 1.2355,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18",
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 0.76
   }
  },
  "testid": [
   "VIBILAGARE-2022-W-STUDDED-235-55R18",
   "ZaRulem-2022-W-235-60R18-studded"
  ],
  "viimane": 2022,
  "g_allikas": "test"
 },
 "t_nokian_nordman_north_9": {
  "nimi": "Nokian Nordman North 9",
  "pinnad": {
   "ice": {
    "mu": 0.2513,
    "n": 1,
    "testid": [
     "VIBILAGARE-2024-W-STUDDED-225-45R17"
    ],
    "kaal": 0.37
   },
   "snow": {
    "mu": 0.3932,
    "n": 1,
    "testid": [
     "VIBILAGARE-2024-W-STUDDED-225-45R17"
    ],
    "kaal": 0.26
   },
   "dry": {
    "mu": 0.8051,
    "n": 1,
    "testid": [
     "VIBILAGARE-2024-W-STUDDED-225-45R17"
    ],
    "kaal": 0.74
   },
   "wet": {
    "mu": 1.2526,
    "n": 1,
    "testid": [
     "VIBILAGARE-2024-W-STUDDED-225-45R17"
    ],
    "kaal": 0.74
   }
  },
  "testid": [
   "VIBILAGARE-2024-W-STUDDED-225-45R17"
  ],
  "viimane": 2024,
  "g_allikas": "test"
 },
 "t_nokian_nordman_north_9_suv": {
  "nimi": "Nokian Nordman North 9 SUV",
  "pinnad": {
   "ice": {
    "mu": 0.2425,
    "n": 1,
    "testid": [
     "VIBILAGARE-2026-W-STUDDED-215-65R17"
    ],
    "kaal": 0.43
   },
   "snow": {
    "mu": 0.3961,
    "n": 1,
    "testid": [
     "VIBILAGARE-2026-W-STUDDED-215-65R17"
    ],
    "kaal": 0.36
   },
   "dry": {
    "mu": 0.8012,
    "n": 1,
    "testid": [
     "VIBILAGARE-2026-W-STUDDED-215-65R17"
    ],
    "kaal": 0.86
   },
   "wet": {
    "mu": 1.2239,
    "n": 1,
    "testid": [
     "VIBILAGARE-2026-W-STUDDED-215-65R17"
    ],
    "kaal": 0.86
   }
  },
  "testid": [
   "VIBILAGARE-2026-W-STUDDED-215-65R17"
  ],
  "viimane": 2026,
  "g_allikas": "test"
 },
 "t_nokian_nordman_north_rs3_suv": {
  "nimi": "Nokian Nordman North RS3 SUV",
  "pinnad": {
   "ice": {
    "mu": 0.1966,
    "n": 1,
    "testid": [
     "VIBILAGARE-2025-W-NORDIC-235-60R18"
    ],
    "kaal": 0.29
   },
   "snow": {
    "mu": 0.3739,
    "n": 1,
    "testid": [
     "VIBILAGARE-2025-W-NORDIC-235-60R18"
    ],
    "kaal": 0.39
   },
   "dry": {
    "mu": 0.8317,
    "n": 1,
    "testid": [
     "VIBILAGARE-2025-W-NORDIC-235-60R18"
    ],
    "kaal": 0.57
   },
   "wet": {
    "mu": 1.0996,
    "n": 1,
    "testid": [
     "VIBILAGARE-2025-W-NORDIC-235-60R18"
    ],
    "kaal": 0.57
   }
  },
  "testid": [
   "VIBILAGARE-2025-W-NORDIC-235-60R18"
  ],
  "viimane": 2025,
  "g_allikas": "test"
 },
 "t_nokian_nordman_rs": {
  "nimi": "Nokian Nordman RS",
  "pinnad": {
   "ice": {
    "mu": 0.147,
    "n": 2,
    "testid": [
     "TM-2015-W-205-55R16",
     "ZaRulem-2015-W-175-65R14-friction"
    ],
    "kaal": 0.21
   },
   "snow": {
    "mu": 0.3499,
    "n": 2,
    "testid": [
     "TM-2015-W-205-55R16",
     "ZaRulem-2015-W-175-65R14-friction"
    ],
    "kaal": 0.28
   },
   "dry": {
    "mu": 0.7813,
    "n": 2,
    "testid": [
     "TM-2015-W-205-55R16",
     "ZaRulem-2015-W-175-65R14-friction"
    ],
    "kaal": 0.28
   },
   "wet": {
    "mu": 0.9718,
    "n": 2,
    "testid": [
     "TM-2015-W-205-55R16",
     "ZaRulem-2015-W-175-65R14-friction"
    ],
    "kaal": 0.28
   }
  },
  "testid": [
   "TM-2015-W-205-55R16",
   "ZaRulem-2015-W-175-65R14-friction"
  ],
  "viimane": 2015,
  "g_allikas": "test"
 },
 "t_nokian_nordman_rs_2": {
  "nimi": "Nokian Nordman RS 2",
  "pinnad": {
   "ice": {
    "mu": 0.1896,
    "n": 5,
    "testid": [
     "ZaRulem-2017-W-205-55R16-friction",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 0.6
   },
   "snow": {
    "mu": 0.3627,
    "n": 5,
    "testid": [
     "ZaRulem-2017-W-205-55R16-friction",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 1.14
   },
   "dry": {
    "mu": 0.8317,
    "n": 5,
    "testid": [
     "ZaRulem-2017-W-205-55R16-friction",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 1.21
   },
   "wet": {
    "mu": 1.0879,
    "n": 5,
    "testid": [
     "ZaRulem-2017-W-205-55R16-friction",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 1.21
   }
  },
  "testid": [
   "ZaRulem-2017-W-205-55R16-friction",
   "ZaRulem-2018-W-205-55R16-friction",
   "ZaRulem-2019-W-195-65R15-friction",
   "ZaRulem-2020-W-205-55R16-friction",
   "ZaRulem-2022-W-195-65R15-friction"
  ],
  "viimane": 2022,
  "g_allikas": "test"
 },
 "t_nokian_nordman_rs2_suv": {
  "nimi": "Nokian Nordman RS2 SUV",
  "pinnad": {
   "ice": {
    "mu": 0.2086,
    "n": 1,
    "testid": [
     "ZaRulem-2021-W-215-65R16-friction"
    ],
    "kaal": 0.16
   },
   "snow": {
    "mu": 0.377,
    "n": 1,
    "testid": [
     "ZaRulem-2021-W-215-65R16-friction"
    ],
    "kaal": 0.26
   },
   "dry": {
    "mu": 0.8148,
    "n": 1,
    "testid": [
     "ZaRulem-2021-W-215-65R16-friction"
    ],
    "kaal": 0.33
   },
   "wet": {
    "mu": 1.1502,
    "n": 1,
    "testid": [
     "ZaRulem-2021-W-215-65R16-friction"
    ],
    "kaal": 0.33
   }
  },
  "testid": [
   "ZaRulem-2021-W-215-65R16-friction"
  ],
  "viimane": 2021,
  "g_allikas": "test"
 },
 "t_pirelli_ice_friction": {
  "nimi": "Pirelli Ice Friction",
  "pinnad": {
   "ice": {
    "mu": 0.195,
    "n": 1,
    "testid": [
     "VIBILAGARE-2025-W-NORDIC-235-60R18"
    ],
    "kaal": 0.29
   },
   "snow": {
    "mu": 0.3811,
    "n": 1,
    "testid": [
     "VIBILAGARE-2025-W-NORDIC-235-60R18"
    ],
    "kaal": 0.39
   },
   "dry": {
    "mu": 0.8571,
    "n": 1,
    "testid": [
     "VIBILAGARE-2025-W-NORDIC-235-60R18"
    ],
    "kaal": 0.57
   },
   "wet": {
    "mu": 1.1996,
    "n": 1,
    "testid": [
     "VIBILAGARE-2025-W-NORDIC-235-60R18"
    ],
    "kaal": 0.57
   }
  },
  "testid": [
   "VIBILAGARE-2025-W-NORDIC-235-60R18"
  ],
  "viimane": 2025,
  "g_allikas": "test"
 },
 "t_pirelli_winter_icecontrol": {
  "nimi": "Pirelli Winter IceControl",
  "pinnad": {
   "ice": {
    "mu": 0.176,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   },
   "snow": {
    "mu": 0.355,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   },
   "dry": {
    "mu": 0.8449,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   },
   "wet": {
    "mu": 1.1426,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   }
  },
  "testid": [
   "TM-2013-W-205-55R16"
  ],
  "viimane": 2013,
  "g_allikas": "test"
 },
 "t_pirelli_ice_zero": {
  "nimi": "Pirelli Ice Zero",
  "pinnad": {
   "ice": {
    "mu": 0.2163,
    "n": 5,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-studded",
     "ZaRulem-2016-W-235-65R17-studded",
     "ZaRulem-2018-W-195-65R15-studded"
    ],
    "kaal": 0.59
   },
   "snow": {
    "mu": 0.3696,
    "n": 5,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-studded",
     "ZaRulem-2016-W-235-65R17-studded",
     "ZaRulem-2018-W-195-65R15-studded"
    ],
    "kaal": 0.77
   },
   "dry": {
    "mu": 0.8234,
    "n": 4,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "ZaRulem-2016-W-235-65R17-studded",
     "ZaRulem-2018-W-195-65R15-studded"
    ],
    "kaal": 0.61
   },
   "wet": {
    "mu": 1.2657,
    "n": 4,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2015-W-205-55R16",
     "ZaRulem-2016-W-235-65R17-studded",
     "ZaRulem-2018-W-195-65R15-studded"
    ],
    "kaal": 0.61
   }
  },
  "testid": [
   "TM-2013-W-205-55R16",
   "TM-2015-W-205-55R16",
   "TM-2016-W-205-55R16-studded",
   "ZaRulem-2016-W-235-65R17-studded",
   "ZaRulem-2018-W-195-65R15-studded"
  ],
  "viimane": 2018,
  "g_allikas": "test"
 },
 "t_pirelli_ice_zero_asimmetrico": {
  "nimi": "Pirelli Ice Zero Asimmetrico",
  "pinnad": {
   "ice": {
    "mu": 0.1916,
    "n": 1,
    "testid": [
     "VIBILAGARE-2023-W-NORDIC-225-45R17"
    ],
    "kaal": 0.25
   },
   "snow": {
    "mu": 0.3752,
    "n": 1,
    "testid": [
     "VIBILAGARE-2023-W-NORDIC-225-45R17"
    ],
    "kaal": 0.29
   },
   "dry": {
    "mu": 0.825,
    "n": 1,
    "testid": [
     "VIBILAGARE-2023-W-NORDIC-225-45R17"
    ],
    "kaal": 0.51
   },
   "wet": {
    "mu": 1.0613,
    "n": 1,
    "testid": [
     "VIBILAGARE-2023-W-NORDIC-225-45R17"
    ],
    "kaal": 0.51
   }
  },
  "testid": [
   "VIBILAGARE-2023-W-NORDIC-225-45R17"
  ],
  "viimane": 2023,
  "g_allikas": "test"
 },
 "t_pirelli_ice_zero_fr": {
  "nimi": "Pirelli Ice Zero FR",
  "pinnad": {
   "ice": {
    "mu": 0.1948,
    "n": 11,
    "testid": [
     "MOOTTORI-2018-W-NORDIC-205-55R16-PARTIAL",
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-friction",
     "TM-2020-W-205-55R16-mixed",
     "TUULILASI-2018-W-NORDIC-205-55R16-PARTIAL",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 1.48
   },
   "snow": {
    "mu": 0.3697,
    "n": 8,
    "testid": [
     "TM-2015-W-205-55R16",
     "TM-2016-W-205-55R16-friction",
     "TM-2020-W-205-55R16-mixed",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 1.6
   },
   "dry": {
    "mu": 0.8483,
    "n": 9,
    "testid": [
     "TM-2015-W-205-55R16",
     "TM-2020-W-205-55R16-mixed",
     "ViBilagare-2020-W-205-60R16",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 2.08
   },
   "wet": {
    "mu": 1.1825,
    "n": 9,
    "testid": [
     "TM-2015-W-205-55R16",
     "TM-2020-W-205-55R16-mixed",
     "ViBilagare-2020-W-205-60R16",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction",
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2022-W-195-65R15-friction"
    ],
    "kaal": 2.08
   }
  },
  "testid": [
   "MOOTTORI-2018-W-NORDIC-205-55R16-PARTIAL",
   "TM-2015-W-205-55R16",
   "TM-2016-W-205-55R16-friction",
   "TM-2020-W-205-55R16-mixed",
   "TUULILASI-2018-W-NORDIC-205-55R16-PARTIAL",
   "ViBilagare-2020-W-205-60R16",
   "ZaRulem-2016-W-225-45R17-friction",
   "ZaRulem-2017-W-205-55R16-friction",
   "ZaRulem-2018-W-205-55R16-friction",
   "ZaRulem-2019-W-195-65R15-friction",
   "ZaRulem-2020-W-205-55R16-friction",
   "ZaRulem-2022-W-195-65R15-friction"
  ],
  "viimane": 2022,
  "g_allikas": "test"
 },
 "t_pirelli_scorpion_icezero_2": {
  "nimi": "Pirelli Scorpion IceZero 2",
  "pinnad": {
   "ice": {
    "mu": 0.2072,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18",
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.46
   },
   "snow": {
    "mu": 0.3879,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18",
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.7
   },
   "dry": {
    "mu": 0.8262,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18",
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.91
   },
   "wet": {
    "mu": 1.3378,
    "n": 2,
    "testid": [
     "VIBILAGARE-2022-W-STUDDED-235-55R18",
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.91
   }
  },
  "testid": [
   "VIBILAGARE-2022-W-STUDDED-235-55R18",
   "VIBILAGARE-2025-W-STUDDED-235-60R18"
  ],
  "viimane": 2025,
  "g_allikas": "test"
 },
 "t_radar_dimax_ice": {
  "nimi": "Radar Dimax Ice",
  "pinnad": {
   "ice": {
    "mu": 0.1483,
    "n": 1,
    "testid": [
     "VIBILAGARE-2024-W-NORDIC-225-45R17"
    ],
    "kaal": 0.33
   },
   "snow": {
    "mu": 0.367,
    "n": 1,
    "testid": [
     "VIBILAGARE-2024-W-NORDIC-225-45R17"
    ],
    "kaal": 0.29
   },
   "dry": {
    "mu": 0.8056,
    "n": 1,
    "testid": [
     "VIBILAGARE-2024-W-NORDIC-225-45R17"
    ],
    "kaal": 0.66
   },
   "wet": {
    "mu": 1.0783,
    "n": 1,
    "testid": [
     "VIBILAGARE-2024-W-NORDIC-225-45R17"
    ],
    "kaal": 0.66
   }
  },
  "testid": [
   "VIBILAGARE-2024-W-NORDIC-225-45R17"
  ],
  "viimane": 2024,
  "g_allikas": "test"
 },
 "t_sailun_ice_blazer_wsl2": {
  "nimi": "Sailun Ice Blazer WSL2",
  "pinnad": {
   "ice": {
    "mu": 0.1674,
    "n": 1,
    "testid": [
     "ZaRulem-2019-W-195-65R15-friction"
    ],
    "kaal": 0.11
   },
   "snow": {
    "mu": 0.3443,
    "n": 1,
    "testid": [
     "ZaRulem-2019-W-195-65R15-friction"
    ],
    "kaal": 0.22
   },
   "dry": {
    "mu": 0.8013,
    "n": 1,
    "testid": [
     "ZaRulem-2019-W-195-65R15-friction"
    ],
    "kaal": 0.22
   },
   "wet": {
    "mu": 1.1584,
    "n": 1,
    "testid": [
     "ZaRulem-2019-W-195-65R15-friction"
    ],
    "kaal": 0.22
   }
  },
  "testid": [
   "ZaRulem-2019-W-195-65R15-friction"
  ],
  "viimane": 2019,
  "g_allikas": "test"
 },
 "t_sailun_ice_blazer_wst3": {
  "nimi": "Sailun Ice Blazer WST3",
  "pinnad": {
   "ice": {
    "mu": 0.1691,
    "n": 4,
    "testid": [
     "ViBilagare-2019-W-225-50R17",
     "ZaRulem-2019-W-205-55R16-studded",
     "ZaRulem-2020-W-215-65R16-studded",
     "ZaRulem-2020-W-225-45R17-studded"
    ],
    "kaal": 0.56
   },
   "snow": {
    "mu": 0.3669,
    "n": 4,
    "testid": [
     "ViBilagare-2019-W-225-50R17",
     "ZaRulem-2019-W-205-55R16-studded",
     "ZaRulem-2020-W-215-65R16-studded",
     "ZaRulem-2020-W-225-45R17-studded"
    ],
    "kaal": 0.88
   },
   "dry": {
    "mu": 0.7906,
    "n": 3,
    "testid": [
     "ZaRulem-2019-W-205-55R16-studded",
     "ZaRulem-2020-W-215-65R16-studded",
     "ZaRulem-2020-W-225-45R17-studded"
    ],
    "kaal": 0.82
   },
   "wet": {
    "mu": 1.2035,
    "n": 4,
    "testid": [
     "ViBilagare-2019-W-225-50R17",
     "ZaRulem-2019-W-205-55R16-studded",
     "ZaRulem-2020-W-215-65R16-studded",
     "ZaRulem-2020-W-225-45R17-studded"
    ],
    "kaal": 1.11
   }
  },
  "testid": [
   "ViBilagare-2019-W-225-50R17",
   "ZaRulem-2019-W-205-55R16-studded",
   "ZaRulem-2020-W-215-65R16-studded",
   "ZaRulem-2020-W-225-45R17-studded"
  ],
  "viimane": 2020,
  "g_allikas": "test"
 },
 "t_sailun_winterpro_sw61": {
  "nimi": "Sailun Winterpro SW61",
  "pinnad": {
   "ice": {
    "mu": 0.1799,
    "n": 1,
    "testid": [
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 0.12
   },
   "snow": {
    "mu": 0.3444,
    "n": 1,
    "testid": [
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 0.25
   },
   "dry": {
    "mu": 0.8543,
    "n": 1,
    "testid": [
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 0.25
   },
   "wet": {
    "mu": 1.2729,
    "n": 1,
    "testid": [
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 0.25
   }
  },
  "testid": [
   "ZaRulem-2020-W-205-55R16-friction"
  ],
  "viimane": 2020,
  "g_allikas": "test"
 },
 "t_sava_eskimo_ice": {
  "nimi": "Sava Eskimo Ice",
  "pinnad": {
   "ice": {
    "mu": 0.2105,
    "n": 2,
    "testid": [
     "TM-2016-W-205-55R16-friction",
     "TM-2020-W-205-55R16-mixed"
    ],
    "kaal": 0.46
   },
   "snow": {
    "mu": 0.3773,
    "n": 2,
    "testid": [
     "TM-2016-W-205-55R16-friction",
     "TM-2020-W-205-55R16-mixed"
    ],
    "kaal": 0.41
   },
   "dry": {
    "mu": 0.7824,
    "n": 1,
    "testid": [
     "TM-2020-W-205-55R16-mixed"
    ],
    "kaal": 0.29
   },
   "wet": {
    "mu": 1.1318,
    "n": 1,
    "testid": [
     "TM-2020-W-205-55R16-mixed"
    ],
    "kaal": 0.29
   }
  },
  "testid": [
   "TM-2016-W-205-55R16-friction",
   "TM-2020-W-205-55R16-mixed"
  ],
  "viimane": 2020,
  "g_allikas": "test"
 },
 "t_sava_eskimo_stud": {
  "nimi": "Sava Eskimo Stud",
  "pinnad": {
   "ice": {
    "mu": 0.186,
    "n": 3,
    "testid": [
     "MOOTTORI-2021-W-STUDDED-205-55R16",
     "TM-2015-W-205-55R16",
     "ZaRulem-2015-W-175-65R14-studded"
    ],
    "kaal": 0.65
   },
   "snow": {
    "mu": 0.3752,
    "n": 3,
    "testid": [
     "MOOTTORI-2021-W-STUDDED-205-55R16",
     "TM-2015-W-205-55R16",
     "ZaRulem-2015-W-175-65R14-studded"
    ],
    "kaal": 0.5
   },
   "dry": {
    "mu": 0.846,
    "n": 3,
    "testid": [
     "MOOTTORI-2021-W-STUDDED-205-55R16",
     "TM-2015-W-205-55R16",
     "ZaRulem-2015-W-175-65R14-studded"
    ],
    "kaal": 0.72
   },
   "wet": {
    "mu": 1.272,
    "n": 3,
    "testid": [
     "MOOTTORI-2021-W-STUDDED-205-55R16",
     "TM-2015-W-205-55R16",
     "ZaRulem-2015-W-175-65R14-studded"
    ],
    "kaal": 0.72
   }
  },
  "testid": [
   "MOOTTORI-2021-W-STUDDED-205-55R16",
   "TM-2015-W-205-55R16",
   "ZaRulem-2015-W-175-65R14-studded"
  ],
  "viimane": 2021,
  "g_allikas": "test"
 },
 "t_tigar_ice": {
  "nimi": "Tigar Ice",
  "pinnad": {
   "ice": {
    "mu": 0.1894,
    "n": 1,
    "testid": [
     "ZaRulem-2021-W-205-55R16-studded"
    ],
    "kaal": 0.16
   },
   "snow": {
    "mu": 0.3545,
    "n": 1,
    "testid": [
     "ZaRulem-2021-W-205-55R16-studded"
    ],
    "kaal": 0.26
   },
   "dry": {
    "mu": 0.8321,
    "n": 1,
    "testid": [
     "ZaRulem-2021-W-205-55R16-studded"
    ],
    "kaal": 0.32
   },
   "wet": {
    "mu": 1.3845,
    "n": 1,
    "testid": [
     "ZaRulem-2021-W-205-55R16-studded"
    ],
    "kaal": 0.32
   }
  },
  "testid": [
   "ZaRulem-2021-W-205-55R16-studded"
  ],
  "viimane": 2021,
  "g_allikas": "test"
 },
 "t_tigar_suv_ice": {
  "nimi": "Tigar SUV Ice",
  "pinnad": {
   "ice": {
    "mu": 0.1709,
    "n": 1,
    "testid": [
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 0.18
   },
   "snow": {
    "mu": 0.3624,
    "n": 1,
    "testid": [
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 0.3
   },
   "dry": {
    "mu": 0.8983,
    "n": 1,
    "testid": [
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 0.36
   },
   "wet": {
    "mu": 1.4063,
    "n": 1,
    "testid": [
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 0.36
   }
  },
  "testid": [
   "ZaRulem-2022-W-235-60R18-studded"
  ],
  "viimane": 2022,
  "g_allikas": "test"
 },
 "t_toyo_observe_g3_ice": {
  "nimi": "Toyo Observe G3-Ice",
  "pinnad": {
   "ice": {
    "mu": 0.1811,
    "n": 6,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2016-W-205-55R16-studded",
     "ZaRulem-2015-W-175-65R14-studded",
     "ZaRulem-2016-W-195-65R15-studded",
     "ZaRulem-2016-W-235-65R17-studded",
     "ZaRulem-2017-W-185-65R15-studded"
    ],
    "kaal": 0.58
   },
   "snow": {
    "mu": 0.3672,
    "n": 6,
    "testid": [
     "TM-2013-W-205-55R16",
     "TM-2016-W-205-55R16-studded",
     "ZaRulem-2015-W-175-65R14-studded",
     "ZaRulem-2016-W-195-65R15-studded",
     "ZaRulem-2016-W-235-65R17-studded",
     "ZaRulem-2017-W-185-65R15-studded"
    ],
    "kaal": 0.9
   },
   "dry": {
    "mu": 0.8064,
    "n": 5,
    "testid": [
     "TM-2013-W-205-55R16",
     "ZaRulem-2015-W-175-65R14-studded",
     "ZaRulem-2016-W-195-65R15-studded",
     "ZaRulem-2016-W-235-65R17-studded",
     "ZaRulem-2017-W-185-65R15-studded"
    ],
    "kaal": 0.74
   },
   "wet": {
    "mu": 1.2071,
    "n": 5,
    "testid": [
     "TM-2013-W-205-55R16",
     "ZaRulem-2015-W-175-65R14-studded",
     "ZaRulem-2016-W-195-65R15-studded",
     "ZaRulem-2016-W-235-65R17-studded",
     "ZaRulem-2017-W-185-65R15-studded"
    ],
    "kaal": 0.74
   }
  },
  "testid": [
   "TM-2013-W-205-55R16",
   "TM-2016-W-205-55R16-studded",
   "ZaRulem-2015-W-175-65R14-studded",
   "ZaRulem-2016-W-195-65R15-studded",
   "ZaRulem-2016-W-235-65R17-studded",
   "ZaRulem-2017-W-185-65R15-studded"
  ],
  "viimane": 2017,
  "g_allikas": "test"
 },
 "t_toyo_observe_gsi_5": {
  "nimi": "Toyo Observe GSi-5",
  "pinnad": {
   "ice": {
    "mu": 0.1903,
    "n": 4,
    "testid": [
     "ZaRulem-2015-W-175-65R14-friction",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction",
     "ZaRulem-2018-W-205-55R16-friction"
    ],
    "kaal": 0.34
   },
   "snow": {
    "mu": 0.365,
    "n": 4,
    "testid": [
     "ZaRulem-2015-W-175-65R14-friction",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction",
     "ZaRulem-2018-W-205-55R16-friction"
    ],
    "kaal": 0.67
   },
   "dry": {
    "mu": 0.781,
    "n": 4,
    "testid": [
     "ZaRulem-2015-W-175-65R14-friction",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction",
     "ZaRulem-2018-W-205-55R16-friction"
    ],
    "kaal": 0.67
   },
   "wet": {
    "mu": 0.9803,
    "n": 4,
    "testid": [
     "ZaRulem-2015-W-175-65R14-friction",
     "ZaRulem-2016-W-225-45R17-friction",
     "ZaRulem-2017-W-205-55R16-friction",
     "ZaRulem-2018-W-205-55R16-friction"
    ],
    "kaal": 0.67
   }
  },
  "testid": [
   "ZaRulem-2015-W-175-65R14-friction",
   "ZaRulem-2016-W-225-45R17-friction",
   "ZaRulem-2017-W-205-55R16-friction",
   "ZaRulem-2018-W-205-55R16-friction"
  ],
  "viimane": 2018,
  "g_allikas": "test"
 },
 "t_toyo_observe_gsi_6": {
  "nimi": "Toyo Observe GSi-6",
  "pinnad": {
   "ice": {
    "mu": 0.1983,
    "n": 1,
    "testid": [
     "ZaRulem-2019-W-195-65R15-friction"
    ],
    "kaal": 0.11
   },
   "snow": {
    "mu": 0.367,
    "n": 1,
    "testid": [
     "ZaRulem-2019-W-195-65R15-friction"
    ],
    "kaal": 0.22
   },
   "dry": {
    "mu": 0.8347,
    "n": 1,
    "testid": [
     "ZaRulem-2019-W-195-65R15-friction"
    ],
    "kaal": 0.22
   },
   "wet": {
    "mu": 1.0986,
    "n": 1,
    "testid": [
     "ZaRulem-2019-W-195-65R15-friction"
    ],
    "kaal": 0.22
   }
  },
  "testid": [
   "ZaRulem-2019-W-195-65R15-friction"
  ],
  "viimane": 2019,
  "g_allikas": "test"
 },
 "t_toyo_observe_gsi_6_hp": {
  "nimi": "Toyo Observe GSi-6 HP",
  "pinnad": {
   "ice": {
    "mu": 0.19,
    "n": 2,
    "testid": [
     "TM-2020-W-205-55R16-mixed",
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 0.41
   },
   "snow": {
    "mu": 0.369,
    "n": 2,
    "testid": [
     "TM-2020-W-205-55R16-mixed",
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 0.48
   },
   "dry": {
    "mu": 0.8428,
    "n": 2,
    "testid": [
     "TM-2020-W-205-55R16-mixed",
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 0.54
   },
   "wet": {
    "mu": 1.1936,
    "n": 2,
    "testid": [
     "TM-2020-W-205-55R16-mixed",
     "ZaRulem-2020-W-205-55R16-friction"
    ],
    "kaal": 0.54
   }
  },
  "testid": [
   "TM-2020-W-205-55R16-mixed",
   "ZaRulem-2020-W-205-55R16-friction"
  ],
  "viimane": 2020,
  "g_allikas": "test"
 },
 "t_toyo_observe_ice_freezer": {
  "nimi": "Toyo Observe Ice-Freezer",
  "pinnad": {
   "ice": {
    "mu": 0.1655,
    "n": 2,
    "testid": [
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2019-W-205-55R16-studded"
    ],
    "kaal": 0.23
   },
   "snow": {
    "mu": 0.3627,
    "n": 2,
    "testid": [
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2019-W-205-55R16-studded"
    ],
    "kaal": 0.4
   },
   "dry": {
    "mu": 0.8134,
    "n": 3,
    "testid": [
     "VIBILAGARE-2020-W-STUDDED-205-60R16",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2019-W-205-55R16-studded"
    ],
    "kaal": 0.82
   },
   "wet": {
    "mu": 1.2024,
    "n": 3,
    "testid": [
     "VIBILAGARE-2020-W-STUDDED-205-60R16",
     "ZaRulem-2018-W-195-65R15-studded",
     "ZaRulem-2019-W-205-55R16-studded"
    ],
    "kaal": 0.82
   }
  },
  "testid": [
   "VIBILAGARE-2020-W-STUDDED-205-60R16",
   "ZaRulem-2018-W-195-65R15-studded",
   "ZaRulem-2019-W-205-55R16-studded"
  ],
  "viimane": 2020,
  "g_allikas": "test"
 },
 "t_toyo_observe_ice_freezer_suv": {
  "nimi": "Toyo Observe Ice-Freezer SUV",
  "pinnad": {
   "ice": {
    "mu": 0.1851,
    "n": 1,
    "testid": [
     "ZaRulem-2020-W-215-65R16-studded"
    ],
    "kaal": 0.13
   },
   "snow": {
    "mu": 0.3768,
    "n": 1,
    "testid": [
     "ZaRulem-2020-W-215-65R16-studded"
    ],
    "kaal": 0.24
   },
   "dry": {
    "mu": 0.8029,
    "n": 1,
    "testid": [
     "ZaRulem-2020-W-215-65R16-studded"
    ],
    "kaal": 0.27
   },
   "wet": {
    "mu": 1.1772,
    "n": 1,
    "testid": [
     "ZaRulem-2020-W-215-65R16-studded"
    ],
    "kaal": 0.27
   }
  },
  "testid": [
   "ZaRulem-2020-W-215-65R16-studded"
  ],
  "viimane": 2020,
  "g_allikas": "test"
 },
 "t_triangle_icelink": {
  "nimi": "Triangle IceLink",
  "pinnad": {
   "ice": {
    "mu": 0.1767,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-195-65R15-studded"
    ],
    "kaal": 0.08
   },
   "snow": {
    "mu": 0.3597,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-195-65R15-studded"
    ],
    "kaal": 0.16
   },
   "dry": {
    "mu": 0.8549,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-195-65R15-studded"
    ],
    "kaal": 0.16
   },
   "wet": {
    "mu": 1.2712,
    "n": 1,
    "testid": [
     "ZaRulem-2016-W-195-65R15-studded"
    ],
    "kaal": 0.16
   }
  },
  "testid": [
   "ZaRulem-2016-W-195-65R15-studded"
  ],
  "viimane": 2016,
  "g_allikas": "test"
 },
 "t_triangle_icelink_sport_utility": {
  "nimi": "Triangle Icelink Sport Utility",
  "pinnad": {
   "ice": {
    "mu": 0.1634,
    "n": 1,
    "testid": [
     "ZaRulem-2020-W-215-65R16-studded"
    ],
    "kaal": 0.13
   },
   "snow": {
    "mu": 0.3718,
    "n": 1,
    "testid": [
     "ZaRulem-2020-W-215-65R16-studded"
    ],
    "kaal": 0.24
   },
   "dry": {
    "mu": 0.8639,
    "n": 1,
    "testid": [
     "ZaRulem-2020-W-215-65R16-studded"
    ],
    "kaal": 0.27
   },
   "wet": {
    "mu": 1.3146,
    "n": 1,
    "testid": [
     "ZaRulem-2020-W-215-65R16-studded"
    ],
    "kaal": 0.27
   }
  },
  "testid": [
   "ZaRulem-2020-W-215-65R16-studded"
  ],
  "viimane": 2020,
  "g_allikas": "test"
 },
 "t_triangle_icelynx_ti501": {
  "nimi": "Triangle IceLynx TI501",
  "pinnad": {
   "ice": {
    "mu": 0.1444,
    "n": 1,
    "testid": [
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.25
   },
   "snow": {
    "mu": 0.3821,
    "n": 1,
    "testid": [
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.42
   },
   "dry": {
    "mu": 0.8533,
    "n": 1,
    "testid": [
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.51
   },
   "wet": {
    "mu": 1.4529,
    "n": 1,
    "testid": [
     "VIBILAGARE-2025-W-STUDDED-235-60R18"
    ],
    "kaal": 0.51
   }
  },
  "testid": [
   "VIBILAGARE-2025-W-STUDDED-235-60R18"
  ],
  "viimane": 2025,
  "g_allikas": "test"
 },
 "t_triangle_snowlink_pl01": {
  "nimi": "Triangle Snowlink PL01",
  "pinnad": {
   "ice": {
    "mu": 0.182,
    "n": 3,
    "testid": [
     "VIBILAGARE-2023-W-NORDIC-225-45R17",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction"
    ],
    "kaal": 0.46
   },
   "snow": {
    "mu": 0.361,
    "n": 3,
    "testid": [
     "VIBILAGARE-2023-W-NORDIC-225-45R17",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction"
    ],
    "kaal": 0.71
   },
   "dry": {
    "mu": 0.8547,
    "n": 3,
    "testid": [
     "VIBILAGARE-2023-W-NORDIC-225-45R17",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction"
    ],
    "kaal": 0.93
   },
   "wet": {
    "mu": 1.0903,
    "n": 3,
    "testid": [
     "VIBILAGARE-2023-W-NORDIC-225-45R17",
     "ZaRulem-2018-W-205-55R16-friction",
     "ZaRulem-2019-W-195-65R15-friction"
    ],
    "kaal": 0.93
   }
  },
  "testid": [
   "VIBILAGARE-2023-W-NORDIC-225-45R17",
   "ZaRulem-2018-W-205-55R16-friction",
   "ZaRulem-2019-W-195-65R15-friction"
  ],
  "viimane": 2023,
  "g_allikas": "test"
 },
 "t_vredestein_nord_trac_2": {
  "nimi": "Vredestein Nord-Trac 2",
  "pinnad": {
   "ice": {
    "mu": 0.1605,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   },
   "snow": {
    "mu": 0.3543,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   },
   "dry": {
    "mu": 0.8696,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   },
   "wet": {
    "mu": 1.1589,
    "n": 1,
    "testid": [
     "TM-2013-W-205-55R16"
    ],
    "kaal": 0.11
   }
  },
  "testid": [
   "TM-2013-W-205-55R16"
  ],
  "viimane": 2013,
  "g_allikas": "test"
 },
 "t_yokohama_iceguard_ig50_plus": {
  "nimi": "Yokohama iceGUARD iG50 Plus",
  "pinnad": {
   "ice": {
    "mu": 0.1578,
    "n": 1,
    "testid": [
     "TM-2016-W-205-55R16-friction"
    ],
    "kaal": 0.17
   },
   "snow": {
    "mu": 0.3618,
    "n": 1,
    "testid": [
     "TM-2016-W-205-55R16-friction"
    ],
    "kaal": 0.17
   }
  },
  "testid": [
   "TM-2016-W-205-55R16-friction"
  ],
  "viimane": 2016,
  "g_allikas": "D-klassi keskpunkt (märg mõõtmata)"
 },
 "t_yokohama_iceguard_ig55": {
  "nimi": "Yokohama iceGUARD iG55",
  "pinnad": {
   "ice": {
    "mu": 0.182,
    "n": 1,
    "testid": [
     "ZaRulem-2015-W-175-65R14-studded"
    ],
    "kaal": 0.07
   },
   "snow": {
    "mu": 0.359,
    "n": 1,
    "testid": [
     "ZaRulem-2015-W-175-65R14-studded"
    ],
    "kaal": 0.14
   },
   "dry": {
    "mu": 0.7905,
    "n": 1,
    "testid": [
     "ZaRulem-2015-W-175-65R14-studded"
    ],
    "kaal": 0.14
   },
   "wet": {
    "mu": 1.1519,
    "n": 1,
    "testid": [
     "ZaRulem-2015-W-175-65R14-studded"
    ],
    "kaal": 0.14
   }
  },
  "testid": [
   "ZaRulem-2015-W-175-65R14-studded"
  ],
  "viimane": 2015,
  "g_allikas": "test"
 },
 "t_yokohama_iceguard_ig60": {
  "nimi": "Yokohama IceGuard IG60",
  "pinnad": {
   "ice": {
    "mu": 0.2073,
    "n": 2,
    "testid": [
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2021-W-215-65R16-friction"
    ],
    "kaal": 0.29
   },
   "snow": {
    "mu": 0.377,
    "n": 2,
    "testid": [
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2021-W-215-65R16-friction"
    ],
    "kaal": 0.51
   },
   "dry": {
    "mu": 0.7972,
    "n": 2,
    "testid": [
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2021-W-215-65R16-friction"
    ],
    "kaal": 0.58
   },
   "wet": {
    "mu": 1.1216,
    "n": 2,
    "testid": [
     "ZaRulem-2020-W-205-55R16-friction",
     "ZaRulem-2021-W-215-65R16-friction"
    ],
    "kaal": 0.58
   }
  },
  "testid": [
   "ZaRulem-2020-W-205-55R16-friction",
   "ZaRulem-2021-W-215-65R16-friction"
  ],
  "viimane": 2021,
  "g_allikas": "test"
 },
 "t_yokohama_iceguard_ig65": {
  "nimi": "Yokohama iceGUARD iG65",
  "pinnad": {
   "ice": {
    "mu": 0.2072,
    "n": 7,
    "testid": [
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ZaRulem-2018-W-215-65R16-studded",
     "ZaRulem-2019-W-205-55R16-studded",
     "ZaRulem-2020-W-215-65R16-studded",
     "ZaRulem-2020-W-225-45R17-studded",
     "ZaRulem-2021-W-205-55R16-studded",
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 1.05
   },
   "snow": {
    "mu": 0.375,
    "n": 7,
    "testid": [
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ZaRulem-2018-W-215-65R16-studded",
     "ZaRulem-2019-W-205-55R16-studded",
     "ZaRulem-2020-W-215-65R16-studded",
     "ZaRulem-2020-W-225-45R17-studded",
     "ZaRulem-2021-W-205-55R16-studded",
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 1.64
   },
   "dry": {
    "mu": 0.842,
    "n": 7,
    "testid": [
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ZaRulem-2018-W-215-65R16-studded",
     "ZaRulem-2019-W-205-55R16-studded",
     "ZaRulem-2020-W-215-65R16-studded",
     "ZaRulem-2020-W-225-45R17-studded",
     "ZaRulem-2021-W-205-55R16-studded",
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 1.9
   },
   "wet": {
    "mu": 1.2969,
    "n": 7,
    "testid": [
     "VIBILAGARE-2018-W-STUDDED-205-55R16",
     "ZaRulem-2018-W-215-65R16-studded",
     "ZaRulem-2019-W-205-55R16-studded",
     "ZaRulem-2020-W-215-65R16-studded",
     "ZaRulem-2020-W-225-45R17-studded",
     "ZaRulem-2021-W-205-55R16-studded",
     "ZaRulem-2022-W-235-60R18-studded"
    ],
    "kaal": 1.9
   }
  },
  "testid": [
   "VIBILAGARE-2018-W-STUDDED-205-55R16",
   "ZaRulem-2018-W-215-65R16-studded",
   "ZaRulem-2019-W-205-55R16-studded",
   "ZaRulem-2020-W-215-65R16-studded",
   "ZaRulem-2020-W-225-45R17-studded",
   "ZaRulem-2021-W-205-55R16-studded",
   "ZaRulem-2022-W-235-60R18-studded"
  ],
  "viimane": 2022,
  "g_allikas": "test"
 }
}
