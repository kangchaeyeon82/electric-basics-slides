"""섹션 5 — 전력과 전기요금 그림."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))
import draw_helpers as D  # noqa: E402
import style as S  # noqa: E402
from matplotlib.patches import Circle  # noqa: E402

C = D.C


# ── 로컬 아이콘 ────────────────────────────────────
def microwave(ax, cx, cy):
    D.box(ax, cx - 0.7, cy - 0.45, 1.4, 0.9, fc="FFFFFF", ec=S.INK, lw=3, r=0.1, z=5)
    D.box(ax, cx - 0.58, cy - 0.33, 0.85, 0.66, fc=S.INK_SOFT, r=0.06, z=6)
    for dy in (0.18, -0.02):
        ax.add_patch(Circle((cx + 0.47, cy + dy), 0.07, fc=C(S.INK), ec="none", zorder=6))
    D.box(ax, cx + 0.37, cy - 0.32, 0.2, 0.1, fc=S.RESIST, r=0.02, z=6)


def tv(ax, cx, cy):
    D.box(ax, cx - 0.7, cy - 0.3, 1.4, 0.85, fc=S.CURRENT, ec=S.INK, lw=3, r=0.08, z=5)
    ax.plot([cx, cx], [cy - 0.3, cy - 0.5], color=C(S.INK), lw=4, zorder=4)
    ax.plot([cx - 0.35, cx + 0.35], [cy - 0.5, cy - 0.5], color=C(S.INK), lw=4,
            solid_capstyle="round", zorder=4)


def clock(ax, cx, cy, r=0.48, hours=1):
    ax.add_patch(Circle((cx, cy), r, fc="#FFFFFF", ec=C(S.INK), lw=3, zorder=5))
    for i in range(12):
        a = math.radians(i * 30)
        ax.plot([cx + r * 0.78 * math.sin(a), cx + r * 0.9 * math.sin(a)],
                [cy + r * 0.78 * math.cos(a), cy + r * 0.9 * math.cos(a)],
                color=C(S.INK_SOFT), lw=1.8, zorder=6)
    # 지나간 시간 부채꼴
    from matplotlib.patches import Wedge
    ang = min(hours, 12) * 30
    ax.add_patch(Wedge((cx, cy), r * 0.72, 90 - ang, 90, fc=C(S.SPARK), ec="none", alpha=0.6, zorder=5))
    ax.plot([cx, cx], [cy, cy + r * 0.62], color=C(S.INK), lw=3, solid_capstyle="round", zorder=7)
    a = math.radians(ang)
    ax.plot([cx, cx + r * 0.45 * math.sin(a)], [cy, cy + r * 0.45 * math.cos(a)],
            color=C(S.INK), lw=4, solid_capstyle="round", zorder=7)
    ax.add_patch(Circle((cx, cy), 0.05, fc=C(S.INK), ec="none", zorder=8))


def bill(ax, cx, cy):
    D.box(ax, cx - 0.75, cy - 1.0, 1.5, 2.0, fc="FFFFFF", ec=S.INK, lw=3, r=0.1, z=5)
    D.text(ax, cx, cy + 0.68, "전기요금", size=15, weight="bold")
    for k in range(3):
        y = cy + 0.3 - k * 0.25
        ax.plot([cx - 0.5, cx + 0.5 - (0.25 if k == 2 else 0)], [y, y], color=C(S.LINE), lw=4,
                solid_capstyle="round", zorder=6)
    D.pill(ax, cx, cy - 0.55, "kWh", fc=S.SPARK, tc=S.INK, size=16)


# ── 05_power ──────────────────────────────────────
def fig_power():
    W, H = S.FIG_SPLIT
    fig, ax = D.new_fig(W, H)
    y = 4.8
    D.pill(ax, 1.0, y, "전력 W", fc=S.SPARK, tc=S.INK, size=17)
    D.text(ax, 2.1, y, "=", size=26, color=S.INK_SOFT, weight="bold")
    D.pill(ax, 3.3, y, "전압 V", fc=S.VOLT, size=17)
    D.text(ax, 4.5, y, "×", size=26, color=S.INK_SOFT, weight="bold")
    D.pill(ax, 5.7, y, "전류 A", fc=S.CURRENT, size=17)

    for cx, b, watt, desc, fc, tc in ((1.9, 0.3, "10W", "은은하게 · 전기 조금", S.INK_SOFT, S.PAPER),
                                      (5.3, 1.0, "60W", "환하게 · 전기 많이", S.SPARK, S.INK)):
        D.bulb(ax, cx, 2.6, r=0.6, lit=True, brightness=b)
        D.pill(ax, cx, 1.15, watt, fc=fc, tc=tc, size=20)
        D.text(ax, cx, 0.45, desc, size=15, color=S.INK_SOFT)
    D.save(fig, "05_power")


# ── 05_kwh ────────────────────────────────────────
def kwh_row(ax, y, icon, watt, hours, hours_txt):
    D.box(ax, 0.2, y - 0.95, 9.3, 1.9, fc=S.PANEL, r=0.25, z=0)
    icon(ax, 1.15, y + 0.05)
    D.text(ax, 2.75, y, watt, size=26, weight="bold")
    D.text(ax, 3.9, y, "×", size=30, color=S.INK_SOFT, weight="bold")
    clock(ax, 4.8, y, hours=hours)
    D.text(ax, 6.0, y, hours_txt, size=24, weight="bold")
    D.text(ax, 7.05, y, "=", size=30, color=S.INK_SOFT, weight="bold")
    D.pill(ax, 8.3, y, "1 kWh", fc=S.SPARK, tc=S.INK, size=26)


def fig_kwh():
    W, H = S.FIG_FULL
    fig, ax = D.new_fig(W, H)
    kwh_row(ax, 3.65, microwave, "1,000W", 1, "1시간")
    kwh_row(ax, 1.25, tv, "100W", 10, "10시간")
    bill(ax, 10.8, 2.75)
    D.text(ax, 10.8, 1.25, "둘 다 같은 요금", size=16, weight="bold", color=S.INK)
    D.text(ax, 10.8, 0.8, "(1kWh 만큼)", size=14, color=S.INK_SOFT)
    D.save(fig, "05_kwh")


def main():
    fig_power()
    fig_kwh()


if __name__ == "__main__":
    main()
