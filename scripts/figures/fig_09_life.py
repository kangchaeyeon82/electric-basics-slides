"""섹션 9 — 휴대폰 충전기 속 5단계 흐름도."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))
import draw_helpers as D  # noqa: E402
import style as S  # noqa: E402
from matplotlib.patches import Circle, Polygon  # noqa: E402

C = S.mpl

CARD_W, GAP = 1.8, 0.38
CARD_Y0, CARD_Y1 = 0.3, 4.6


# ── 단계별 파형 ────────────────────────────────────
def wave(kind, t):
    s = math.sin(t)
    if kind == "ac_big":
        return 0.55 * s
    if kind == "ac_small":
        return 0.25 * s
    if kind == "rect":
        return 0.3 * abs(s)
    if kind == "smooth":
        ph = (t % math.pi) / math.pi
        return 0.3 - 0.06 * ph
    return 0.3  # flat


def mini_graph(ax, x, y, w, h, kind, color):
    """(x, y) = 그래프 영역 왼쪽 아래. 가운데 점선이 0V."""
    D.box(ax, x, y, w, h, fc="FFFFFF", r=0.08, z=2)
    zero = y + h / 2
    ax.plot([x + 0.08, x + w - 0.08], [zero, zero], color=C(S.LINE), lw=1.5, ls=(0, (3, 2)), zorder=3)
    n = 160
    xs = [x + 0.12 + (w - 0.24) * i / n for i in range(n + 1)]
    ys = [zero + wave(kind, 4 * math.pi * i / n) * (h / 1.3) for i in range(n + 1)]
    ax.plot(xs, ys, color=C(color), lw=3, zorder=4, solid_capstyle="round")


# ── 단계별 아이콘 ──────────────────────────────────
def icon_outlet(ax, cx, cy):
    D.box(ax, cx - 0.36, cy - 0.36, 0.72, 0.72, fc="FFFFFF", ec=S.INK, lw=2.5, r=0.14, z=5)
    for dx in (-0.14, 0.14):
        ax.add_patch(Circle((cx + dx, cy), 0.07, fc=C(S.INK), zorder=6))


def icon_transformer(ax, cx, cy):
    for dx in (-0.2, 0.2):
        for k in range(4):
            ax.add_patch(Circle((cx + dx, cy - 0.27 + k * 0.18), 0.09, fc="none", ec=C(S.COPPER), lw=2.5,
                                zorder=5))
    for dx in (-0.03, 0.03):
        ax.plot([cx + dx, cx + dx], [cy - 0.38, cy + 0.38], color=C(S.INK), lw=2, zorder=5)


def icon_diode(ax, cx, cy):
    s = 0.22
    ax.plot([cx - 0.42, cx + 0.42], [cy, cy], color=C(S.INK), lw=2.5, zorder=4)
    ax.add_patch(Polygon([(cx - s, cy + s), (cx - s, cy - s), (cx + s * 0.8, cy)], fc=C(S.INK), zorder=5))
    ax.plot([cx + s * 0.8] * 2, [cy - s, cy + s], color=C(S.INK), lw=3, zorder=5)


def icon_capacitor(ax, cx, cy):
    D.box(ax, cx - 0.22, cy - 0.32, 0.44, 0.64, fc="2D6FB7", r=0.05, z=5)
    D.box(ax, cx + 0.08, cy - 0.32, 0.14, 0.64, fc="A9C8EA", r=0.0, z=6)
    D.box(ax, cx - 0.22, cy + 0.26, 0.44, 0.06, fc=S.METAL, r=0.0, z=7)
    for dx in (-0.1, 0.1):
        ax.plot([cx + dx, cx + dx], [cy - 0.32, cy - 0.45], color=C(S.METAL), lw=2.5, zorder=4)


def icon_transistor(ax, cx, cy):
    ax.add_patch(Polygon([(cx - 0.25, cy - 0.15), (cx + 0.25, cy - 0.15), (cx + 0.25, cy + 0.22),
                          (cx + 0.15, cy + 0.32), (cx - 0.15, cy + 0.32), (cx - 0.25, cy + 0.22)],
                         fc=C(S.INK), zorder=5))
    for dx in (-0.14, 0, 0.14):
        ax.plot([cx + dx, cx + dx], [cy - 0.15, cy - 0.42], color=C(S.METAL), lw=2.5, zorder=4)


def phone(ax, x, y, w=0.8, h=1.5):
    D.box(ax, x, y, w, h, fc=S.INK, r=0.14, z=5)
    D.box(ax, x + 0.07, y + 0.15, w - 0.14, h - 0.3, fc="E8F6EE", r=0.06, z=6)
    D.bolt(ax, x + w / 2, y + h / 2, h=0.6, color=S.SAFE, z=7)


STAGES = [
    ("① 콘센트", icon_outlet, "ac_big", S.VOLT, "교류 220V", "방향이 바뀜"),
    ("② 변압기", icon_transformer, "ac_small", S.VOLT, "전압 낮추기", "높게 → 낮게"),
    ("③ 다이오드", icon_diode, "rect", S.CURRENT, "한 방향으로", "교류 → 직류"),
    ("④ 커패시터", icon_capacitor, "smooth", S.CURRENT, "매끈하게", "울퉁불퉁 다듬기"),
    ("⑤ 트랜지스터", icon_transistor, "flat", S.SAFE, "딱 5V 유지", "일정하게 조절"),
]


def charger():
    W, H = S.FIG_FULL
    fig, ax = D.new_fig(W, H)
    for i, (title, icon, kind, color, line1, line2) in enumerate(STAGES):
        x = 0.1 + i * (CARD_W + GAP)
        cx = x + CARD_W / 2
        D.box(ax, x, CARD_Y0, CARD_W, CARD_Y1 - CARD_Y0, fc=S.PANEL, r=0.2, z=1)
        D.text(ax, cx, 4.22, title, size=15, weight="bold")
        icon(ax, cx, 3.4)
        mini_graph(ax, x + 0.15, 1.6, CARD_W - 0.3, 1.2, kind, color)
        D.text(ax, cx, 1.08, line1, size=15, weight="bold", color=color)
        D.text(ax, cx, 0.66, line2, size=14, color=S.INK_SOFT)
        D.big_arrow(ax, x + CARD_W + 0.05, 2.45, x + CARD_W + GAP - 0.05, 2.45, color=S.INK_SOFT, width=0.14)

    px = 0.1 + 5 * (CARD_W + GAP) + 0.05
    phone(ax, px, 1.75, w=0.8, h=1.5)
    D.text(ax, px + 0.4, 1.3, "휴대폰", size=15, weight="bold")
    D.text(ax, px + 0.4, 0.9, "직류 5V", size=14, color=S.SAFE, weight="bold")
    D.save(fig, "09_charger")


def main():
    charger()


if __name__ == "__main__":
    main()
