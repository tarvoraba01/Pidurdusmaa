# -*- coding: utf-8 -*-
"""MÕÕDETUD klassi keskmised -- loodud automaatselt.

Tee see uuesti:  python3 -m mudel.gklass_ext --write
Allikad: testitud rehvid (kalibreeri_gklass.py) + välistestid
(testid_ext/, päris EPREL-i märgised, vt gklass_ext.py).
Jäta-üks-test-välja: praegune 8.99 % -> uus 8.27 %.

Kuju: klass -> {"_": [G, n]} pluss (kategooria: [G, n]) seal, kus
mõõdetud rehve on vähemalt 3. n = mitu mõõdetud rehvi väärtuse taga.
Loodud: 2026-09-28
"""

G_CLASS_MEASURED = {
    'A': {'_': [1.355, 74], 'ALL_SEASON': [1.623, 3], 'SUMMER_TOURING': [1.49, 55], 'SUMMER_UHP': [1.638, 13], 'WINTER_CENTRAL': [1.355, 3]},
    'B': {'_': [1.243, 147], 'ALL_SEASON': [1.45, 37], 'SUMMER_TOURING': [1.384, 41], 'WINTER_CENTRAL': [1.243, 68]},
    'C': {'_': [1.166, 84], 'ALL_SEASON': [1.301, 13], 'SUMMER_TOURING': [1.37, 17], 'WINTER_CENTRAL': [1.166, 54], 'WINTER_NORDIC': [1.225, 6]},
    'D': {'_': [1.112, 15], 'WINTER_CENTRAL': [1.112, 9], 'WINTER_NORDIC': [1.225, 6]},
    'E': {'_': [1.016, 8], 'WINTER_CENTRAL': [1.016, 3], 'WINTER_NORDIC': [1.225, 5]},
}
