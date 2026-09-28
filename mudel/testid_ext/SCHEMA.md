Output: ONE JSON file (UTF-8) = array of TEST objects.

TEST object:
{
 "test_id": "ADAC-2023-S-205-55R16",        // publication-year-season-size, unique
 "publication": "ADAC",                       // magazine / organisation that ran the test
 "year": 2023,                                // publication year
 "season": "summer" | "winter" | "allseason",
 "size": "205/55 R16",                        // test size (if several sizes in one article, make one TEST per size)
 "car": "VW Golf 8",                          // test car if given, else null
 "tester": "ADAC / GTÜ proving ground ..." or null,
 "url": "https://...",                        // page you actually read the numbers from
 "url_original": "https://..." or null,       // original magazine page/PDF if different
 "disciplines": [                             // one per braking measurement published
   {"id":"wet","surface":"asphalt"|"concrete"|"snow"|"ice"|"gravel",
    "wet": true|false, "v_from": 80, "v_to": 0,
    "temp_c": 12 or null,                     // ONLY if the source states it
    "note": "e.g. ABS, average of 10 stops, water depth if given" }
 ],
 "tyres": [
   {"name": "Michelin Primacy 4+",            // exact brand + model as published
    "category": "summer"|"summer_uhp"|"allseason"|"winter_central"|"winter_nordic"|"winter_studded",
    "label_wet": "A".."E" or null,            // EU label wet grip class ONLY if the source prints it
    "results": {"wet": 32.1, "dry": 35.4, ...}, // keys = discipline ids; METRES, absolute, as published
    "aqua_kmh": 72.3 or null,                 // straight aquaplaning float speed if published
    "note": "" }
 ]
}

Rules:
- Only absolute braking distances in metres. If a source gives only % / ranks / points / "metres behind the winner" without the winner's absolute value, do not convert — skip that discipline (or compute ONLY if the winner's absolute distance is printed in the same table, and say so in the discipline note).
- Numbers exactly as published. Do not round, do not invent, do not average across sources.
- Record v_from / v_to exactly (e.g. 100->1, 80->5, 30->5, 20->5). This matters.
- Do NOT copy article prose. Numbers, names, and short neutral notes only.
