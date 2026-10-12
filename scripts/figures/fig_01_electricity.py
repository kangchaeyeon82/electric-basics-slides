"""섹션 1. 전기의 정체 — 원자, 전선 속 전자, 도체/부도체."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))
import draw_helpers as D  # noqa: E402
import style as S  # noqa: E402
from matplotlib.patches import Circle, Ellipse  # noqa: E402

C = S.mpl


def nucleon(ax, x, y, r, plus=True):
    fc = S.RESIST if plus else "B8BECB"
    ax.add_patch(Circle((x, y), r, fc=C(fc), ec="white", lw=1.5, zorder=8))
    if plus:
        D.text(ax, x, y + 0.01, "+", size=r * 80, color="FFFFFF", weight="bold", zorder=9)


def nucleus(ax, cx, cy, r=0.17):
    # 꽃 모양 배치 (가운데 1 + 둘레 6, 서로 맞닿게)
    nucleon(ax, cx, cy, r, True)
    for i in range(6):
        a = math.radians(90 + i * 60)
        nucleon(ax, cx + 2 * r * math.cos(a), cy + 2 * r * math.sin(a), r, i % 2 == 0)


# ── 01_atom ─────────────────────────────────────
def atom():
    w, h = S.FIG_SPLIT
    fig, ax = D.new_fig(w, h)
    cx, cy = 2.65, 2.75
    for R in (1.15, 2.0):
        ax.add_patch(Circle((cx, cy), R, fc="none", ec=C(S.LINE), lw=2.5, zorder=2))
    nucleus(ax, cx, cy, r=0.2)
    for ang in (30, 210):
        a = math.radians(ang)
        D.electron(ax, cx + 1.15 * math.cos(a), cy + 1.15 * math.sin(a), r=0.17)
    for ang in (100, 175, 250, 320):
        a = math.radians(ang)
        D.electron(ax, cx + 2.0 * math.cos(a), cy + 2.0 * math.sin(a), r=0.17)

    # 떨어져 나가는 전자
    a = math.radians(38)
    sx, sy = cx + 2.0 * math.cos(a), cy + 2.0 * math.sin(a)
    ex, ey = 5.9, 4.55
    ax.add_patch(Circle((sx, sy), 0.17, fc="none", ec=C(S.CURRENT), lw=2, ls="--", zorder=6))
    D.arrow(ax, sx + 0.2, sy + 0.1, ex - 0.25, ey - 0.08, color=S.CURRENT, lw=3, rad=-0.2)
    D.electron(ax, ex, ey, r=0.2)
    D.text(ax, 5.85, 3.95, "떨어져 나온 전자", size=15, color=S.CURRENT, weight="bold")
    D.text(ax, 5.85, 3.55, "→ 이것이 움직이면 전기!", size=14, color=S.INK_SOFT)

    # 범례
    lx, ly = 5.0, 1.75
    nucleon(ax, lx, ly, 0.17, True)
    D.text(ax, lx + 0.32, ly, "양성자 (+)", size=15, ha="left")
    nucleon(ax, lx, ly - 0.55, 0.17, False)
    D.text(ax, lx + 0.32, ly - 0.55, "중성자", size=15, ha="left")
    D.electron(ax, lx, ly - 1.1, r=0.17)
    D.text(ax, lx + 0.32, ly - 1.1, "전자 (−)", size=15, ha="left")
    D.save(fig, "01_atom")


# ── 01_wire_electrons ───────────────────────────
def wire_electrons():
    w, h = S.FIG_FULL
    fig, ax = D.new_fig(w, h)
    yc = 2.45
    x1, x2 = 2.4, 9.4
    # 전구 (왼쪽)
    l_pt, r_pt = D.bulb(ax, 1.15, 3.55, r=0.42, lit=True)
    # 건전지 (오른쪽, + 가 위)
    top, bot = D.battery(ax, 10.9, 1.6, w=1.6, h=0.75, label="1.5V", vertical=True)
    # 일반 전선
    D.wire(ax, [r_pt, (r_pt[0], yc), (x1, yc)], lw=6)
    D.wire(ax, [(x2, yc), (top[0], yc), top], lw=6)
    D.wire(ax, [bot, (bot[0], 0.5), (l_pt[0], 0.5), l_pt], lw=6)
    D.electrons_along(ax, [bot, (bot[0], 0.5), (l_pt[0], 0.5), (l_pt[0], 2.0)], 9, r=0.08)

    # 단면으로 본 전선
    ins_h, core_h = 1.25, 0.72
    D.box(ax, x1, yc - ins_h / 2, x2 - x1, ins_h, fc="D5DAE5", ec=S.INK_SOFT, lw=2, r=0.25, z=4)
    D.box(ax, x1 + 0.05, yc - core_h / 2, x2 - x1 - 0.1, core_h, fc="F2C9A2", ec=S.COPPER, lw=2, r=0.12, z=5)
    n = 9
    for i in range(n):
        x = x1 + 0.55 + i * (x2 - x1 - 1.1) / (n - 1)
        D.electron(ax, x, yc, r=0.2)
        if i < n - 1:
            step = (x2 - x1 - 1.1) / (n - 1)
            D.arrow(ax, x + 0.25, yc, x + step - 0.27, yc, color=S.CURRENT, lw=2.5, head=12)

    # 위쪽 큰 화살표 + 이름표
    D.arrow(ax, 3.4, 3.55, 8.4, 3.55, color=S.CURRENT, lw=5, head=22)
    D.pill(ax, 5.9, 4.15, "전자의 이동", fc=S.CURRENT, size=17)

    # 구조 이름
    D.wire(ax, [(4.0, yc - 0.2), (4.0, 1.25)], color=S.COPPER, lw=2)
    D.text(ax, 4.0, 1.0, "구리선 (속)", size=15, color=S.COPPER, weight="bold")
    D.wire(ax, [(7.6, yc - ins_h / 2 + 0.05), (7.6, 1.25)], color=S.INK_SOFT, lw=2)
    D.text(ax, 7.6, 1.0, "피복 (겉)", size=15, color=S.INK_SOFT, weight="bold")
    D.text(ax, 10.9, 3.0, "건전지", size=15, weight="bold")
    D.save(fig, "01_wire_electrons")


# ── 01_conductors ───────────────────────────────
def lattice_panel(ax, x0, w, head, color, free, caption, examples):
    D.box(ax, x0, 0.2, w, 4.5, fc=S.PANEL, r=0.25)
    D.pill(ax, x0 + w / 2, 4.2, head, fc=color, size=18)
    cols, rows = 4, 3
    gx0, gy0, gdx, gdy = x0 + 0.75, 1.85, (w - 1.5) / (cols - 1), 0.75
    for i in range(cols):
        for j in range(rows):
            ax_ = gx0 + i * gdx
            ay_ = gy0 + j * gdy
            ax.add_patch(Circle((ax_, ay_), 0.24, fc=C("C3C9D6"), ec="white", lw=1.5, zorder=5))
            D.text(ax, ax_, ay_ + 0.01, "+", size=15, color="FFFFFF", weight="bold", zorder=6)
            if not free:
                D.electron(ax, ax_ + 0.27, ay_ + 0.2, r=0.11, sign=False)
    if free:
        import random
        random.seed(3)
        for j in range(rows - 1):
            for k in range(cols):
                ex = gx0 - 0.2 + k * gdx + random.uniform(0.1, 0.5)
                ey = gy0 + j * gdy + gdy / 2 + random.uniform(-0.08, 0.08)
                D.electron(ax, ex, ey, r=0.11, sign=False)
                D.arrow(ax, ex + 0.14, ey, ex + 0.45, ey, color=S.CURRENT, lw=2, head=10)
    D.text(ax, x0 + w / 2, 1.1, caption, size=16, weight="bold", color=color)
    D.text(ax, x0 + w / 2, 0.6, examples, size=15, color=S.INK_SOFT)


def conductors():
    w, h = S.FIG_FULL
    fig, ax = D.new_fig(w, h)
    lattice_panel(ax, 0.15, 4.55, "도체", S.CURRENT, True, "전자가 자유롭게 이동", "구리 · 알루미늄 · 금")
    lattice_panel(ax, 4.95, 4.55, "부도체 (절연체)", S.RESIST, False, "전자가 원자에 묶여 있음",
                  "고무 · 플라스틱 · 유리")
    # 전선 단면
    cx, cy = 10.75, 2.75
    D.pill(ax, cx, 4.2, "전선 단면", fc=S.INK, size=16)
    ax.add_patch(Circle((cx, cy), 0.85, fc=C(S.INK_SOFT), ec=C(S.INK), lw=2, zorder=4))
    ax.add_patch(Circle((cx, cy), 0.5, fc=C("F2C9A2"), ec=C(S.COPPER), lw=2, zorder=5))
    for ang in range(0, 360, 60):
        a = math.radians(ang)
        ax.add_patch(Circle((cx + 0.27 * math.cos(a), cy + 0.27 * math.sin(a)), 0.13,
                            fc=C(S.COPPER), ec="white", lw=1, zorder=6))
    ax.add_patch(Circle((cx, cy), 0.13, fc=C(S.COPPER), ec="white", lw=1, zorder=6))
    D.text(ax, cx, 1.35, "속 : 구리 (도체)", size=15, color=S.COPPER, weight="bold")
    D.text(ax, cx, 0.85, "겉 : 피복 (부도체)", size=15, color=S.INK_SOFT, weight="bold")
    D.save(fig, "01_conductors")


def main():
    atom()
    wire_electrons()
    conductors()


if __name__ == "__main__":
    main()
