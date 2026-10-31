# 예지보전 정답 — 설비별 평상 범위(평균 ± 2표준편차)로 이상 후보를 찾고 진동 그래프 한 장을 만든다.
# 실행 위치(현재 폴더)에 sensor_50_virtual.csv 가 있어야 한다. 결과: anomaly.csv · index.html · expected.json
import csv, json, statistics as st
from pathlib import Path

SRC = "sensor_50_virtual.csv"
COLS = {"진동(mm/s)": "mm/s", "온도(℃)": "℃", "압력(bar)": "bar"}

rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig")))
equips = sorted({r["설비"] for r in rows})

# 1) 설비별·변수별 평상 범위 — 표본 표준편차(Google Sheets STDEV와 같은 방식)
stats, cands = {}, []
for eq in equips:
    rs = [r for r in rows if r["설비"] == eq]
    for col in COLS:
        v = [float(r[col]) for r in rs]
        m, sd = st.mean(v), st.stdev(v)
        lo, hi = m - 2 * sd, m + 2 * sd
        stats[(eq, col)] = (m, sd, lo, hi)
        for r, x in zip(rs, v):
            if x < lo or x > hi:
                cands.append({"설비": eq, "시간": r["시간"], "변수": col, "값": x,
                              "평상 범위": f"{lo:.2f} ~ {hi:.2f}"})

# 2) 이상 후보 저장
with open("anomaly.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["설비", "시간", "변수", "값", "평상 범위"])
    w.writeheader(); w.writerows(cands)

# 3) 진동 그래프 한 장 (SVG, 외부 라이브러리 없음)
VIB = "진동(mm/s)"
W, H, L, R, T, B = 640, 340, 44, 16, 16, 40
ymax = 4.0
times = [r["시간"][11:16] for r in rows if r["설비"] == equips[0]]
n = len(times)
X = lambda i: L + i * (W - L - R) / (n - 1)
Y = lambda y: T + (1 - y / ymax) * (H - T - B)
color = {equips[0]: "var(--a)", equips[1]: "var(--b)"}
short = {eq: eq.split("(")[0] for eq in equips}
svg = []
for y in range(0, 5):  # 가로 눈금
    svg.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(y):.1f}" y2="{Y(y):.1f}" class="grid"/>'
               f'<text x="{L-8}" y="{Y(y)+4:.1f}" class="tick" text-anchor="end">{y}</text>')
for i in range(0, n, 6):  # 세로 눈금(2시간 간격)
    svg.append(f'<text x="{X(i):.1f}" y="{H-B+18}" class="tick" text-anchor="middle">{times[i]}</text>')
for eq in equips:
    v = [float(r[VIB]) for r in rows if r["설비"] == eq]
    hi = stats[(eq, VIB)][3]
    svg.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(hi):.1f}" y2="{Y(hi):.1f}" stroke="{color[eq]}" class="limit"/>')
    pts = " ".join(f"{X(i):.1f},{Y(y):.1f}" for i, y in enumerate(v))
    svg.append(f'<polyline points="{pts}" fill="none" stroke="{color[eq]}" stroke-width="2"/>')
    for i, y in enumerate(v):
        if y > hi:
            svg.append(f'<circle cx="{X(i):.1f}" cy="{Y(y):.1f}" r="5" class="hit"/>'
                       f'<text x="{X(i)-8:.1f}" y="{Y(y)+4:.1f}" class="lab" text-anchor="end">{y}</text>')
legend = "".join(
    f'<span><i style="background:{color[eq]}"></i>{short[eq]} · 상한 {stats[(eq, VIB)][3]:.2f}</span>' for eq in equips)
a_hi, b_hi = stats[(equips[0], VIB)][3], stats[(equips[1], VIB)][3]
html = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>노이즈 vs 추세</title>
<style>
:root{{--bg:#fafaf8;--fg:#1d1d1b;--mute:#6b6b66;--line:#e2e1dc;--a:#2f6db5;--b:#c2571a;--hit:#c62828}}
@media (prefers-color-scheme:dark){{:root{{--bg:#161615;--fg:#ecebe6;--mute:#a09f99;--line:#33322f;--a:#6fa3e0;--b:#ee8a4f;--hit:#ff6b6b}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:system-ui,"Malgun Gothic",sans-serif}}
main{{max-width:720px;margin:0 auto;padding:24px 16px}}
h1{{font-size:1.3rem;margin:0 0 6px}} p{{margin:0 0 14px;line-height:1.5}}
svg{{width:100%;height:auto;display:block}}
.grid{{stroke:var(--line)}} .tick{{fill:var(--mute);font-size:11px}}
.limit{{stroke-dasharray:5 4;stroke-width:1.2;opacity:.8}}
.hit{{fill:none;stroke:var(--hit);stroke-width:2}} .lab{{fill:var(--hit);font-size:12px;font-weight:600}}
.legend{{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:.85rem;color:var(--mute);margin:6px 0 12px}}
.legend i{{display:inline-block;width:14px;height:3px;margin-right:6px;vertical-align:middle}}
small{{color:var(--mute);line-height:1.5;display:block}}
</style></head><body><main>
<h1>노이즈 vs 추세 — 설비A·B 진동</h1>
<p>설비A는 3.5 mm/s 한 번 튀고 돌아온 <b>노이즈</b>, 설비B는 꾸준히 오르는 <b>추세</b>(2.2→2.9) — 정비 신호는 설비B.</p>
<div class="legend">{legend}<span>점선 = 평상 범위 상한(평균 + 2σ) · 빨간 원 = 이상 후보</span></div>
<svg viewBox="0 0 {W} {H}" role="img" aria-label="설비A·B 진동 시계열">{"".join(svg)}</svg>
<small>진동 단위 mm/s · 2026-09-15 08:00~16:00, 20분 간격 · 평상 범위는 설비별 평균 ± 2 × 표본 표준편차.<br>
가상 데이터 — 출처: keerhee/kma-auto-genai-3-1 data/Day5/Day5_설비센서_50건_가상.csv (Day5 예지보전 실습용)</small>
</main></body></html>'''
Path("index.html").write_text(html, encoding="utf-8")

# 4) 기준 수치
def first(eq, col):
    return [c["값"] for c in cands if c["설비"] == eq and c["변수"] == col]
a_c, b_c, bt_c = first(equips[0], VIB), first(equips[1], VIB), first(equips[1], "온도(℃)")
vals = {
    "rows": {"value": len(rows), "decimals": 0, "block": 0},
    "A_vib_upper": {"value": round(a_hi, 2), "decimals": 2, "block": 1},
    "A_vib_candidate": {"value": a_c[0], "decimals": 1, "block": 1},
    "A_vib_candidate_count": {"value": len(a_c), "decimals": 0, "block": 1},
    "B_vib_upper": {"value": round(b_hi, 2), "decimals": 2, "block": 1},
    "B_vib_candidate_1": {"value": b_c[0], "decimals": 1, "block": 1},
    "B_vib_candidate_2": {"value": b_c[1], "decimals": 1, "block": 1},
    "B_temp_candidate": {"value": bt_c[0], "decimals": 1, "block": 1},
    "candidates_total": {"value": len(cands), "decimals": 0, "block": 1},
}
Path("expected.json").write_text(json.dumps({"values": vals}, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: v["value"] for k, v in vals.items()}, ensure_ascii=False))
