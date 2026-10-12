"""섹션 4 — 회로의 기초 그림."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))
import draw_helpers as D  # noqa: E402
import style as S  # noqa: E402
from matplotlib.patches import Circle, Polygon, Rectangle  # noqa: E402

C = D.C


# ── 로컬 도우미 ────────────────────────────────────
def broken_mark(ax, cx, cy, s=0.32, color=S.RESIST):
    for dx in (-1, 1):
        ax.plot([cx - s, cx + s], [cy - s * dx, cy + s * dx], color=C(color), lw=6,
                solid_capstyle="round", zorder=30)


def ladder(ax, xl, xr, yb, rungs, bat_label="3V", bat_w=1.3, bat_h=0.6, r=0.35,
           flow=True, lw=5, n_e=0):
    """왼쪽·오른쪽 세로선 + 아래 건전지 + 위쪽 가로줄(rungs).

    rungs: [(y, [bulb 설정...]), ...]  bulb 설정 = dict(x=, lit=, brightness=, broken=)
    """
    cx = (xl + xr) / 2
    neg, pos = D.battery(ax, cx, yb, w=bat_w, h=bat_h, label=bat_label)
    top = max(y for y, _ in rungs)
    D.wire(ax, [neg, (xl, yb), (xl, top)], lw=lw)
    D.wire(ax, [pos, (xr, yb), (xr, top)], lw=lw)
    for y, bulbs in rungs:
        xs = [xl]
        for b in bulbs:
            l, rr = D.bulb(ax, b["x"], y + r * 1.45, r=r, lit=b.get("lit", True),
                           brightness=b.get("brightness", 1.0))
            xs += [l[0], rr[0]]
            if b.get("broken"):
                broken_mark(ax, b["x"], y + r * 1.45, s=r * 0.8)
        xs.append(xr)
        for i in range(0, len(xs), 2):
            D.wire(ax, [(xs[i], y), (xs[i + 1], y)], lw=lw)
    return cx


def panel_title(ax, x, y, s, fc):
    D.pill(ax, x, y, s, fc=fc, size=17)


# ── 04_open_closed ────────────────────────────────
def loop_circuit(ax, x0, y0, w, h, closed):
    lw = 5
    cx = x0 + w / 2
    neg, pos = D.battery(ax, cx, y0, w=1.5, h=0.7, label="1.5V")
    yt = y0 + h
    r = 0.42
    bx = x0 + w * 0.36
    l, rr = D.bulb(ax, bx, yt + r * 1.45, r=r, lit=closed)
    s1, s2 = x0 + w * 0.66, x0 + w * 0.86
    D.wire(ax, [neg, (x0, y0), (x0, yt), (l[0], yt)], lw=lw)
    D.wire(ax, [(rr[0], yt), (s1, yt)], lw=lw)
    D.switch(ax, s1, s2, yt, closed=closed)
    D.wire(ax, [(s2, yt), (x0 + w, yt), (x0 + w, y0), pos], lw=lw)
    if closed:
        path = [(x0, y0), (x0, yt), (l[0] - 0.45, yt)]
        D.electrons_along(ax, path, 5, r=0.12)
        D.electrons_along(ax, [(s2, yt), (x0 + w, yt), (x0 + w, y0)], 4, r=0.12)
        D.arrow(ax, x0 - 0.35, y0 + h * 0.3, x0 - 0.35, y0 + h * 0.75, color=S.CURRENT, lw=4)
        D.arrow(ax, x0 + w + 0.35, yt - h * 0.25, x0 + w + 0.35, y0 + h * 0.25, color=S.CURRENT, lw=4)
    else:
        # 끊어진 곳 강조
        gx = (s1 + s2) / 2
        ax.add_patch(Circle((gx, yt + 0.12), 0.55, fc="none", ec=C(S.RESIST), lw=3,
                            ls=(0, (4, 3)), zorder=20))
        D.text(ax, gx, yt + 0.9, "끊김!", size=16, weight="bold", color=S.RESIST)


def fig_open_closed():
    W, H = S.FIG_FULL
    fig, ax = D.new_fig(W, H)
    for i, closed in enumerate((False, True)):
        px = 0.2 + i * 6.0
        D.box(ax, px, 0.15, 5.6, 4.6, fc=S.PANEL, r=0.25, z=0)
        loop_circuit(ax, px + 1.0, 1.25, 3.6, 1.8, closed)
        if closed:
            panel_title(ax, px + 0.95, 4.3, "닫힌 회로", S.SAFE)
            D.pill(ax, px + 2.8, 0.55, "전기 흐름 → 전구 켜짐", fc=S.CURRENT, size=15)
        else:
            panel_title(ax, px + 0.95, 4.3, "열린 회로", S.RESIST)
            D.pill(ax, px + 2.8, 0.55, "전기 멈춤 → 전구 꺼짐", fc=S.INK_SOFT, size=15)
    D.save(fig, "04_open_closed")


# ── 04_symbols ────────────────────────────────────
def sym_lead(ax, x1, x2, y, lw=3):
    ax.plot([x1, x2], [y, y], color=C(S.INK), lw=lw, solid_capstyle="round", zorder=5)


def sym_battery(ax, cx, cy):
    sym_lead(ax, cx - 0.62, cx - 0.1, cy)
    sym_lead(ax, cx + 0.1, cx + 0.62, cy)
    ax.plot([cx - 0.1, cx - 0.1], [cy - 0.18, cy + 0.18], color=C(S.INK), lw=5, zorder=5)
    ax.plot([cx + 0.1, cx + 0.1], [cy - 0.4, cy + 0.4], color=C(S.INK), lw=3, zorder=5)
    D.text(ax, cx + 0.32, cy + 0.42, "+", size=16, weight="bold", color=S.RESIST)


def sym_bulb(ax, cx, cy, r=0.3):
    sym_lead(ax, cx - 0.62, cx - r, cy)
    sym_lead(ax, cx + r, cx + 0.62, cy)
    ax.add_patch(Circle((cx, cy), r, fc="white", ec=C(S.INK), lw=3, zorder=5))
    k = r * 0.707
    for s in (1, -1):
        ax.plot([cx - k, cx + k], [cy - k * s, cy + k * s], color=C(S.INK), lw=3, zorder=6)


def sym_switch(ax, cx, cy):
    sym_lead(ax, cx - 0.62, cx - 0.3, cy)
    sym_lead(ax, cx + 0.3, cx + 0.62, cy)
    for x in (cx - 0.3, cx + 0.3):
        ax.add_patch(Circle((x, cy), 0.07, fc="white", ec=C(S.INK), lw=2.5, zorder=6))
    ax.plot([cx - 0.3, cx + 0.25], [cy, cy + 0.33], color=C(S.INK), lw=3, solid_capstyle="round", zorder=5)


def sym_resistor(ax, cx, cy):
    pts = [(cx - 0.62, cy), (cx - 0.45, cy)]
    n = 6
    for i in range(n):
        pts.append((cx - 0.45 + 0.9 * (i + 0.5) / n, cy + (0.22 if i % 2 == 0 else -0.22)))
    pts += [(cx + 0.45, cy), (cx + 0.62, cy)]
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=C(S.INK), lw=3, solid_joinstyle="round", zorder=5)


def sym_wire(ax, cx, cy):
    sym_lead(ax, cx - 0.62, cx + 0.62, cy)


def sym_led(ax, cx, cy):
    sym_lead(ax, cx - 0.62, cx - 0.22, cy)
    sym_lead(ax, cx + 0.22, cx + 0.62, cy)
    ax.add_patch(Polygon([(cx - 0.22, cy + 0.25), (cx - 0.22, cy - 0.25), (cx + 0.2, cy)],
                         closed=True, fc=C(S.INK), ec=C(S.INK), lw=2, zorder=5))
    ax.plot([cx + 0.22, cx + 0.22], [cy - 0.27, cy + 0.27], color=C(S.INK), lw=3, zorder=5)
    for dx in (-0.05, 0.13):
        D.arrow(ax, cx + dx, cy + 0.32, cx + dx + 0.22, cy + 0.58, color=S.SPARK, lw=2.5, head=10)


def pic_resistor(ax, cx, cy):
    ax.plot([cx - 0.62, cx + 0.62], [cy, cy], color=C(S.METAL), lw=4, zorder=4)
    D.box(ax, cx - 0.45, cy - 0.18, 0.9, 0.36, fc="E9D3A8", ec=S.INK, lw=2, r=0.15, z=5)
    for x, col in ((-0.25, "8B4513"), (-0.08, "111111"), (0.09, "E5533D"), (0.28, "D4AF37")):
        ax.add_patch(Rectangle((cx + x - 0.04, cy - 0.17), 0.08, 0.34, fc=C(col), ec="none", zorder=6))


def pic_wire(ax, cx, cy):
    D.box(ax, cx - 0.6, cy - 0.13, 1.2, 0.26, fc=S.RESIST, r=0.12, z=5)
    for s in (-1, 1):
        ax.plot([cx + s * 0.6, cx + s * 0.85], [cy, cy], color=C(S.COPPER), lw=5,
                solid_capstyle="round", zorder=4)


def pic_switch(ax, cx, cy):
    D.box(ax, cx - 0.42, cy - 0.55, 0.84, 1.1, fc="FFFFFF", ec=S.INK, lw=2.5, r=0.12, z=4)
    D.box(ax, cx - 0.2, cy - 0.32, 0.4, 0.64, fc=S.PANEL, ec=S.INK, lw=2, r=0.08, z=5)
    D.box(ax, cx - 0.16, cy - 0.02, 0.32, 0.3, fc=S.INK_SOFT, r=0.06, z=6)


def pic_led(ax, cx, cy):
    ax.add_patch(Circle((cx, cy + 0.3), 0.55, fc=C(S.GLOW), ec="none", alpha=0.45, zorder=3))
    D.box(ax, cx - 0.25, cy - 0.05, 0.5, 0.55, fc="FF6B5A", r=0.0, z=5)
    ax.add_patch(Circle((cx, cy + 0.5), 0.25, fc=C("FF6B5A"), ec="none", zorder=5))
    D.box(ax, cx - 0.3, cy - 0.12, 0.6, 0.1, fc="E04A3A", r=0.02, z=6)
    ax.plot([cx - 0.1, cx - 0.1], [cy - 0.12, cy - 0.75], color=C(S.METAL), lw=3.5, zorder=4)
    ax.plot([cx + 0.1, cx + 0.1], [cy - 0.12, cy - 0.58], color=C(S.METAL), lw=3.5, zorder=4)


def fig_symbols():
    W, H = S.FIG_FULL
    fig, ax = D.new_fig(W, H)
    items = [
        ("건전지", lambda a, x, y: D.battery(a, x, y, w=1.2, h=0.55, label=None), sym_battery),
        ("전구", lambda a, x, y: D.bulb(a, x, y + 0.2, r=0.36, lit=True, brightness=0.6), sym_bulb),
        ("스위치", pic_switch, sym_switch),
        ("저항", pic_resistor, sym_resistor),
        ("전선", pic_wire, sym_wire),
        ("LED", pic_led, sym_led),
    ]
    colw = W / len(items)
    for i, (name, pic, sym) in enumerate(items):
        cx = colw * (i + 0.5)
        D.box(ax, cx - colw / 2 + 0.12, 0.15, colw - 0.24, 4.6, fc=S.PANEL, r=0.2, z=0)
        D.text(ax, cx, 4.35, name, size=18, weight="bold")
        pic(ax, cx, 3.15)
        D.big_arrow(ax, cx, 2.25, cx, 1.75, color=S.LINE, width=0.16)
        D.box(ax, cx - colw / 2 + 0.3, 0.45, colw - 0.6, 1.15, fc="FFFFFF", r=0.15, z=1)
        sym(ax, cx, 1.02)
    D.save(fig, "04_symbols")


# ── 04_series / 04_parallel ───────────────────────
def mini_panel(ax, x, y, w, h, title, result, rcolor):
    D.box(ax, x, y, w, h, fc=S.PANEL, r=0.2, z=0)
    D.text(ax, x + w - 1.45, y + 1.4, title, size=15, weight="bold")
    D.pill(ax, x + w - 1.45, y + 0.7, result, fc=rcolor, size=15)


def fig_series():
    W, H = S.FIG_SPLIT
    fig, ax = D.new_fig(W, H)
    # 메인: 한 줄에 전구 두 개 (어둡게)
    ladder(ax, 0.9, 6.3, 2.6, [(3.85, [dict(x=2.6, brightness=0.45), dict(x=4.6, brightness=0.45)])],
           r=0.38, bat_label="3V")
    D.electrons_along(ax, [(0.9, 2.6), (0.9, 3.85), (1.8, 3.85)], 3, r=0.1)
    D.electrons_along(ax, [(5.4, 3.85), (6.3, 3.85), (6.3, 2.6)], 3, r=0.1)
    # 작은 그림: 하나 고장
    mini_panel(ax, 0.1, 0.05, 7.0, 2.0, "하나가 고장 나면?", "모두 꺼짐", S.RESIST)
    ladder(ax, 0.5, 3.9, 0.45, [(1.1, [dict(x=1.55, lit=False, broken=True), dict(x=2.85, lit=False)])],
           r=0.22, bat_label=None, bat_w=0.9, bat_h=0.38, lw=3.5)
    D.save(fig, "04_series")


def fig_parallel():
    W, H = S.FIG_SPLIT
    fig, ax = D.new_fig(W, H)
    ladder(ax, 1.2, 6.0, 2.5, [(3.25, [dict(x=4.9)]), (4.3, [dict(x=2.7)])], r=0.25, bat_label="3V")
    D.electrons_along(ax, [(1.2, 2.5), (1.2, 4.3), (2.35, 4.3)], 4, r=0.09)
    D.electrons_along(ax, [(1.2, 3.25), (3.9, 3.25)], 3, r=0.09)
    mini_panel(ax, 0.1, 0.05, 7.0, 2.0, "하나가 고장 나면?", "나머지는 켜짐", S.SAFE)
    ladder(ax, 0.5, 3.9, 0.4, [(1.0, [dict(x=2.9, lit=False, broken=True)]),
                               (1.5, [dict(x=1.5, brightness=0.8)])],
           r=0.15, bat_label=None, bat_w=0.9, bat_h=0.32, lw=3)
    D.save(fig, "04_parallel")


# ── 04_house_parallel ─────────────────────────────
def fridge(ax, cx, yb, h=1.6):
    D.box(ax, cx - 0.45, yb, 0.9, h, fc="FFFFFF", ec=S.INK, lw=2.5, r=0.12, z=5)
    ax.plot([cx - 0.45, cx + 0.45], [yb + h * 0.66, yb + h * 0.66], color=C(S.INK), lw=2, zorder=6)
    for y in (yb + h * 0.74, yb + h * 0.3):
        ax.plot([cx + 0.28, cx + 0.28], [y, y + h * 0.17], color=C(S.INK_SOFT), lw=3.5,
                solid_capstyle="round", zorder=6)
    D.text(ax, cx - 0.1, yb + h * 0.33, "❄", size=16, color=S.CURRENT)
    return (cx, yb + h)


def tv(ax, cx, yb, on=True):
    D.box(ax, cx - 0.85, yb + 0.45, 1.7, 1.05, fc=S.CURRENT if on else S.INK, ec=S.INK, lw=3, r=0.08, z=5)
    ax.plot([cx, cx], [yb + 0.1, yb + 0.45], color=C(S.INK), lw=4, zorder=4)
    ax.plot([cx - 0.4, cx + 0.4], [yb + 0.1, yb + 0.1], color=C(S.INK), lw=4,
            solid_capstyle="round", zorder=4)
    return (cx, yb + 1.5)


def pendant(ax, cx, ytop, on=True):
    yb = ytop - 1.0
    ax.add_patch(Polygon([(cx - 0.18, ytop - 0.55), (cx + 0.18, ytop - 0.55), (cx + 0.5, yb),
                          (cx - 0.5, yb)], closed=True, fc=C(S.INK_SOFT), ec="none", zorder=6))
    if on:
        ax.add_patch(Polygon([(cx - 0.5, yb), (cx + 0.5, yb), (cx + 1.0, yb - 1.4), (cx - 1.0, yb - 1.4)],
                             closed=True, fc=C(S.GLOW), ec="none", alpha=0.45, zorder=2))
    ax.add_patch(Circle((cx, yb), 0.2, fc=C(S.GLOW if on else "E6E9F0"), ec=C(S.INK), lw=2, zorder=7))
    return (cx, ytop - 0.55)


def outlet(ax, cx, cy):
    D.box(ax, cx - 0.45, cy - 0.45, 0.9, 0.9, fc="FFFFFF", ec=S.INK, lw=2.5, r=0.15, z=5)
    ax.add_patch(Circle((cx, cy), 0.3, fc=S.PANEL and C(S.PANEL), ec=C(S.INK), lw=2, zorder=6))
    for dx in (-0.12, 0.12):
        ax.add_patch(Circle((cx + dx, cy), 0.06, fc=C(S.INK), ec="none", zorder=7))
    return (cx, cy + 0.45)


def vswitch_open(ax, x, y1, y2):
    """세로 방향 열린 스위치 (y1 위, y2 아래)."""
    for y in (y1, y2):
        ax.add_patch(Circle((x, y), 0.07, fc="white", ec=C(S.INK), lw=2, zorder=8))
    L = y1 - y2
    ax.plot([x, x + L * 0.6], [y1, y1 - L * 0.8], color=C(S.INK), lw=3.5,
            solid_capstyle="round", zorder=7)


def fig_house_parallel():
    W, H = S.FIG_FULL
    fig, ax = D.new_fig(W, H)
    # 집 외곽
    roof = [(0.25, 3.75), (6.0, 4.8), (11.75, 3.75)]
    xs, ys = zip(*roof)
    ax.plot(xs, ys, color=C(S.INK), lw=4, solid_joinstyle="round", zorder=2)
    ax.plot([0.7, 0.7, 11.3, 11.3], [3.83, 0.15, 0.15, 3.83], color=C(S.INK), lw=4, zorder=2)
    # 분전반
    D.box(ax, 1.0, 1.7, 1.2, 1.5, fc=S.INK, r=0.12, z=5)
    D.bolt(ax, 1.6, 2.6, h=0.75, color=S.SPARK, z=6)
    D.text(ax, 1.6, 1.25, "분전반", size=15, weight="bold")
    D.text(ax, 1.6, 0.85, "(두꺼비집)", size=13, color=S.INK_SOFT)
    bus_y = 3.4
    D.wire(ax, [(2.2, 2.9), (2.5, 2.9), (2.5, bus_y), (10.6, bus_y)], color=S.COPPER, lw=6)
    D.pill(ax, 6.0, 4.05, "모두 220V", fc=S.VOLT, size=16)
    # 가지들
    apps = [
        ("냉장고", 3.8, True), ("TV", 5.95, False), ("전등", 8.0, True), ("콘센트", 10.0, True)
    ]
    for name, x, on in apps:
        if name == "냉장고":
            top = fridge(ax, x, 0.9)
        elif name == "TV":
            top = tv(ax, x, 0.8, on=on)
        elif name == "전등":
            top = pendant(ax, x, bus_y)
        else:
            top = outlet(ax, x, 1.6)
        ax.add_patch(Circle((x, bus_y), 0.09, fc=C(S.COPPER), ec="none", zorder=7))
        if on:
            D.wire(ax, [(x, bus_y), top], color=S.COPPER, lw=4)
            if top[1] < bus_y - 0.6:
                D.electrons_along(ax, [(x, bus_y), top], 2, r=0.08)
        else:
            D.wire(ax, [(x, bus_y), (x, bus_y - 0.3)], color=S.COPPER, lw=4)
            vswitch_open(ax, x, bus_y - 0.3, bus_y - 0.75)
            D.wire(ax, [(x, bus_y - 0.75), top], color=S.COPPER, lw=4)
        D.text(ax, x + 0.05, 0.5, name, size=15, weight="bold", ha="right")
        D.pill(ax, x + 0.5, 0.5, "켜짐" if on else "꺼짐", fc=S.SAFE if on else S.INK_SOFT, size=13)
    D.save(fig, "04_house_parallel")


def main():
    fig_open_closed()
    fig_symbols()
    fig_series()
    fig_parallel()
    fig_house_parallel()


if __name__ == "__main__":
    main()
