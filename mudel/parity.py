"""Python <-> JS paarsuse kontroll.

Genereerib juhuslikud juhtumid, laseb need labi Python-mootori ja
web/verify.js kaudu labi JS-mootori ning vordleb tulemusi.
Kaivita kaustast /home/claude:  python3 -m pidurdus.parity
"""
import json
import random
import subprocess
import tempfile
from dataclasses import replace

from .model import BrakingModel, Conditions, Surface, Texture
from .presets import TYRES, VEHICLES

N = 60
SURFACES = list(Surface)
TEXTURES = list(Texture)


def build_cases(n=N, seed=7):
    rnd = random.Random(seed)
    tk, vk = list(TYRES), list(VEHICLES)
    out = []
    for _ in range(n):
        t = rnd.choice(tk)
        v = rnd.choice(vk)
        surf = rnd.choice(SURFACES)
        wet = surf in (Surface.ASPHALT, Surface.CONCRETE) and rnd.random() < 0.5
        out.append({
            "tyre": t,
            "veh": v,
            "tyreOv": {
                "treadDepthMm": round(rnd.uniform(1.2, 8.5), 1),
                "pressureBar": round(rnd.uniform(1.6, 3.0), 2),
                "ageYears": rnd.choice([1, 3, 6, 9]),
            },
            "cond": {
                "speedKmh": round(rnd.uniform(20, 130), 1),
                "surface": surf.name,
                "texture": rnd.choice(TEXTURES).name,
                "waterMm": round(rnd.uniform(0.2, 6.0), 2) if wet else 0.0,
                "tempC": round(rnd.uniform(-20, 35), 1),
                "payloadKg": round(rnd.uniform(75, 450)),
                "gradientPct": round(rnd.uniform(-8, 8), 1),
                "reactionTimeS": rnd.choice([0.0, 0.8, 1.5]),
                "brakeCondition": rnd.choice([1.0, 0.85, 0.65, 0.45]),
            },
        })
    return out


def run_python(cases):
    m = BrakingModel()
    res = []
    for c in cases:
        t = TYRES[c["tyre"]]
        ov = c["tyreOv"]
        t = replace(t, tread_depth_mm=ov["treadDepthMm"],
                    pressure_bar=ov["pressureBar"], age_years=ov["ageYears"])
        cd = c["cond"]
        cond = Conditions(
            speed_kmh=cd["speedKmh"], surface=Surface[cd["surface"]],
            texture=Texture[cd["texture"]], water_mm=cd["waterMm"],
            temp_c=cd["tempC"], payload_kg=cd["payloadKg"],
            gradient_pct=cd["gradientPct"], reaction_time_s=cd["reactionTimeS"],
            brake_condition=cd["brakeCondition"])
        r = m.stopping_distance(t, VEHICLES[c["veh"]], cond)
        # Vordleme KOIKI valjundeid, mida leht kasutajale naitab, mitte
        # ainult pidurdusmaad. Varem oli siin ainult "d" -- ja just seda
        # auku mooda pugesid labi peatumistee / vahemiku ebakolad.
        res.append({"d": r.distance_m, "tot": r.total_distance_m,
                    "react": r.reaction_m, "lo": r.low_m, "hi": r.high_m,
                    "sig": r.sigma_rel, "mu": r.mu_effective,
                    "g": r.peak_decel_g, "t": r.time_s,
                    "lim": r.limiter, "conf": r.confidence,
                    "w": len(r.warnings), "at": r.accel_time_s,
                    "ad": r.accel_dist_m, "ex": r.extreme})
    return res


def main():
    cases = build_cases()
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(cases, f)
        path = f.name
    js = json.loads(subprocess.check_output(
        ["node", "web/verify.js", path], text=True))
    py = run_python(cases)

    bad = 0
    for i, (a, b) in enumerate(zip(py, js)):
        for k in ("d", "tot", "react", "lo", "hi", "sig", "mu", "g", "t",
                  "at", "ad"):
            if abs(a[k] - b[k]) > 1e-6 * max(1.0, abs(a[k])):
                print(f"#{i} {k}: py={a[k]!r} js={b[k]!r}  {cases[i]['cond']}")
                bad += 1
        for k in ("lim", "conf", "w", "ex"):
            if a[k] != b[k]:
                print(f"#{i} {k}: py={a[k]!r} js={b[k]!r}")
                bad += 1
    print(("PAARSUS OK" if not bad else f"ERINEVUSI: {bad}") + f"  ({len(py)} juhtumit)")
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
