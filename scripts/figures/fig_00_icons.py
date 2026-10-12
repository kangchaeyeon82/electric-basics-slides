"""표지 그림, 로드맵, 섹션 아이콘, 카드 아이콘."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))
import draw_helpers as D  # noqa: E402
import style as S  # noqa: E402
from matplotlib import patches  # noqa: E402
from matplotlib.patches import Circle, Ellipse, Polygon, Arc  # noqa: E402

C = D.C
WHITE = "FFFFFF"


# ── 공통 로컬 도형 ─────────────────────────────────
def line(ax, xs, ys, color=WHITE, lw=4, z=10, alpha=1.0):
    ax.plot(xs, ys, color=C(color), lw=lw, solid_capstyle="round", solid_joinstyle="round",
            zorder=z, alpha=alpha)


def poly(ax, pts, fc=WHITE, ec=None, lw=0, z=10):
    ax.add_patch(Polygon(pts, closed=True, fc=C(fc), ec=C(ec) if ec else "none", lw=lw, zorder=z,
                         joinstyle="round"))


def shield_pts(cx, cy, w, h):
    pts = [(cx - w / 2, cy + h * 0.42), (cx, cy + h / 2), (cx + w / 2, cy + h * 0.42)]
    for i in range(1, 12):
        t = i / 12
        pts.append((cx + w / 2 * (1 - t ** 1.6), cy + h * 0.42 - h * 0.92 * t ** 0.9))
    pts.append((cx, cy - h / 2))
    for i in range(11, 0, -1):
        t = i / 12
        pts.append((cx - w / 2 * (1 - t ** 1.6), cy + h * 0.42 - h * 0.92 * t ** 0.9))
    return pts


def drop_shape(ax, cx, cy, s, fc, z=10):
    """물방울: (cx, cy) = 둥근 부분 중심, s = 반지름."""
    pts = [(cx, cy + s * 2.0)]
    for i in range(30, -211, -10):
        a = math.radians(i)
        pts.append((cx + s * math.cos(a), cy + s * math.sin(a)))
    poly(ax, pts, fc=fc, z=z)


# ── 1. 표지 ────────────────────────────────────────
def cover():
    W = 6.2
    fig, ax = D.new_fig(W, W)
    cx, cy = 3.1, 3.35
    r = 1.35

    # 회로 기판 배선 (밝은 선 + 끝 패드)
    traces = [
        [(cx - r - 0.1, cy + 0.2), (0.9, cy + 0.2), (0.9, 5.4)],
        [(cx - r, cy - 0.5), (0.45, cy - 0.5)],
        [(cx + r + 0.1, cy + 0.2), (5.3, cy + 0.2), (5.3, 5.5)],
        [(cx + r, cy - 0.5), (5.8, cy - 0.5)],
        [(cx - 0.35, 1.0), (cx - 0.35, 0.55), (1.2, 0.55), (1.2, 1.6)],
        [(cx + 0.35, 1.0), (cx + 0.35, 0.55), (5.0, 0.55), (5.0, 1.7)],
        [(cx, cy + r + 0.1), (cx, 5.85)],
    ]
    for tr in traces:
        xs, ys = zip(*tr)
        line(ax, xs, ys, color=S.CURRENT, lw=3, z=2, alpha=0.9)
        ax.add_patch(Circle(tr[-1], 0.11, fc=C(S.NIGHT), ec=C(S.CURRENT), lw=3, zorder=3))
    for tr, n, off in zip(traces, (3, 1, 3, 2, 3, 3, 2), (0.0, 0.3, 0.5, 0.1, 0.2, 0.6, 0.25)):
        D.electrons_along(ax, tr, n, r=0.075, color=WHITE, offset=off)

    # 빛 번짐
    for k, a in ((2.05, 0.10), (1.7, 0.16), (1.38, 0.28)):
        ax.add_patch(Circle((cx, cy), r * k, fc=C(S.SPARK), ec="none", alpha=a, zorder=4))
    # 광선
    for i in range(12):
        ang = math.radians(i * 30 + 15)
        if 200 < math.degrees(ang) % 360 < 340:
            continue
        L1, L2 = r * 1.5, r * 1.85
        line(ax, [cx + L1 * math.cos(ang), cx + L2 * math.cos(ang)],
             [cy + L1 * math.sin(ang), cy + L2 * math.sin(ang)], color=S.SPARK, lw=5, z=5)

    # 유리구
    ax.add_patch(Circle((cx, cy), r, fc=C(S.GLOW), ec=C(WHITE), lw=5, zorder=6))
    ax.add_patch(Arc((cx - 0.35, cy + 0.35), 1.2, 1.2, theta1=100, theta2=170, color=C(WHITE), lw=6, zorder=7))
    D.bolt(ax, cx + 0.05, cy - 0.05, h=1.75, color=S.VOLT, z=8)
    # 목 + 소켓
    poly(ax, [(cx - 0.62, cy - r * 0.78), (cx + 0.62, cy - r * 0.78), (cx + 0.45, cy - r - 0.2),
              (cx - 0.45, cy - r - 0.2)], fc=S.GLOW, ec=WHITE, lw=5, z=5)
    for k in range(3):
        y = cy - r - 0.25 - k * 0.2
        D.box(ax, cx - 0.48 + k * 0.03, y - 0.16, 0.96 - k * 0.06, 0.16, fc=S.METAL, ec=WHITE, lw=2.5,
              r=0.06, z=8)
    D.box(ax, cx - 0.25, cy - r - 0.98, 0.5, 0.2, fc=WHITE, r=0.08, z=8)
    D.save(fig, "00_cover")


# ── 2. 로드맵 ──────────────────────────────────────
STOPS = [
    ("01", "전기의 정체", S.CURRENT),
    ("02", "전압·전류·저항", S.VOLT),
    ("03", "옴의 법칙", S.INK),
    ("04", "회로", S.SAFE),
    ("05", "전력·요금", S.SPARK),
    ("06", "직류·교류", S.CURRENT),
    ("07", "전자 부품", S.VOLT),
    ("08", "전기 안전", S.RESIST),
]


def roadmap():
    fig, ax = D.new_fig(12.0, 4.9)
    y1, y2 = 3.6, 1.6
    xr = 10.65
    rc = (y1 - y2) / 2
    road_w = 0.42 * 72 * 1.0  # pt (선 굵기)

    # 길: 아래 회색 띠 + 가운데 흰 점선
    xs = [0.45, xr]
    ys = [y1, y1]
    t = [math.radians(90 - i * 6) for i in range(31)]
    xs += [xr + rc * math.cos(a) for a in t]
    ys += [y2 + rc + rc * math.sin(a) for a in t]
    xs += [0.45]
    ys += [y2]
    ax.plot(xs, ys, color=C(S.LINE), lw=road_w, solid_capstyle="round", solid_joinstyle="round", zorder=1)
    ax.plot(xs, ys, color=C(WHITE), lw=2.5, ls=(0, (4, 4)), zorder=2)

    pos = [(0.95 + i * 2.88, y1) for i in range(4)] + [(9.59 - i * 2.6, y2) for i in range(4)]
    for (num, label, col), (x, y) in zip(STOPS, pos):
        ax.add_patch(Circle((x, y), 0.4, fc=C(col), ec=C(WHITE), lw=4, zorder=5))
        tc = S.INK if col == S.SPARK else WHITE
        D.text(ax, x, y, num, size=17, color=tc, weight="bold")
        D.text(ax, x, y - 0.68, label, size=16, color=S.INK, weight="bold")

    # 도착 깃발
    fx, fy = 0.42, y2
    line(ax, [fx, fx], [fy - 0.05, fy + 0.95], color=S.INK, lw=4, z=6)
    poly(ax, [(fx, fy + 0.95), (fx + 0.62, fy + 0.8), (fx, fy + 0.6)], fc=S.RESIST, z=6)
    ax.add_patch(Circle((fx, fy - 0.05), 0.09, fc=C(S.INK), ec="none", zorder=6))
    D.text(ax, fx, fy - 0.68, "정리", size=16, color=S.RESIST, weight="bold")
    D.save(fig, "00_roadmap")


# ── 3. 섹션 아이콘 (어두운 배경용) ─────────────────
def sec_base():
    fig, ax = D.new_fig(3.0, 3.0)
    ax.add_patch(Circle((1.5, 1.5), 1.42, fc=C(S.NIGHT_2), ec=C(S.SPARK), lw=3, zorder=1))
    return fig, ax


def sec_atom():
    fig, ax = sec_base()
    for ang in (0, 60, 120):
        ax.add_patch(Ellipse((1.5, 1.5), 2.2, 0.8, angle=ang, fc="none", ec=C(S.CURRENT), lw=4, zorder=3))
    ax.add_patch(Circle((1.5, 1.5), 0.25, fc=C(S.RESIST), ec=C(WHITE), lw=2, zorder=5))
    for ang in (0, 60, 120):
        a = math.radians(ang)
        # 타원 위 한 점
        px, py = 1.1 * math.cos(math.radians(40)), 0.4 * math.sin(math.radians(40))
        x = 1.5 + px * math.cos(a) - py * math.sin(a)
        y = 1.5 + px * math.sin(a) + py * math.cos(a)
        ax.add_patch(Circle((x, y), 0.12, fc=C(WHITE), ec="none", zorder=6))
    D.save(fig, "sec_atom", folder=S.ICON_DIR)


def sec_water():
    fig, ax = sec_base()
    drop_shape(ax, 1.5, 1.35, 0.62, S.WATER, z=4)
    ax.add_patch(Arc((1.5, 1.35), 0.8, 0.8, theta1=200, theta2=260, color=C(WHITE), lw=5, zorder=5))
    D.bolt(ax, 1.52, 1.45, h=0.8, color=S.SPARK, z=6)
    D.save(fig, "sec_water", folder=S.ICON_DIR)


def sec_ohm():
    fig, ax = sec_base()
    cx, cy = 1.5, 1.4
    pts = [(cx, cy + 0.95), (cx + 1.0, cy - 0.65), (cx - 1.0, cy - 0.65)]
    poly(ax, pts, fc=S.NIGHT_2, ec=S.SPARK, lw=4, z=3)
    line(ax, [cx - 0.62, cx + 0.62], [cy - 0.05, cy - 0.05], color=S.SPARK, lw=4, z=4)
    line(ax, [cx, cx], [cy - 0.05, cy - 0.65], color=S.SPARK, lw=4, z=4)
    D.text(ax, cx, cy + 0.35, "V", size=30, color=S.VOLT, weight="bold")
    D.text(ax, cx - 0.4, cy - 0.36, "I", size=26, color=S.CURRENT, weight="bold")
    D.text(ax, cx + 0.4, cy - 0.36, "R", size=26, color=S.RESIST, weight="bold")
    D.save(fig, "sec_ohm", folder=S.ICON_DIR)


def sec_circuit():
    fig, ax = sec_base()
    x0, x1, y0, y1 = 0.7, 2.3, 0.85, 2.0
    line(ax, [x0, x0, 1.2], [y0 + 0.45, y1, y1], color=C(WHITE), lw=5, z=3)
    line(ax, [1.8, x1, x1, x0, x0], [y1, y1, y0, y0, y0 + 0.45], color=C(WHITE), lw=5, z=3)
    # 전구 (위)
    ax.add_patch(Circle((1.5, y1), 0.38, fc=C(S.SPARK), ec=C(WHITE), lw=4, zorder=5))
    for i in range(5):
        a = math.radians(30 + i * 30)
        line(ax, [1.5 + 0.5 * math.cos(a), 1.5 + 0.68 * math.cos(a)],
             [y1 + 0.5 * math.sin(a), y1 + 0.68 * math.sin(a)], color=S.SPARK, lw=4, z=5)
    # 전지 (아래)
    D.box(ax, 1.2, y0 - 0.17, 0.6, 0.34, fc=S.CURRENT, ec=C(WHITE), lw=3, r=0.06, z=5)
    D.text(ax, 1.5, y0, "+  −", size=12, color=C(WHITE), weight="bold")
    D.save(fig, "sec_circuit", folder=S.ICON_DIR)


def plug_glyph(ax, cx, cy, s=1.0, fc=WHITE, z=6, prong=None):
    """콘센트 플러그(한국형 둥근 핀) — (cx, cy) = 몸체 중심."""
    prong = prong or fc
    D.box(ax, cx - 0.42 * s, cy - 0.32 * s, 0.84 * s, 0.64 * s, fc=fc, r=0.16 * s, z=z)
    for dx in (-0.2, 0.2):
        D.box(ax, cx + dx * s - 0.06 * s, cy + 0.3 * s, 0.12 * s, 0.38 * s, fc=prong, r=0.05 * s, z=z)
    line(ax, [cx, cx], [cy - 0.3 * s, cy - 0.75 * s], color=fc, lw=6 * s, z=z)


def sec_power():
    fig, ax = sec_base()
    plug_glyph(ax, 1.5, 1.55, s=1.25, fc=WHITE)
    D.bolt(ax, 1.5, 1.5, h=0.62, color=S.SPARK, z=8)
    D.save(fig, "sec_power", folder=S.ICON_DIR)


def sec_wave():
    fig, ax = sec_base()
    xs = [0.45 + i * 2.1 / 100 for i in range(101)]
    ys = [1.75 + 0.45 * math.sin(i / 100 * 4 * math.pi) for i in range(101)]
    line(ax, xs, ys, color=S.SPARK, lw=5, z=4)
    line(ax, [0.45, 2.55], [0.95, 0.95], color=S.CURRENT, lw=5, z=4)
    D.text(ax, 2.35, 1.12, "", size=10)
    D.save(fig, "sec_wave", folder=S.ICON_DIR)


def sec_chip():
    fig, ax = sec_base()
    s = 1.1
    x0, y0 = 1.5 - s / 2, 1.5 - s / 2
    for i in range(4):
        o = x0 + 0.17 + i * (s - 0.34) / 3
        for (xa, ya, xb, yb) in ((o, y0, o, y0 - 0.28), (o, y0 + s, o, y0 + s + 0.28),
                                 (x0, o, x0 - 0.28, o), (x0 + s, o, x0 + s + 0.28, o)):
            line(ax, [xa, xb], [ya, yb], color=S.METAL, lw=5, z=3)
    D.box(ax, x0, y0, s, s, fc=S.INK, ec=S.SPARK, lw=4, r=0.12, z=5)
    D.box(ax, x0 + 0.3, y0 + 0.3, s - 0.6, s - 0.6, fc=S.SPARK, r=0.06, z=6)
    ax.add_patch(Circle((x0 + 0.17, y0 + s - 0.17), 0.06, fc=C(WHITE), ec="none", zorder=6))
    D.save(fig, "sec_chip", folder=S.ICON_DIR)


def sec_shield():
    fig, ax = sec_base()
    poly(ax, shield_pts(1.5, 1.45, 1.55, 1.85), fc=S.SAFE, ec=WHITE, lw=4, z=4)
    D.bolt(ax, 1.5, 1.45, h=0.95, color=S.SPARK, z=6)
    D.save(fig, "sec_shield", folder=S.ICON_DIR)


# ── 4. 카드 아이콘 (밝은 배경용) ───────────────────
def card(fc):
    fig, ax = D.new_fig(1.6, 1.6)
    ax.add_patch(Circle((0.8, 0.8), 0.72, fc=C(fc), ec="none", zorder=1))
    return fig, ax


def done(fig, name):
    D.save(fig, name, folder=S.ICON_DIR)


def icon_voltage():
    fig, ax = card(S.VOLT)
    # 높은 물탱크 + 높이 화살표
    ax.add_patch(patches.Rectangle((0.72, 0.98), 0.42, 0.18, fc=C(WHITE), ec="none", zorder=4))
    line(ax, [0.72, 0.72, 1.14, 1.14], [1.3, 0.98, 0.98, 1.3], lw=3, z=5)
    line(ax, [0.78, 0.78], [0.98, 0.42], lw=3, z=4)
    line(ax, [1.08, 1.08], [0.98, 0.42], lw=3, z=4)
    line(ax, [0.5, 0.5], [0.45, 1.22], lw=3, z=4)
    poly(ax, [(0.5, 1.33), (0.41, 1.17), (0.59, 1.17)], z=5)
    line(ax, [0.4, 1.2], [0.42, 0.42], lw=3, z=4)
    done(fig, "icon_voltage")


def icon_current():
    fig, ax = card(S.CURRENT)
    for y in (1.0, 0.6):
        line(ax, [0.32, 1.12], [y, y], lw=4, z=4)
        poly(ax, [(1.3, y), (1.08, y + 0.13), (1.08, y - 0.13)], z=5)
    for x, y in ((0.55, 1.0), (0.85, 0.6)):
        ax.add_patch(Circle((x, y), 0.11, fc=C(WHITE), ec=C(S.CURRENT), lw=2, zorder=6))
    done(fig, "icon_current")


def zigzag(ax, x0, x1, y, amp, n, color=WHITE, lw=4, z=5):
    xs = [x0] + [x0 + (x1 - x0) * (i + 0.5) / n for i in range(n)] + [x1]
    ys = [y] + [y + (amp if i % 2 == 0 else -amp) for i in range(n)] + [y]
    line(ax, xs, ys, color=color, lw=lw, z=z)


def icon_resistance():
    fig, ax = card(S.RESIST)
    line(ax, [0.22, 0.45], [0.8, 0.8], lw=4)
    line(ax, [1.15, 1.38], [0.8, 0.8], lw=4)
    zigzag(ax, 0.45, 1.15, 0.8, 0.2, 6)
    done(fig, "icon_resistance")


def icon_resistor():
    fig, ax = card(S.RESIST)
    line(ax, [0.18, 1.42], [0.8, 0.8], color=S.METAL, lw=4, z=3)
    D.box(ax, 0.42, 0.6, 0.76, 0.4, fc="F4E3C8", r=0.16, z=5)
    for x, c in ((0.58, S.INK), (0.73, S.VOLT), (0.88, S.RESIST), (1.03, S.SPARK)):
        ax.add_patch(patches.Rectangle((x - 0.035, 0.6), 0.07, 0.4, fc=C(c), ec="none", zorder=6))
    done(fig, "icon_resistor")


def icon_capacitor():
    fig, ax = card(S.CURRENT)
    line(ax, [0.22, 0.68], [0.8, 0.8], lw=4)
    line(ax, [0.92, 1.38], [0.8, 0.8], lw=4)
    line(ax, [0.68, 0.68], [0.45, 1.15], lw=6)
    line(ax, [0.92, 0.92], [0.45, 1.15], lw=6)
    done(fig, "icon_capacitor")


def icon_diode():
    fig, ax = card(S.SAFE)
    line(ax, [0.2, 1.4], [0.8, 0.8], lw=4, z=3)
    poly(ax, [(0.55, 1.12), (0.55, 0.48), (1.03, 0.8)], z=5)
    line(ax, [1.06, 1.06], [0.46, 1.14], lw=5, z=5)
    done(fig, "icon_diode")


def icon_led():
    fig, ax = card(S.SPARK)
    ink = S.INK
    # 돔
    ax.add_patch(patches.Wedge((0.8, 0.95), 0.27, 0, 180, fc=C(ink), ec="none", zorder=5))
    ax.add_patch(patches.Rectangle((0.53, 0.72), 0.54, 0.24, fc=C(ink), ec="none", zorder=5))
    ax.add_patch(patches.Rectangle((0.48, 0.66), 0.64, 0.08, fc=C(ink), ec="none", zorder=5))
    line(ax, [0.68, 0.68], [0.66, 0.3], color=ink, lw=3.5, z=4)
    line(ax, [0.92, 0.92], [0.66, 0.38], color=ink, lw=3.5, z=4)
    for a in (35, 90, 145):
        r = math.radians(a)
        line(ax, [0.8 + 0.38 * math.cos(r), 0.8 + 0.52 * math.cos(r)],
             [0.97 + 0.38 * math.sin(r), 0.97 + 0.52 * math.sin(r)], color=ink, lw=3.5, z=4)
    done(fig, "icon_led")


def icon_transistor():
    fig, ax = card(S.VOLT)
    # 수도꼭지
    D.box(ax, 0.25, 0.9, 0.7, 0.2, fc=WHITE, r=0.05, z=5)          # 가로 파이프
    D.box(ax, 0.82, 0.62, 0.22, 0.48, fc=WHITE, r=0.08, z=5)       # 꼭지 몸통
    D.box(ax, 0.86, 0.5, 0.14, 0.14, fc=WHITE, r=0.03, z=5)        # 주둥이
    line(ax, [0.93, 0.93], [1.1, 1.24], lw=4, z=5)                  # 손잡이 축
    line(ax, [0.76, 1.1], [1.26, 1.26], lw=5, z=5)                  # 손잡이
    for y in (0.38, 0.24):
        ax.add_patch(Circle((0.93, y), 0.045, fc=C(WHITE), ec="none", zorder=5))
    done(fig, "icon_transistor")


def icon_wet_hand():
    fig, ax = card(S.RESIST)
    # 손바닥
    D.box(ax, 0.48, 0.32, 0.5, 0.5, fc=WHITE, r=0.14, z=5)
    for i, h in enumerate((0.42, 0.5, 0.47, 0.38)):
        D.box(ax, 0.49 + i * 0.125, 0.62, 0.105, h, fc=WHITE, r=0.05, z=5)
    # 엄지
    ax.add_patch(patches.FancyBboxPatch((0.3, 0.5), 0.3, 0.11, boxstyle="round,pad=0,rounding_size=0.05",
                                        fc=C(WHITE), ec="none", zorder=5,
                                        transform=__import__("matplotlib").transforms.Affine2D()
                                        .rotate_deg_around(0.55, 0.55, 35) + ax.transData))
    # 물방울
    drop_shape(ax, 1.17, 1.02, 0.1, WHITE, z=6)
    drop_shape(ax, 1.25, 0.66, 0.07, WHITE, z=6)
    done(fig, "icon_wet_hand")


def icon_multitap():
    fig, ax = card(S.RESIST)
    D.box(ax, 0.28, 0.45, 1.04, 0.3, fc=WHITE, r=0.08, z=5)
    for x in (0.45, 0.8, 1.15):
        ax.add_patch(Circle((x, 0.6), 0.07, fc=C(S.RESIST), ec="none", zorder=6))
        D.box(ax, x - 0.1, 0.8, 0.2, 0.2, fc=WHITE, r=0.04, z=5)
        line(ax, [x, x], [1.0, 1.25], lw=3, z=5)
    line(ax, [0.28, 0.2], [0.6, 0.6], lw=3, z=4)
    done(fig, "icon_multitap")


def icon_plug():
    fig, ax = card(S.VOLT)
    plug_glyph(ax, 0.8, 0.82, s=0.75, fc=WHITE)
    done(fig, "icon_plug")


def icon_breaker():
    fig, ax = card(S.SAFE)
    D.box(ax, 0.45, 0.32, 0.7, 0.96, fc=WHITE, r=0.1, z=5)
    D.box(ax, 0.66, 0.62, 0.28, 0.46, fc=S.SAFE, r=0.06, z=6)
    D.box(ax, 0.7, 0.85, 0.2, 0.19, fc=WHITE, r=0.04, z=7)
    ax.add_patch(Circle((0.8, 0.45), 0.07, fc=C(S.RESIST), ec="none", zorder=6))
    done(fig, "icon_breaker")


def icon_electron():
    fig, ax = card(S.CURRENT)
    ax.add_patch(Ellipse((0.8, 0.8), 1.05, 0.42, angle=25, fc="none", ec=C(WHITE), lw=2.5, zorder=4))
    ax.add_patch(Circle((0.8, 0.8), 0.3, fc=C(WHITE), ec="none", zorder=5))
    line(ax, [0.66, 0.94], [0.8, 0.8], color=S.CURRENT, lw=6, z=6)
    done(fig, "icon_electron")


def icon_ohm():
    fig, ax = card(S.INK)
    D.text(ax, 0.8, 0.82, "Ω", size=46, color=WHITE, weight="bold")
    done(fig, "icon_ohm")


def icon_circuit():
    fig, ax = card(S.SAFE)
    line(ax, [0.62, 0.38, 0.38, 1.22, 1.22, 0.98], [1.08, 1.08, 0.48, 0.48, 1.08, 1.08], lw=3.5, z=4)
    ax.add_patch(Circle((0.8, 1.08), 0.17, fc=C(S.SPARK), ec=C(WHITE), lw=3, zorder=5))
    line(ax, [0.72, 0.72], [0.36, 0.6], lw=4, z=5)
    line(ax, [0.88, 0.88], [0.41, 0.55], lw=4, z=5)
    ax.add_patch(patches.Rectangle((0.73, 0.4), 0.14, 0.16, fc=C(S.SAFE), ec="none", zorder=4))
    line(ax, [0.72, 0.72], [0.36, 0.6], lw=4, z=5)
    line(ax, [0.88, 0.88], [0.41, 0.55], lw=4, z=5)
    done(fig, "icon_circuit")


def icon_power():
    fig, ax = card(S.SPARK)
    D.bolt(ax, 0.82, 0.8, h=0.95, color=S.INK, z=5)
    done(fig, "icon_power")


def icon_shield():
    fig, ax = card(S.RESIST)
    poly(ax, shield_pts(0.8, 0.8, 0.76, 0.92), fc=WHITE, z=5)
    D.bolt(ax, 0.8, 0.8, h=0.5, color=S.RESIST, z=6)
    done(fig, "icon_shield")


def main():
    cover()
    roadmap()
    for f in (sec_atom, sec_water, sec_ohm, sec_circuit, sec_power, sec_wave, sec_chip, sec_shield):
        f()
    for f in (icon_voltage, icon_current, icon_resistance, icon_resistor, icon_capacitor, icon_diode,
              icon_led, icon_transistor, icon_wet_hand, icon_multitap, icon_plug, icon_breaker,
              icon_electron, icon_ohm, icon_circuit, icon_power, icon_shield):
        f()


if __name__ == "__main__":
    main()
