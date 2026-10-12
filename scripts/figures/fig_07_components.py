"""섹션 7 — 전자 부품 5총사 그림.

모든 그림은 같은 구성 (split 7.2 x 5.3 in):
  위 왼쪽 = 실물 그림, 위 오른쪽 = 회로 기호, 아래 = 비유 그림
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))
import draw_helpers as D  # noqa: E402
import style as S  # noqa: E402
from matplotlib import transforms  # noqa: E402
from matplotlib.patches import Circle, Polygon, Wedge  # noqa: E402

C = S.mpl
W, H = S.FIG_SPLIT
SYM_Y = 3.85           # 회로 기호 중심 높이
SYM_X1, SYM_X2 = 4.6, 6.85


# ── 공통 틀 ────────────────────────────────────────
def pill_left(ax, x, y, s, fc, tc="FFFFFF", size=15):
    ax.text(x, y, s, fontsize=size, color=C(tc), fontweight="bold", ha="left", va="center", zorder=25,
            bbox=dict(boxstyle="round,pad=0.35", fc=C(fc), ec="none"))


def frame(color, analogy):
    fig, ax = D.new_fig(W, H)
    D.box(ax, 0.1, 2.95, 4.1, 2.25, fc=S.PANEL, r=0.2)
    D.box(ax, 4.35, 2.95, 2.75, 2.25, fc=S.PANEL, r=0.2)
    D.text(ax, 0.32, 4.95, "실물", size=14, color=S.INK_SOFT, weight="bold", ha="left")
    D.text(ax, 4.57, 4.95, "회로 기호", size=14, color=S.INK_SOFT, weight="bold", ha="left")
    D.box(ax, 0.1, 0.1, 7.0, 2.65, fc="FFFFFF", ec=S.LINE, lw=2, r=0.2)
    pill_left(ax, 0.32, 2.42, analogy, fc=color)
    return fig, ax


def leg(ax, x1, y1, x2, y2, lw=4):
    ax.plot([x1, x2], [y1, y2], color=C(S.METAL), lw=lw, solid_capstyle="round", zorder=3)


def sym_line(ax, x1, x2, y=SYM_Y):
    ax.plot([x1, x2], [y, y], color=C(S.INK), lw=3, solid_capstyle="round", zorder=5)


def diode_symbol(ax, cx, cy, s=0.42, color=S.INK, fill=True):
    """삼각형 + 막대 다이오드 기호 (오른쪽 방향)."""
    tri = Polygon([(cx - s, cy + s), (cx - s, cy - s), (cx + s * 0.75, cy)], closed=True,
                  fc=C(color) if fill else "white", ec=C(color), lw=3, zorder=6, joinstyle="round")
    ax.add_patch(tri)
    ax.plot([cx + s * 0.75] * 2, [cy - s, cy + s], color=C(color), lw=3.5, zorder=6)


def check(ax, x, y, ok=True, r=0.24):
    ax.add_patch(Circle((x, y), r, fc=C(S.SAFE if ok else S.RESIST), ec="none", zorder=20))
    ax.text(x, y, "✓" if ok else "✗", fontsize=17, color="white", ha="center", va="center",
            fontweight="bold", zorder=21, family="DejaVu Sans")


def pipe_profile(ax, x1, x2, y, dfun, n=120, z=4):
    """굵기가 x 에 따라 변하는 가로 파이프."""
    xs = [x1 + (x2 - x1) * i / n for i in range(n + 1)]
    top = [y + dfun(x) / 2 for x in xs]
    bot = [y - dfun(x) / 2 for x in xs]
    ax.fill_between(xs, bot, top, color=C(S.WATER), lw=0, zorder=z)
    ax.plot(xs, top, color=C(S.INK), lw=3, zorder=z + 1)
    ax.plot(xs, bot, color=C(S.INK), lw=3, zorder=z + 1)


# ── 1. 저항 ────────────────────────────────────────
def resistor():
    fig, ax = frame(S.RESIST, "비유: 좁은 관")
    cy = 3.95
    leg(ax, 0.4, cy, 3.9, cy)
    D.box(ax, 1.0, cy - 0.32, 2.2, 0.64, fc="E8D3A8", ec="B89A66", lw=2, r=0.25, z=4)
    for x, col in ((1.4, "8B4A1E"), (1.75, "1F2433"), (2.1, "E5533D"), (2.85, "D4A72C")):
        D.box(ax, x - 0.09, cy - 0.32, 0.18, 0.64, fc=col, r=0.0, z=5)
    D.text(ax, 2.1, 3.25, "색깔 띠 = 저항값 암호", size=14, color=S.INK_SOFT)

    # 기호: 지그재그
    zx1, zx2 = 5.0, 6.45
    sym_line(ax, SYM_X1, zx1)
    sym_line(ax, zx2, SYM_X2)
    n = 6
    pts = [(zx1, SYM_Y)]
    for i in range(n):
        pts.append((zx1 + (i + 0.5) * (zx2 - zx1) / n, SYM_Y + (0.25 if i % 2 == 0 else -0.25)))
    pts.append((zx2, SYM_Y))
    D.wire(ax, pts, color=S.INK, lw=3)
    D.text(ax, 5.72, 3.3, "지그재그", size=14, color=S.INK_SOFT)

    # 비유: 넓은 관 vs 중간이 좁은 관
    pipe_profile(ax, 0.6, 4.3, 1.75, lambda x: 0.55)
    pipe_profile(ax, 0.6, 4.3, 0.7,
                 lambda x: 0.55 - 0.38 * max(0.0, min(1.0, (1.0 - abs(x - 2.45) / 0.9) * 2.2)))
    D.arrow(ax, 1.0, 1.75, 3.9, 1.75, color=S.CURRENT, lw=6, head=20)
    D.arrow(ax, 1.0, 0.7, 1.75, 0.7, color=S.CURRENT, lw=3, head=12)
    D.arrow(ax, 3.15, 0.7, 3.9, 0.7, color=S.CURRENT, lw=3, head=12)
    D.text(ax, 4.6, 1.75, "넓은 관 → 콸콸", size=15, ha="left", weight="bold", color=S.CURRENT)
    D.text(ax, 4.6, 0.7, "좁은 관 → 졸졸", size=15, ha="left", weight="bold", color=S.RESIST)
    D.save(fig, "07_resistor")


# ── 2. 커패시터 ────────────────────────────────────
def bucket(ax, cx, by, w=0.9, h=0.85, level=0.6, angle=0.0, z=6):
    """물통 (cx = 가운데, by = 바닥 y). angle 만큼 기울임."""
    tr = transforms.Affine2D().rotate_deg_around(cx, by, angle) + ax.transData
    tw, bw = w, w * 0.75
    water = Polygon([(cx - bw / 2, by), (cx + bw / 2, by),
                     (cx + bw / 2 + (tw - bw) / 2 * level, by + h * level),
                     (cx - bw / 2 - (tw - bw) / 2 * level, by + h * level)],
                    closed=True, fc=C(S.WATER), ec="none", zorder=z, transform=tr)
    body = Polygon([(cx - tw / 2, by + h), (cx - bw / 2, by), (cx + bw / 2, by), (cx + tw / 2, by + h)],
                   closed=False, fc="none", ec=C(S.INK), lw=3, zorder=z + 1, transform=tr, joinstyle="round")
    if level > 0:
        ax.add_patch(water)
    ax.add_patch(body)


def capacitor():
    fig, ax = frame(S.CURRENT, "비유: 물통")
    # 실물: 원통형 전해 커패시터
    x0, x1, y0, y1 = 1.55, 2.65, 3.45, 4.75
    leg(ax, 1.85, y0, 1.85, 3.05)
    leg(ax, 2.35, y0, 2.35, 3.2)
    D.box(ax, x0, y0, x1 - x0, y1 - y0, fc="2D6FB7", r=0.0, z=4)
    D.box(ax, x1 - 0.32, y0, 0.32, y1 - y0, fc="A9C8EA", r=0.0, z=5)
    for yy in (3.75, 4.1, 4.45):
        D.text(ax, x1 - 0.16, yy, "−", size=14, color="2D6FB7", weight="bold")
    D.box(ax, x0, y1 - 0.12, x1 - x0, 0.12, fc=S.METAL, r=0.04, z=6)
    D.text(ax, 1.0, 3.25, "+ 긴 다리", size=14, color=S.RESIST, weight="bold")
    D.text(ax, 3.35, 3.4, "− 짧은 다리", size=14, color=S.INK_SOFT, weight="bold")

    # 기호: 판 두 장
    sym_line(ax, SYM_X1, 5.57)
    sym_line(ax, 5.87, SYM_X2)
    for x in (5.57, 5.87):
        ax.plot([x, x], [SYM_Y - 0.42, SYM_Y + 0.42], color=C(S.INK), lw=4, zorder=6)
    D.text(ax, 5.72, 3.25, "마주 보는 판 두 장", size=14, color=S.INK_SOFT)

    # 비유: 수도꼭지 → 물통 (저장) → 붓기 (방출)
    D.box(ax, 0.55, 1.95, 0.9, 0.18, fc=S.METAL, ec=S.INK, lw=2, r=0.04, z=6)
    D.box(ax, 1.3, 1.65, 0.18, 0.48, fc=S.METAL, ec=S.INK, lw=2, r=0.04, z=6)
    ax.add_patch(Polygon([(1.33, 1.65), (1.45, 1.65), (1.43, 1.0), (1.35, 1.0)], fc=C(S.WATER), ec="none",
                         zorder=5))
    bucket(ax, 1.39, 0.4, level=0.6)
    D.text(ax, 2.4, 0.9, "모으기", size=15, weight="bold", color=S.CURRENT)
    D.text(ax, 2.4, 0.55, "(저장)", size=14, color=S.INK_SOFT)

    D.big_arrow(ax, 3.1, 1.0, 3.9, 1.0, color=S.INK_SOFT, width=0.18)

    bucket(ax, 4.6, 1.0, level=0.25, angle=-55)
    # 쏟아지는 물 (기울어진 물통 입구 아래쪽 모서리에서)
    ax.add_patch(Polygon([(5.48, 1.13), (5.6, 1.08), (5.9, 0.3), (5.5, 0.3)], fc=C(S.WATER), ec="none",
                         zorder=5))
    for x, y in ((5.3, 0.45), (6.05, 0.55), (6.15, 0.3)):
        D.drop(ax, x, y, s=0.08)
    D.text(ax, 6.45, 1.55, "한꺼번에", size=15, weight="bold", color=S.VOLT)
    D.text(ax, 6.45, 1.2, "(방출)", size=14, color=S.INK_SOFT)
    D.save(fig, "07_capacitor")


# ── 3. 다이오드 ────────────────────────────────────
def gate(ax, x, y, open_=True, h=0.7):
    """벽 사이의 한쪽(오른쪽)으로만 열리는 문."""
    D.box(ax, x - 0.1, y + h / 2, 0.2, 0.18, fc=S.INK_SOFT, r=0.03, z=6)
    D.box(ax, x - 0.1, y - h / 2 - 0.18, 0.2, 0.18, fc=S.INK_SOFT, r=0.03, z=6)
    hinge_y = y + h / 2
    if open_:
        ang = math.radians(-30)
        ax.plot([x, x + h * math.cos(ang)], [hinge_y, hinge_y + h * math.sin(ang)], color=C(S.INK), lw=6,
                solid_capstyle="round", zorder=7)
    else:
        ax.plot([x, x], [hinge_y, y - h / 2], color=C(S.INK), lw=6, solid_capstyle="round", zorder=7)
        # 멈춤턱: 문이 왼쪽으로는 못 열림
        D.box(ax, x - 0.24, y - h / 2, 0.14, 0.2, fc=S.RESIST, r=0.02, z=8)
    ax.add_patch(Circle((x, hinge_y), 0.07, fc=C(S.INK), zorder=8))


def diode():
    fig, ax = frame(S.SAFE, "비유: 한쪽으로만 열리는 문")
    cy = 4.0
    leg(ax, 0.4, cy, 3.9, cy)
    D.box(ax, 1.3, cy - 0.3, 1.6, 0.6, fc=S.INK, r=0.22, z=4)
    D.box(ax, 2.45, cy - 0.3, 0.18, 0.6, fc="C9CED8", r=0.0, z=5)
    D.arrow(ax, 1.3, 3.3, 2.9, 3.3, color=S.SAFE, lw=4, head=14)
    D.text(ax, 3.05, 3.3, "이 방향만", size=14, color=S.SAFE, weight="bold", ha="left")
    D.text(ax, 2.54, 4.55, "은색 띠", size=14, color=S.INK_SOFT)

    sym_line(ax, SYM_X1, 5.3)
    sym_line(ax, 6.1, SYM_X2)
    diode_symbol(ax, 5.62, SYM_Y, s=0.38)
    D.text(ax, 5.72, 3.25, "삼각형 + 막대", size=14, color=S.INK_SOFT)

    # 비유
    gate(ax, 3.3, 1.72, open_=True)
    D.arrow(ax, 0.6, 1.57, 4.2, 1.57, color=S.SAFE, lw=6, head=20)
    check(ax, 4.6, 1.67, ok=True)
    D.text(ax, 4.95, 1.67, "정방향 → 통과", size=15, weight="bold", ha="left", color=S.SAFE)

    gate(ax, 3.3, 0.72, open_=False)
    D.arrow(ax, 4.2, 0.62, 3.42, 0.62, color=S.RESIST, lw=6, head=20)
    check(ax, 4.6, 0.67, ok=False)
    D.text(ax, 4.95, 0.67, "역방향 → 막힘", size=15, weight="bold", ha="left", color=S.RESIST)
    D.save(fig, "07_diode")


# ── 4. LED ────────────────────────────────────────
def led_shape(ax, cx, by, w=0.5, h=0.7, lit=True, color="E5533D", z=6, legs=True, leg_len=(0.5, 0.35), glow=1.15):
    """LED 실물 모양. (cx, by) = 몸통 아래 가운데."""
    if lit:
        for k, a in ((glow, 0.18), (glow * 0.75, 0.3)):
            ax.add_patch(Circle((cx, by + h * 0.6), w * k, fc=C(S.GLOW), ec="none", alpha=a, zorder=z - 1))
    fc = "FF6B5A" if lit else "F1C4BE"
    D.box(ax, cx - w / 2, by, w, h - w / 2, fc=fc, r=0.0, z=z)
    ax.add_patch(Wedge((cx, by + h - w / 2), w / 2, 0, 180, fc=C(fc), ec="none", zorder=z))
    D.box(ax, cx - w / 2 - 0.06, by - 0.02, w + 0.12, 0.1, fc=fc, ec=C(color) if False else None, r=0.02,
          z=z + 1)
    if legs:
        leg(ax, cx - w * 0.22, by, cx - w * 0.22, by - leg_len[0], lw=3.5)
        leg(ax, cx + w * 0.22, by, cx + w * 0.22, by - leg_len[1], lw=3.5)


def mini_battery(ax, cx, cy, flip=False, w=0.9, h=0.42):
    """작은 건전지. flip=False 면 + 가 오른쪽."""
    D.box(ax, cx - w / 2, cy - h / 2, w, h, fc=S.INK, r=0.06, z=6)
    pos_x = cx + w / 2 - 0.22 if not flip else cx - w / 2
    D.box(ax, pos_x, cy - h / 2, 0.22, h, fc=S.SPARK, r=0.0, z=7)
    D.text(ax, cx + (0.28 if not flip else -0.28), cy, "+", size=15, color=S.INK, weight="bold", zorder=9)


def led():
    fig, ax = frame(S.VOLT, "정방향 → 빛남 / 역방향 → 꺼짐")
    # 실물
    led_shape(ax, 2.15, 3.75, w=0.75, h=0.95, lit=True, leg_len=(0.65, 0.4))
    D.text(ax, 1.05, 3.3, "+ 긴 다리", size=14, color=S.RESIST, weight="bold")
    D.text(ax, 3.25, 3.45, "− 짧은 다리", size=14, color=S.INK_SOFT, weight="bold")

    # 기호
    sym_line(ax, SYM_X1, 5.3)
    sym_line(ax, 6.1, SYM_X2)
    diode_symbol(ax, 5.62, SYM_Y - 0.1, s=0.36)
    for dx in (0.0, 0.28):
        D.arrow(ax, 5.75 + dx, SYM_Y + 0.35, 6.05 + dx, SYM_Y + 0.75, color=S.VOLT, lw=2.5, head=10)
    D.text(ax, 5.72, 3.25, "다이오드 + 빛 화살표", size=14, color=S.INK_SOFT)

    # 비유 대신: 두 개의 작은 회로
    for x0, ok in ((0.35, True), (3.75, False)):
        lx, rx, ty, bty, mx = x0 + 0.3, x0 + 2.0, 1.45, 0.4, x0 + 1.15
        D.wire(ax, [(mx, bty), (lx, bty), (lx, ty), (rx, ty), (rx, bty), (mx, bty)], lw=3.5)
        mini_battery(ax, mx, bty, flip=not ok)
        led_shape(ax, mx, ty + 0.02, w=0.36, h=0.5, lit=ok, legs=False, glow=1.0)
        check(ax, x0 + 2.55, 1.2, ok=ok, r=0.22)
        D.text(ax, x0 + 2.55, 0.65, "빛남" if ok else "꺼짐", size=15, weight="bold",
               color=S.SAFE if ok else S.RESIST)
    D.save(fig, "07_led")


# ── 5. 트랜지스터 ──────────────────────────────────
def transistor():
    fig, ax = frame(S.VOLT, "비유: 수도꼭지")
    # 실물 TO-92
    cx, by, w, h = 2.15, 3.85, 1.0, 1.05
    ax.add_patch(Polygon([(cx - w / 2, by), (cx + w / 2, by), (cx + w / 2, by + h * 0.8),
                          (cx + w * 0.3, by + h), (cx - w * 0.3, by + h), (cx - w / 2, by + h * 0.8)],
                         closed=True, fc=C(S.INK), ec="none", zorder=5))
    for i, lab in enumerate(("E", "B", "C")):
        x = cx - 0.3 + i * 0.3
        leg(ax, x, by, x, 3.2, lw=3.5)
        D.text(ax, x, 3.05, lab, size=13, color=S.INK_SOFT, weight="bold")
    D.text(ax, 3.35, 4.35, "다리 3개", size=14, color=S.INK_SOFT, weight="bold")

    # 기호 (NPN)
    sx, sy, r = 5.85, SYM_Y, 0.55
    ax.add_patch(Circle((sx, sy), r, fc="white", ec=C(S.INK), lw=2.5, zorder=4))
    ax.plot([sx - 0.18] * 2, [sy - 0.3, sy + 0.3], color=C(S.INK), lw=4, zorder=6)
    sym_line(ax, SYM_X1 + 0.1, sx - 0.18)
    ax.plot([sx - 0.18, sx + 0.22, sx + 0.22], [sy + 0.12, sy + 0.38, sy + 0.8], color=C(S.INK), lw=3,
            zorder=6)
    ax.plot([sx + 0.22, sx + 0.22], [sy - 0.38, sy - 0.8], color=C(S.INK), lw=3, zorder=6)
    D.arrow(ax, sx - 0.18, sy - 0.12, sx + 0.22, sy - 0.38, color=S.INK, lw=3, head=12)
    D.text(ax, SYM_X1 + 0.15, sy + 0.25, "B", size=13, weight="bold", color=S.INK_SOFT)
    D.text(ax, sx + 0.48, sy + 0.65, "C", size=13, weight="bold", color=S.INK_SOFT)
    D.text(ax, sx + 0.48, sy - 0.65, "E", size=13, weight="bold", color=S.INK_SOFT)

    # 비유: 수도꼭지
    D.box(ax, 0.4, 1.12, 1.9, 0.42, fc=S.WATER, ec=S.INK, lw=2.5, r=0.04, z=4)
    D.box(ax, 2.2, 0.95, 0.85, 0.75, fc=S.METAL, ec=S.INK, lw=2.5, r=0.1, z=6)
    D.box(ax, 2.95, 1.12, 0.75, 0.42, fc=S.METAL, ec=S.INK, lw=2.5, r=0.06, z=6)
    D.box(ax, 3.35, 0.82, 0.35, 0.72, fc=S.METAL, ec=S.INK, lw=2.5, r=0.06, z=6)
    D.box(ax, 2.58, 1.7, 0.1, 0.25, fc=S.INK_SOFT, r=0.02, z=5)
    D.box(ax, 2.2, 1.93, 0.85, 0.14, fc=S.RESIST, r=0.05, z=6)
    # 손잡이 돌리는 작은 화살표
    D.arrow(ax, 2.05, 2.25, 3.25, 2.25, color=S.CURRENT, lw=3, head=12, rad=-0.35)
    D.text(ax, 1.25, 1.95, "살짝 돌림", size=14, weight="bold", color=S.CURRENT)
    # 콸콸 쏟아지는 물
    ax.add_patch(Polygon([(3.37, 0.82), (3.68, 0.82), (3.85, 0.25), (3.2, 0.25)], fc=C(S.WATER), ec="none",
                         zorder=5))
    for x, y in ((3.05, 0.4), (4.0, 0.45), (3.95, 0.7)):
        D.drop(ax, x, y, s=0.07)
    D.text(ax, 4.45, 1.75, "작은 신호 (B)", size=15, weight="bold", color=S.CURRENT, ha="left")
    D.text(ax, 4.45, 1.3, "↓", size=15, weight="bold", color=S.INK_SOFT, ha="left")
    D.text(ax, 4.45, 0.85, "큰 전류 (C → E)", size=15, weight="bold", color=S.VOLT, ha="left")
    D.save(fig, "07_transistor")


def main():
    resistor()
    capacitor()
    diode()
    led()
    transistor()


if __name__ == "__main__":
    main()
