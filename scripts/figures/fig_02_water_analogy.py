"""섹션 2. 전압·전류·저항 — 물 비유 그림."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))
import draw_helpers as D  # noqa: E402
import style as S  # noqa: E402
from matplotlib.patches import Circle, Polygon, Rectangle  # noqa: E402

C = S.mpl


def pipe_path(ax, pts, d_lw=18):
    """꺾인 수도관 (테두리 INK + 속 물)."""
    D.wire(ax, pts, color=S.INK, lw=d_lw + 6, z=3)
    D.wire(ax, pts, color=S.WATER, lw=d_lw, z=4)


def water_wheel(ax, cx, cy, r=0.5):
    ax.add_patch(Circle((cx, cy), r, fc="white", ec=C(S.INK), lw=3, zorder=8))
    for i in range(8):
        a = math.radians(i * 45)
        ax.plot([cx, cx + r * 1.3 * math.cos(a)], [cy, cy + r * 1.3 * math.sin(a)],
                color=C("8C6A4A"), lw=5, solid_capstyle="round", zorder=9)
    ax.add_patch(Circle((cx, cy), r * 0.22, fc=C(S.INK), ec="none", zorder=10))


def pump(ax, cx, cy, r=0.45):
    ax.add_patch(Circle((cx, cy), r, fc=C(S.VOLT), ec=C(S.INK), lw=3, zorder=8))
    D.arrow(ax, cx, cy - r * 0.55, cx, cy + r * 0.6, color="FFFFFF", lw=4, head=14, z=9)


# ── 02_water_vs_circuit ─────────────────────────
def water_vs_circuit():
    w, h = S.FIG_FULL
    fig, ax = D.new_fig(w, h)
    # 물 회로
    L, R, B, T = 0.7, 4.9, 0.85, 3.9
    pipe_path(ax, [(L, B), (R, B), (R, T), (L, T), (L, B)])
    pump(ax, L, 2.35)
    water_wheel(ax, R, 2.35)
    for x in (1.7, 2.8, 3.9):
        D.arrow(ax, x, T, x + 0.45, T, color=S.WATER_DARK, lw=3, head=12, z=6)
        D.arrow(ax, x + 0.45, B, x, B, color=S.WATER_DARK, lw=3, head=12, z=6)
    D.pill(ax, 1.8, 2.35, "펌프", fc=S.VOLT, size=16)
    D.pill(ax, 3.7, 2.35, "물레방아", fc=S.SPARK, tc=S.INK, size=16)
    D.pill(ax, 2.8, 4.45, "수도관", fc=S.INK, size=16)
    D.pill(ax, 2.8, 0.3, "물", fc=S.CURRENT, size=16)

    # 가운데 =
    D.text(ax, 6.0, 2.35, "=", size=54, color=S.INK_SOFT, weight="bold")

    # 전기 회로
    bx, RX, T2, B2 = 7.0, 10.9, 3.9, 0.85
    top, bot = D.battery(ax, bx, 2.35, w=1.5, h=0.72, label="", vertical=True)
    r = 0.4
    cy = 2.55
    l_pt, r_pt = D.bulb(ax, RX, cy, r=r, lit=True)
    sock_y = l_pt[1]
    D.wire(ax, [top, (bx, T2), (RX, T2), (RX, cy + r)], lw=6, z=5)
    D.wire(ax, [bot, (bx, B2), (RX, B2), (RX, sock_y)], lw=6)
    D.electrons_along(ax, [(bx, 3.3), (bx, T2), (RX - 0.9, T2)], 8, r=0.09)
    D.electrons_along(ax, [(bx, 1.4), (bx, B2), (RX, B2), (RX, 1.3)], 9, r=0.09)
    D.pill(ax, 8.15, 2.35, "건전지", fc=S.VOLT, size=16)
    D.pill(ax, 9.45, 2.35, "전구", fc=S.SPARK, tc=S.INK, size=16)
    D.pill(ax, 9.0, 4.45, "전선", fc=S.INK, size=16)
    D.pill(ax, 9.0, 0.3, "전기 (전자)", fc=S.CURRENT, size=16)
    D.save(fig, "02_water_vs_circuit")


# ── 02_voltage ──────────────────────────────────
def jet(ax, x0, y0, reach, drop, lw):
    xs = [x0 + reach * t / 30 for t in range(31)]
    ys = [y0 - drop * (t / 30) ** 2 for t in range(31)]
    ax.plot(xs, ys, color=C(S.WATER), lw=lw, solid_capstyle="round", zorder=3)


def voltage():
    w, h = S.FIG_SPLIT
    fig, ax = D.new_fig(w, h)
    floor = 0.75
    D.box(ax, 0.2, floor - 0.12, 6.8, 0.12, fc=S.LINE, r=0.04)

    def tank_unit(x, tw, th, level, reach, lw, tag):
        base_y = floor + 0.5
        D.box(ax, x + 0.1, floor, tw - 0.2, 0.5, fc=S.METAL, r=0.05)
        D.tank(ax, x, base_y, tw, th, level=level)
        # 출구 파이프
        D.pipe(ax, x + tw, x + tw + 0.3, base_y + 0.2, d=0.2)
        jet(ax, x + tw + 0.3, base_y + 0.2, reach, base_y + 0.2 - floor, lw)
        # 수위 화살표
        ax_x = x - 0.3
        D.arrow(ax, ax_x, base_y, ax_x, base_y + th * level, color=S.VOLT, lw=3, head=12, style="<|-|>")
        D.pill(ax, x + tw / 2, base_y + th + 0.4, tag, fc=S.VOLT, size=15)

    tank_unit(0.8, 1.2, 1.4, 0.55, 0.5, 5, "1.5V 건전지")
    tank_unit(3.9, 1.2, 3.0, 0.9, 1.4, 12, "220V 콘센트")
    D.text(ax, 1.75, 0.3, "졸졸 — 약하게", size=15, color=S.INK_SOFT, weight="bold")
    D.text(ax, 5.3, 0.3, "콸콸 — 세게", size=15, color=S.INK, weight="bold")
    D.text(ax, 2.4, 3.9, "물이 높을수록\n= 전압이 클수록", size=16, color=S.VOLT, weight="bold",
           linespacing=1.4)
    D.save(fig, "02_voltage")


# ── 02_current ──────────────────────────────────
def faucet(ax, cx, top=4.3):
    D.box(ax, cx - 1.15, top - 0.35, 1.3, 0.35, fc=S.METAL, ec=S.INK, lw=2.5, r=0.06, z=5)
    D.box(ax, cx - 0.17, top - 0.85, 0.34, 0.85, fc=S.METAL, ec=S.INK, lw=2.5, r=0.06, z=6)
    D.box(ax, cx - 0.55, top + 0.05, 0.6, 0.16, fc=S.INK_SOFT, r=0.05, z=6)
    D.box(ax, cx - 0.32, top - 0.02, 0.14, 0.12, fc=S.INK_SOFT, r=0.02, z=6)
    return top - 0.85


def cup(ax, cx, level):
    y0, ch, cw = 1.0, 1.0, 1.3
    ax.add_patch(Rectangle((cx - cw / 2, y0), cw, ch * level, fc=C(S.WATER), ec="none", zorder=4))
    ax.plot([cx - cw / 2, cx - cw / 2, cx + cw / 2, cx + cw / 2], [y0 + ch, y0, y0, y0 + ch],
            color=C(S.INK), lw=3, zorder=5)
    return y0 + ch


def stopwatch(ax, cx, cy, r=0.42):
    D.box(ax, cx - 0.09, cy + r - 0.02, 0.18, 0.16, fc=S.INK, r=0.03, z=6)
    ax.add_patch(Circle((cx, cy), r, fc="white", ec=C(S.INK), lw=3, zorder=6))
    ax.plot([cx, cx + r * 0.55], [cy, cy + r * 0.45], color=C(S.RESIST), lw=3, zorder=7,
            solid_capstyle="round")
    ax.add_patch(Circle((cx, cy), 0.05, fc=C(S.INK), zorder=8))


def current():
    w, h = S.FIG_SPLIT
    fig, ax = D.new_fig(w, h)
    stopwatch(ax, 3.6, 4.55)
    D.text(ax, 3.6, 3.75, "1초 동안", size=15, weight="bold")

    for cx, n, level, tag, fc in ((1.95, 3, 0.25, "전류 작음", "8FD0EC"),
                                  (5.65, 9, 0.8, "전류 큼", S.CURRENT)):
        y_out = faucet(ax, cx)
        y_cup = cup(ax, cx, level)
        span = y_out - y_cup - 0.25
        if n > 5:
            ax.plot([cx, cx], [y_out, y_cup - 0.1], color=C(S.WATER), lw=10, zorder=3, alpha=0.7)
        for i in range(n):
            yy = y_out - 0.25 - i * span / max(n - 1, 1)
            D.drop(ax, cx + (0.12 if n > 5 and i % 2 else 0) - (0.12 if n > 5 and not i % 2 else 0),
                   yy, s=0.11)
        D.pill(ax, cx, 0.45, tag, fc=fc, tc=S.INK if fc == "8FD0EC" else "FFFFFF", size=16)
    D.save(fig, "02_current")


# ── 02_resistance ───────────────────────────────
def narrow_pipe(ax, x1, x2, y, d_wide, d_narrow, n1, n2):
    """양 끝은 넓고 가운데(n1~n2)가 좁은 관."""
    tw = 0.25
    top = [(x1, y + d_wide / 2), (n1 - tw, y + d_wide / 2), (n1 + tw, y + d_narrow / 2),
           (n2 - tw, y + d_narrow / 2), (n2 + tw, y + d_wide / 2), (x2, y + d_wide / 2)]
    bot = [(px, 2 * y - py) for px, py in top]
    ax.add_patch(Polygon(top + bot[::-1], closed=True, fc=C(S.WATER), ec="none", zorder=4))
    D.wire(ax, top, lw=3, z=5)
    D.wire(ax, bot, lw=3, z=5)


def resistance():
    w, h = S.FIG_SPLIT
    fig, ax = D.new_fig(w, h)
    x1, x2, dw = 0.4, 6.1, 0.95
    # 넓은 관
    yt = 3.65
    D.pipe(ax, x1, x2, yt, d=dw)
    for x in (1.0, 2.6, 4.2):
        D.arrow(ax, x, yt, x + 1.0, yt, color="FFFFFF", lw=7, head=22)
    D.pill(ax, 3.25, 4.65, "넓은 관 = 저항 작음", fc=S.INK_SOFT, size=16)
    D.text(ax, 6.65, yt, "콸콸", size=17, weight="bold", color=S.WATER_DARK)

    # 좁은 관
    yb, n1, n2 = 1.35, 2.4, 4.1
    D.box(ax, n1 - 0.3, yb - dw / 2 - 0.15, n2 - n1 + 0.6, dw + 0.3, fc=S.RESIST, r=0.12, z=2, alpha=0.18)
    narrow_pipe(ax, x1, x2, yb, dw, 0.28, n1, n2)
    for x in (0.9, 4.6):
        D.arrow(ax, x, yb, x + 0.8, yb, color="FFFFFF", lw=2.5, head=11)
    D.arrow(ax, n1 + 0.4, yb, n2 - 0.4, yb, color="FFFFFF", lw=2, head=9)
    D.pill(ax, 3.25, 2.5, "좁은 관 = 저항 큼", fc=S.RESIST, size=16)
    D.text(ax, 6.65, yb, "졸졸", size=17, weight="bold", color=S.INK_SOFT)
    D.text(ax, 3.25, 0.35, "관이 좁을수록 물(전류)이 적게 흐른다", size=15, color=S.INK_SOFT)
    D.save(fig, "02_resistance")


def main():
    water_vs_circuit()
    voltage()
    current()
    resistance()


if __name__ == "__main__":
    main()
