"""그림 스크립트들이 공유하는 matplotlib 도형 함수.

좌표계: new_fig(w, h) 로 만든 축은 x 0~w, y 0~h (단위 = 인치).
그래서 그림 속 크기·글자 pt 가 슬라이드 위 실제 크기와 같다.
"""
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Polygon

sys.path.insert(0, str(Path(__file__).resolve().parent))
import style as S  # noqa: E402

plt.rcParams["font.family"] = [S.FONT, "DejaVu Sans"]  # − 기호 등은 DejaVu 로 대체
plt.rcParams["axes.unicode_minus"] = False

C = S.mpl  # 'F29A07' -> '#F29A07'


# ── 캔버스 ─────────────────────────────────────────
def new_fig(w, h):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name, folder=None):
    """assets/figures/<name>.png 로 저장 (투명 배경)."""
    folder = Path(folder) if folder else S.FIG_DIR
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{name}.png"
    fig.savefig(path, dpi=S.DPI, transparent=True)
    plt.close(fig)
    print("  saved", path.name)
    return path


# ── 글자 ───────────────────────────────────────────
def text(ax, x, y, s, size=16, color=S.INK, weight="normal", ha="center", va="center", **kw):
    return ax.text(x, y, s, fontsize=size, color=C(color), fontweight=weight,
                   ha=ha, va=va, zorder=kw.pop("zorder", 20), **kw)


def pill(ax, x, y, s, fc=S.INK, tc=S.PAPER, size=15, pad=0.12, weight="bold"):
    """둥근 이름표 (x, y = 중심)."""
    return ax.text(x, y, s, fontsize=size, color=C(tc), fontweight=weight, ha="center", va="center",
                   zorder=25, bbox=dict(boxstyle=f"round,pad={pad * 3}", fc=C(fc), ec="none"))


def box(ax, x, y, w, h, fc=S.PANEL, ec=None, lw=0, r=0.15, z=1, alpha=1.0):
    """둥근 사각형 (x, y = 왼쪽 아래)."""
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       fc=C(fc), ec=C(ec) if ec else "none", lw=lw, zorder=z, alpha=alpha)
    ax.add_patch(p)
    return p


# ── 선·화살표 ──────────────────────────────────────
def wire(ax, pts, color=S.INK, lw=5, z=3):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=C(color), lw=lw, solid_capstyle="round", solid_joinstyle="round", zorder=z)


def arrow(ax, x1, y1, x2, y2, color=S.CURRENT, lw=4, head=18, z=10, style="-|>", rad=0.0):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=f"{style},head_length={head / 30},head_width={head / 50}",
                        color=C(color), lw=lw, zorder=z, connectionstyle=f"arc3,rad={rad}",
                        shrinkA=0, shrinkB=0, mutation_scale=20)
    ax.add_patch(a)
    return a


def big_arrow(ax, x1, y1, x2, y2, color=S.INK_SOFT, width=0.35, z=5):
    """속이 찬 굵은 화살표 (단계 흐름도용)."""
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    hl = min(width * 1.4, L * 0.5)
    ax.add_patch(patches.FancyArrow(x1, y1, dx, dy, width=width, head_width=width * 2.0, head_length=hl,
                                    length_includes_head=True, fc=C(color), ec="none", zorder=z))


# ── 전자 ───────────────────────────────────────────
def electron(ax, x, y, r=0.13, color=S.CURRENT, z=12, sign=True):
    ax.add_patch(Circle((x, y), r, fc=C(color), ec="white", lw=1.5, zorder=z))
    if sign:
        ax.text(x, y + r * 0.08, "−", fontsize=r * 85, color="white", ha="center", va="center",
                fontweight="bold", zorder=z + 1)


def electrons_along(ax, pts, n, r=0.11, color=S.CURRENT, offset=0.0, sign=False):
    """꺾인선 pts 위에 전자 n 개를 고르게 배치."""
    segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    lens = [math.dist(a, b) for a, b in segs]
    total = sum(lens)
    for k in range(n):
        d = (offset + (k + 0.5) * total / n) % total
        for (a, b), L in zip(segs, lens):
            if d <= L:
                t = d / L if L else 0
                electron(ax, a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, r=r, color=color, sign=sign)
                break
            d -= L


# ── 회로 부품 (그림 스타일) ────────────────────────
def battery(ax, cx, cy, w=1.5, h=0.7, label="1.5V", vertical=False, z=6):
    """건전지 그림. 기본은 가로(+ 단자가 오른쪽)."""
    if vertical:
        box(ax, cx - h / 2, cy - w / 2, h, w * 0.88, fc=S.INK, r=0.08, z=z)
        box(ax, cx - h / 2, cy + w / 2 - w * 0.12 - w * 0.3, h, w * 0.3, fc=S.SPARK, r=0.0, z=z + 1)
        box(ax, cx - h * 0.18, cy + w / 2 - w * 0.12, h * 0.36, w * 0.12, fc=S.METAL, r=0.04, z=z)
        text(ax, cx + h * 0.9, cy + w * 0.3, "+", size=20, weight="bold", color=S.RESIST)
        text(ax, cx + h * 0.9, cy - w * 0.35, "−", size=20, weight="bold", color=S.INK_SOFT)
        if label:
            text(ax, cx, cy - w * 0.1, label, size=12, color="FFFFFF", weight="bold", rotation=90)
        return (cx, cy + w / 2), (cx, cy - w / 2)
    box(ax, cx - w / 2, cy - h / 2, w * 0.88, h, fc=S.INK, r=0.08, z=z)
    box(ax, cx - w / 2 + w * 0.88 - w * 0.3, cy - h / 2, w * 0.3, h, fc=S.SPARK, r=0.0, z=z + 1)
    box(ax, cx - w / 2 + w * 0.88, cy - h * 0.18, w * 0.12, h * 0.36, fc=S.METAL, r=0.04, z=z)
    text(ax, cx + w * 0.3, cy + h * 0.95, "+", size=20, weight="bold", color=S.RESIST)
    text(ax, cx - w * 0.4, cy + h * 0.95, "−", size=20, weight="bold", color=S.INK_SOFT)
    if label:
        text(ax, cx - w * 0.12, cy, label, size=13, color="FFFFFF", weight="bold")
    return (cx - w / 2, cy), (cx + w / 2, cy)  # (− 단자, + 단자)


def bulb(ax, cx, cy, r=0.45, lit=True, brightness=1.0, z=6):
    """전구 그림. (cx, cy) = 유리구 중심. 반환값: 아래 소켓 좌/우 연결점."""
    if lit and brightness > 0:
        for k, a in ((2.3, 0.18), (1.75, 0.28)):
            ax.add_patch(Circle((cx, cy), r * k * (0.6 + 0.4 * brightness), fc=C(S.GLOW),
                                ec="none", alpha=a * brightness, zorder=z - 1))
        for i in range(8):
            ang = math.radians(90 + i * 45 - 0)
            if i == 4:
                continue
            L1, L2 = r * 1.35, r * (1.35 + 0.55 * brightness)
            ax.plot([cx + L1 * math.cos(ang), cx + L2 * math.cos(ang)],
                    [cy + L1 * math.sin(ang), cy + L2 * math.sin(ang)],
                    color=C(S.SPARK), lw=3.5, solid_capstyle="round", zorder=z - 1)
    glass = S.GLOW if lit and brightness > 0 else "E6E9F0"
    ax.add_patch(Circle((cx, cy), r, fc=C(glass), ec=C(S.INK), lw=2.5, zorder=z))
    # 필라멘트
    fil = S.VOLT if lit and brightness > 0 else S.INK_SOFT
    ax.plot([cx - r * 0.3, cx - r * 0.15, cx, cx + r * 0.15, cx + r * 0.3],
            [cy - r * 0.55, cy + r * 0.1, cy - r * 0.15, cy + r * 0.1, cy - r * 0.55],
            color=C(fil), lw=2.2, zorder=z + 1)
    # 소켓
    bw, bh = r * 0.9, r * 0.6
    box(ax, cx - bw / 2, cy - r * 0.85 - bh, bw, bh, fc=S.METAL, ec=S.INK, lw=2, r=0.04, z=z + 2)
    for k in range(1, 3):
        yy = cy - r * 0.85 - bh * k / 3
        ax.plot([cx - bw / 2, cx + bw / 2], [yy, yy], color=C(S.INK), lw=1.2, zorder=z + 3)
    yb = cy - r * 0.85 - bh
    return (cx - bw * 0.3, yb), (cx + bw * 0.3, yb)


def switch(ax, x1, x2, y, closed=True, color=S.INK, lw=5, z=6):
    """스위치: x1~x2 구간. closed=False 면 레버가 들려 있음."""
    for x in (x1, x2):
        ax.add_patch(Circle((x, y), 0.09, fc="white", ec=C(color), lw=2.5, zorder=z + 1))
    if closed:
        ax.plot([x1, x2], [y, y], color=C(color), lw=lw, solid_capstyle="round", zorder=z)
    else:
        L = x2 - x1
        ang = math.radians(32)
        ax.plot([x1, x1 + L * math.cos(ang)], [y, y + L * math.sin(ang)],
                color=C(color), lw=lw, solid_capstyle="round", zorder=z)


# ── 물 비유 ────────────────────────────────────────
def tank(ax, x, y, w, h, level=0.7, z=4):
    """물탱크 (x, y = 왼쪽 아래). level: 0~1 수위."""
    ax.add_patch(patches.Rectangle((x, y), w, h * level, fc=C(S.WATER), ec="none", zorder=z))
    ax.plot([x, x, x + w, x + w], [y + h, y, y, y + h], color=C(S.INK), lw=3, zorder=z + 1,
            solid_joinstyle="round")
    # 물결
    xs = [x + w * i / 40 for i in range(41)]
    ys = [y + h * level + 0.04 * math.sin(i / 2.2) for i in range(41)]
    ax.plot(xs, ys, color=C(S.WATER_DARK), lw=2, zorder=z + 1)


def pipe(ax, x1, x2, y, d=0.4, water=True, z=4):
    """가로 파이프. d = 굵기."""
    if water:
        ax.add_patch(patches.Rectangle((x1, y - d / 2), x2 - x1, d, fc=C(S.WATER), ec="none", zorder=z))
    ax.plot([x1, x2], [y + d / 2, y + d / 2], color=C(S.INK), lw=3, zorder=z + 1)
    ax.plot([x1, x2], [y - d / 2, y - d / 2], color=C(S.INK), lw=3, zorder=z + 1)


def drop(ax, x, y, s=0.18, color=S.WATER_DARK, z=8):
    """물방울 하나."""
    pts = [(x, y + s * 1.4)]
    for i in range(0, 181, 15):
        a = math.radians(i)
        pts.append((x + s * math.cos(a + math.pi), y + s * math.sin(a + math.pi)))
    ax.add_patch(Polygon(pts, closed=True, fc=C(color), ec="none", zorder=z))


# ── 사람·기타 ──────────────────────────────────────
def person(ax, x, y, h=2.0, color=S.INK_SOFT, z=6):
    """단순한 사람 실루엣. (x, y) = 발 중앙."""
    hr = h * 0.11
    ax.add_patch(Circle((x, y + h - hr), hr, fc=C(color), ec="none", zorder=z))
    box(ax, x - h * 0.14, y + h * 0.36, h * 0.28, h * 0.4, fc=color, r=h * 0.08, z=z)
    for dx in (-0.06, 0.06):
        box(ax, x + dx * h - h * 0.05, y, h * 0.1, h * 0.42, fc=color, r=h * 0.04, z=z)


def icon_circle(ax, cx, cy, r, fc=S.SPARK, z=2):
    ax.add_patch(Circle((cx, cy), r, fc=C(fc), ec="none", zorder=z))


def bolt(ax, cx, cy, h=1.0, color=S.SPARK, z=8, ec=None):
    """번개 모양."""
    w = h * 0.6
    pts = [(0.15, 1.0), (-0.35, 0.05), (0.02, 0.05), (-0.15, -1.0), (0.35, -0.05), (-0.02, -0.05)]
    pts = [(cx + px * w, cy + py * h / 2) for px, py in pts]
    ax.add_patch(Polygon(pts, closed=True, fc=C(color), ec=C(ec) if ec else "none", lw=2, zorder=z,
                         joinstyle="round"))
