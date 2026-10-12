"""섹션 6 — 직류와 교류 그림."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))
import draw_helpers as D  # noqa: E402
import style as S  # noqa: E402
from matplotlib.patches import Circle  # noqa: E402

C = D.C


# ── 로컬 아이콘 ────────────────────────────────────
def outlet(ax, cx, cy, s=1.0):
    D.box(ax, cx - 0.5 * s, cy - 0.5 * s, s, s, fc="FFFFFF", ec=S.INK, lw=3, r=0.15 * s, z=5)
    ax.add_patch(Circle((cx, cy), 0.33 * s, fc=C(S.PANEL), ec=C(S.INK), lw=2.5, zorder=6))
    for dx in (-0.13, 0.13):
        ax.add_patch(Circle((cx + dx * s, cy), 0.065 * s, fc=C(S.INK), ec="none", zorder=7))


def phone(ax, cx, cy):
    D.box(ax, cx - 0.5, cy - 0.95, 1.0, 1.9, fc=S.INK, r=0.15, z=5)
    D.box(ax, cx - 0.4, cy - 0.75, 0.8, 1.55, fc="DFF2FB", r=0.06, z=6)
    D.bolt(ax, cx, cy + 0.02, h=0.75, color=S.SPARK, z=7, ec=S.INK)
    ax.plot([cx - 0.12, cx + 0.12], [cy - 0.85, cy - 0.85], color=C(S.INK_SOFT), lw=3,
            solid_capstyle="round", zorder=7)


def adapter(ax, cx, cy):
    for dy in (0.25, -0.25):
        D.box(ax, cx - 1.05, cy + dy - 0.06, 0.35, 0.12, fc=S.METAL, r=0.03, z=4)
    D.box(ax, cx - 0.75, cy - 0.75, 1.5, 1.5, fc="FFFFFF", ec=S.INK, lw=3, r=0.2, z=5)
    D.box(ax, cx - 0.42, cy - 0.42, 0.84, 0.84, fc=S.PANEL, r=0.1, z=6)
    D.bolt(ax, cx, cy, h=0.6, color=S.SPARK, z=7, ec=S.INK)


def mini_wave(ax, x0, x1, yc, amp, kind, color=S.CURRENT, lw=3.5):
    n = 120
    xs = [x0 + (x1 - x0) * i / n for i in range(n + 1)]
    if kind == "ac":
        ys = [yc + amp * math.sin(2 * math.pi * 2 * i / n) for i in range(n + 1)]
    else:
        ys = [yc + amp for _ in xs]
    ax.plot([x0, x1], [yc, yc], color=C(S.LINE), lw=1.5, zorder=3)
    ax.plot(xs, ys, color=C(color), lw=lw, solid_capstyle="round", zorder=4)


# ── 06_dc_ac ──────────────────────────────────────
def wave_panel(ax, px, kind):
    D.box(ax, px, 0.15, 5.7, 4.6, fc=S.PANEL, r=0.25, z=0)
    if kind == "dc":
        D.battery(ax, px + 1.15, 4.1, w=1.1, h=0.5, label=None)
        D.pill(ax, px + 3.3, 4.1, "직류  DC", fc=S.INK, size=18)
        caption = "한 방향으로 · 일정하게"
    else:
        outlet(ax, px + 1.15, 4.05, s=0.75)
        D.pill(ax, px + 3.3, 4.1, "교류  AC", fc=S.INK, size=18)
        caption = "1초에 60번 방향이 바뀜 (60Hz)"
    gx0, gx1, y0, amp = px + 0.9, px + 5.2, 2.15, 0.85
    # 축
    ax.plot([gx0, gx0], [y0 - amp - 0.25, y0 + amp + 0.25], color=C(S.INK_SOFT), lw=2, zorder=3)
    D.arrow(ax, gx0, y0, gx1 + 0.2, y0, color=S.INK_SOFT, lw=2, head=12, z=3)
    D.text(ax, gx1 + 0.2, y0 - 0.3, "시간 →", size=14, color=S.INK_SOFT, ha="right")
    D.text(ax, gx0 - 0.3, y0 + amp, "+", size=20, weight="bold", color=S.RESIST)
    D.text(ax, gx0 - 0.3, y0 - amp, "−", size=20, weight="bold", color=S.INK_SOFT)
    n = 300
    xs = [gx0 + (gx1 - gx0 - 0.9) * i / n for i in range(n + 1)]
    if kind == "dc":
        ys = [y0 + amp * 0.85 for _ in xs]
    else:
        ys = [y0 + amp * math.sin(2 * math.pi * 3 * i / n) for i in range(n + 1)]
    ax.plot(xs, ys, color=C(S.CURRENT), lw=5, solid_capstyle="round", zorder=5)
    D.text(ax, px + 2.85, 0.6, caption, size=16, weight="bold")


def fig_dc_ac():
    W, H = S.FIG_FULL
    fig, ax = D.new_fig(W, H)
    wave_panel(ax, 0.2, "dc")
    wave_panel(ax, 6.1, "ac")
    D.save(fig, "06_dc_ac")


# ── 06_adapter ────────────────────────────────────
def fig_adapter():
    W, H = S.FIG_FULL
    fig, ax = D.new_fig(W, H)
    yc = 2.55
    xs = (1.6, 6.0, 10.4)
    for x, name in zip(xs, ("콘센트", "어댑터 (충전기)", "휴대폰")):
        D.text(ax, x, 4.4, name, size=18, weight="bold")
    outlet(ax, xs[0], yc, s=1.5)
    adapter(ax, xs[1], yc)
    phone(ax, xs[2], yc)
    D.pill(ax, xs[0], 0.75, "교류 AC · 220V", fc=S.VOLT, size=16)
    D.pill(ax, xs[1], 0.75, "220V → 5V · AC → DC", fc=S.INK, size=16)
    D.pill(ax, xs[2], 0.75, "직류 DC · 5V", fc=S.CURRENT, size=16)
    # 화살표 + 작은 파형
    D.big_arrow(ax, 2.75, yc, 4.85, yc, color=S.LINE, width=0.3)
    D.big_arrow(ax, 7.15, yc, 9.25, yc, color=S.LINE, width=0.3)
    mini_wave(ax, 2.85, 4.6, 3.35, 0.28, "ac", color=S.VOLT)
    mini_wave(ax, 7.25, 9.0, 3.2, 0.28, "dc", color=S.CURRENT)
    D.save(fig, "06_adapter")


def main():
    fig_dc_ac()
    fig_adapter()


if __name__ == "__main__":
    main()
