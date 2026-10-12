"""섹션 8 — 전기 안전 그림 (감전 경로, 누전차단기)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))
import draw_helpers as D  # noqa: E402
import style as S  # noqa: E402
from matplotlib.patches import Circle  # noqa: E402

C = S.mpl


def dashed_path(ax, pts, color=S.RESIST, lw=4):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=C(color), lw=lw, ls=(0, (2.5, 1.6)), solid_capstyle="round", zorder=15)


def ground_symbol(ax, x, y, w=0.6, color=S.INK):
    """접지 기호 (x, y = 맨 위 선 가운데)."""
    for i, k in enumerate((1.0, 0.65, 0.3)):
        yy = y - i * 0.12
        ax.plot([x - w / 2 * k, x + w / 2 * k], [yy, yy], color=C(color), lw=3.5, solid_capstyle="round",
                zorder=8)


# ── 1. 감전 경로 ───────────────────────────────────
def shock():
    W, H = S.FIG_SPLIT
    fig, ax = D.new_fig(W, H)
    gy = 1.0  # 땅 높이

    # 땅
    D.box(ax, 0.2, gy - 0.35, 6.8, 0.35, fc="E7E1D6", r=0.06, z=1)
    ax.plot([0.2, 7.0], [gy, gy], color=C("9C8E76"), lw=3, zorder=2)

    # 사람 (오른쪽, 팔을 왼쪽으로 뻗음)
    px, ph = 4.6, 3.3
    col = S.INK_SOFT
    head_r = ph * 0.11
    ax.add_patch(Circle((px, gy + ph - head_r), head_r, fc=C(col), ec="none", zorder=6))
    D.box(ax, px - ph * 0.14, gy + ph * 0.38, ph * 0.28, ph * 0.38, fc=col, r=ph * 0.08, z=6)
    for dx in (-0.06, 0.06):
        D.box(ax, px + dx * ph - ph * 0.05, gy, ph * 0.1, ph * 0.43, fc=col, r=ph * 0.04, z=6)
    shoulder = (px - ph * 0.08, gy + ph * 0.7)
    hand = (2.75, gy + ph * 0.82)
    ax.plot([shoulder[0], hand[0]], [shoulder[1], hand[1]], color=C(col), lw=15, solid_capstyle="round",
            zorder=6)
    # 반대쪽 팔 (아래로)
    ax.plot([px + ph * 0.1, px + ph * 0.2], [gy + ph * 0.7, gy + ph * 0.45], color=C(col), lw=15,
            solid_capstyle="round", zorder=5)

    # 피복이 벗겨진 전선 (위에서 내려옴)
    wy = hand[1] + 0.05
    D.wire(ax, [(0.4, 4.9), (0.9, wy), (2.2, wy)], color="3A3F4F", lw=12, z=7)
    D.wire(ax, [(2.2, wy), (3.0, wy)], color=S.COPPER, lw=6, z=7)
    D.wire(ax, [(3.0, wy), (3.25, wy)], color="3A3F4F", lw=12, z=7)
    D.bolt(ax, 2.45, wy + 0.55, h=0.65, color=S.SPARK, z=9)
    D.text(ax, 1.55, wy + 0.42, "벗겨진 전선", size=14, weight="bold", color=S.INK_SOFT)

    # 전류 경로 (손 → 어깨 → 몸 → 다리 → 땅)
    path = [(hand[0] + 0.1, hand[1] - 0.18), (shoulder[0], shoulder[1] - 0.15), (px - 0.05, gy + ph * 0.42),
            (px - 0.2, gy + 0.15)]
    dashed_path(ax, path)
    D.arrow(ax, px - 0.2, gy + 0.6, px - 0.2, gy + 0.2, color=S.RESIST, lw=4, head=14, z=16)
    D.arrow(ax, 3.3, hand[1] - 0.12, 3.6, hand[1] - 0.17, color=S.RESIST, lw=4, head=14, z=16)
    ground_symbol(ax, px - 0.2, gy - 0.45)

    # 설명
    D.text(ax, 5.9, 4.8, "몸이 전기의", size=17, weight="bold", color=S.RESIST)
    D.text(ax, 5.9, 4.38, "길이 됨", size=17, weight="bold", color=S.RESIST)
    D.text(ax, 6.05, 1.5, "땅으로", size=14, color=S.INK_SOFT, weight="bold")
    D.text(ax, 6.05, 1.18, "빠져나감", size=14, color=S.INK_SOFT, weight="bold")
    D.text(ax, 2.25, 0.35, "젖은 손·젖은 바닥은 더 위험!", size=14, color=S.RESIST, weight="bold")
    D.drop(ax, 0.8, 0.3, s=0.1)
    D.save(fig, "08_shock")


# ── 2. 누전차단기 ──────────────────────────────────
def breaker_box(ax, x, y, on=True):
    """누전차단기 (x, y = 왼쪽 아래, 1.2 x 2.2)."""
    w, h = 1.2, 2.2
    D.box(ax, x, y, w, h, fc="FFFFFF", ec=S.INK, lw=2.5, r=0.12, z=6)
    D.box(ax, x + 0.35, y + 0.9, 0.5, 0.9, fc=S.PANEL, ec=S.INK_SOFT, lw=1.5, r=0.06, z=7)
    lever_y = y + 1.45 if on else y + 0.95
    D.box(ax, x + 0.4, lever_y, 0.4, 0.3, fc=S.SAFE if on else S.RESIST, r=0.05, z=8)
    D.text(ax, x + 0.6, y + 2.0, "ON" if on else "OFF", size=13, weight="bold",
           color=S.SAFE if on else S.RESIST)
    ax.add_patch(Circle((x + 0.6, y + 0.45), 0.13, fc=C(S.SPARK), ec=C(S.INK), lw=1.5, zorder=8))
    D.text(ax, x + 0.6, y + 0.17, "TEST", size=11, weight="bold", color=S.INK_SOFT)
    return (x + w, y + 1.6), (x + w, y + 0.6)


def breaker_panel(ax, x0, leak):
    color = S.RESIST if leak else S.SAFE
    D.box(ax, x0, 0.1, 5.8, 4.7, fc=S.PANEL, r=0.25, z=0)
    D.pill(ax, x0 + 2.9, 4.4, "누전 발생" if leak else "정상", fc=color, size=17)

    bx, by = x0 + 0.35, 1.45
    D.text(ax, bx + 0.6, by + 2.45, "누전차단기", size=14, weight="bold", color=S.INK_SOFT)
    breaker_box(ax, bx, by, on=not leak)

    ax_l, ax_r = bx + 1.2, x0 + 4.3
    top_y, bot_y = by + 1.6, by + 0.6
    D.wire(ax, [(ax_l, top_y), (ax_r, top_y)], color=S.INK, lw=4)
    D.wire(ax, [(ax_l, bot_y), (ax_r, bot_y)], color=S.INK, lw=4)
    D.arrow(ax, ax_l + 0.9, top_y, ax_l + 1.6, top_y, color=S.CURRENT, lw=4, head=16)
    D.arrow(ax, ax_l + 1.6, bot_y, ax_l + 0.9, bot_y, color=S.CURRENT, lw=4, head=16)
    mid = (ax_l + ax_r) / 2
    D.text(ax, mid, top_y + 0.3, "들어간 전기 10A", size=14, weight="bold", color=S.INK)
    D.text(ax, mid, bot_y - 0.3, f"나온 전기 {'9.97A' if leak else '10A'}", size=14, weight="bold",
           color=S.RESIST if leak else S.INK)

    # 가전제품
    D.box(ax, ax_r, by + 0.25, 1.2, 1.7, fc="FFFFFF", ec=S.INK, lw=2.5, r=0.12, z=6)
    ax.add_patch(Circle((ax_r + 0.6, by + 1.0), 0.38, fc=C(S.PANEL), ec=C(S.INK_SOFT), lw=2, zorder=7))
    D.text(ax, ax_r + 0.6, by + 1.68, "가전제품", size=13, weight="bold", color=S.INK_SOFT)

    if leak:
        lx = ax_r + 0.6
        ax.plot([lx, lx], [by + 0.25, 0.85], color=C(S.RESIST), lw=4, ls=(0, (2.5, 1.6)), zorder=9)
        D.drop(ax, lx + 0.3, 0.95, s=0.12, color=S.WATER_DARK)
        ground_symbol(ax, lx, 0.78, w=0.5)
        D.text(ax, lx - 0.9, 1.0, "0.03A", size=14, weight="bold", color=S.RESIST)
        D.text(ax, lx - 0.9, 0.68, "새는 전기", size=13, color=S.RESIST)
        D.pill(ax, x0 + 1.75, 0.65, "10A ≠ 9.97A → 0.03초 만에 차단!", fc=S.RESIST, size=14)
    else:
        D.pill(ax, x0 + 2.3, 0.65, "10A = 10A → 그대로 사용", fc=S.SAFE, size=14)


def breaker():
    W, H = S.FIG_FULL
    fig, ax = D.new_fig(W, H)
    breaker_panel(ax, 0.1, leak=False)
    breaker_panel(ax, 6.1, leak=True)
    D.save(fig, "08_breaker")


def main():
    shock()
    breaker()


if __name__ == "__main__":
    main()
