"""섹션 3. 옴의 법칙 — 삼각형, 직관 비교, 계산 예시."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))
import draw_helpers as D  # noqa: E402
import style as S  # noqa: E402
from matplotlib.patches import Circle, Polygon  # noqa: E402

C = S.mpl


def ohm_tri(ax, cx, base_y, w, hgt, size, cover=None):
    """V/I/R 삼각형. cover='V'|'I'|'R' 이면 그 글자를 손가락(회색 판)으로 가림."""
    L, R, T = (cx - w / 2, base_y), (cx + w / 2, base_y), (cx, base_y + hgt)
    ax.add_patch(Polygon([L, R, T], closed=True, fc=C(S.PANEL), ec=C(S.INK), lw=max(2, size / 14),
                         zorder=3, joinstyle="round"))
    mid = base_y + hgt * 0.45
    half = (w / 2) * (1 - 0.45)
    ax.plot([cx - half, cx + half], [mid, mid], color=C(S.INK), lw=max(2, size / 14), zorder=4)
    pos = {"V": (cx, base_y + hgt * 0.66), "I": (cx - w * 0.2, base_y + hgt * 0.22),
           "R": (cx + w * 0.2, base_y + hgt * 0.22)}
    col = {"V": S.VOLT, "I": S.CURRENT, "R": S.RESIST}
    for k, (x, y) in pos.items():
        D.text(ax, x, y, k, size=size, color=col[k], weight="bold")
    D.text(ax, cx, base_y + hgt * 0.22, "×", size=size * 0.6, color=S.INK, weight="bold")
    if cover:
        x, y = pos[cover]
        s = size / 72 * 0.62
        D.box(ax, x - s, y - s, 2 * s, 2 * s, fc=S.INK_SOFT, r=s * 0.4, z=21)
        D.text(ax, x, y, "?", size=size * 0.8, color="FFFFFF", weight="bold", zorder=22)


# ── 03_ohm_triangle ─────────────────────────────
def triangle():
    w, h = S.FIG_SPLIT
    fig, ax = D.new_fig(w, h)
    ohm_tri(ax, 2.2, 1.05, 3.9, 3.7, 60)
    for x, s, col in ((1.0, "V 전압", S.VOLT), (2.2, "I 전류", S.CURRENT), (3.4, "R 저항", S.RESIST)):
        D.text(ax, x, 0.45, s, size=16, color=col, weight="bold")
    rows = (("V", "V = I × R"), ("I", "I = V ÷ R"), ("R", "R = V ÷ I"))
    for k, ((cov, formula), y) in enumerate(zip(rows, (3.85, 2.45, 1.05))):
        ohm_tri(ax, 4.95, y, 1.0, 0.95, 16, cover=cov)
        D.text(ax, 5.65, y + 0.4, formula, size=19, weight="bold", ha="left")
    D.save(fig, "03_ohm_triangle")


# ── 03_ohm_intuition ────────────────────────────
def mini_circuit(ax, x0, y0, batt_w, batt_label, brightness, res_len=None, wl=1.8, hl=1.8):
    """작은 회로: 아래 건전지, 위 전구, 왼쪽 변에 저항(선택), 오른쪽 변에 전류 화살표."""
    x1, y1 = x0 + wl, y0 + hl
    cx = x0 + wl / 2
    l_pt, r_pt = D.bulb(ax, cx, y1 + 0.55, r=0.38, lit=True, brightness=brightness)
    if brightness < 0.5:  # 어두운 전구: 유리를 옅게
        ax.add_patch(Circle((cx, y1 + 0.55), 0.37, fc="white", ec="none", alpha=0.55, zorder=6.5))
    neg, pos = D.battery(ax, cx, y0, w=batt_w, h=0.55, label=batt_label)
    D.wire(ax, [neg, (x0, y0), (x0, y1), (l_pt[0], y1), l_pt], lw=4)
    D.wire(ax, [r_pt, (r_pt[0], y1), (x1, y1), (x1, y0), pos], lw=4)
    if res_len:
        ym = y0 + hl / 2
        D.box(ax, x0 - 0.17, ym - res_len / 2, 0.34, res_len, fc=S.RESIST, r=0.06, z=7)
        D.text(ax, x0, ym, "R", size=14, color="FFFFFF", weight="bold", zorder=8)
    lw = 1.5 + 5 * brightness
    D.arrow(ax, x1 + 0.22, y0 + 0.4, x1 + 0.22, y1 - 0.3, color=S.CURRENT, lw=lw, head=8 + 8 * brightness)


def intuition():
    w, h = S.FIG_FULL
    fig, ax = D.new_fig(w, h)
    for px, head, fc in ((0.15, "전압 ↑  →  전류 ↑", S.VOLT), (6.05, "저항 ↑  →  전류 ↓", S.RESIST)):
        D.box(ax, px, 0.15, 5.8, 4.6, fc=S.PANEL, r=0.25)
        D.pill(ax, px + 2.9, 4.3, head, fc=fc, size=18)
    y0 = 0.85
    # 왼쪽: 전압을 키우면
    mini_circuit(ax, 0.75, y0, 1.0, "1.5V", 0.25)
    D.big_arrow(ax, 2.95, 1.9, 3.6, 1.9, width=0.28)
    mini_circuit(ax, 3.85, y0, 1.55, "9V", 1.0)
    # 오른쪽: 저항을 키우면
    mini_circuit(ax, 6.75, y0, 1.3, "9V", 1.0, res_len=0.4)
    D.big_arrow(ax, 8.85, 1.9, 9.5, 1.9, width=0.28)
    mini_circuit(ax, 9.75, y0, 1.3, "9V", 0.25, res_len=1.2)
    for x, s in ((1.65, "어둡게"), (4.75, "밝게"), (7.65, "밝게"), (10.65, "어둡게")):
        D.text(ax, x, 0.36, s, size=14, color=S.INK_SOFT, weight="bold")
    D.save(fig, "03_ohm_intuition")


# ── 03_ohm_example ──────────────────────────────
def zigzag(ax, x1, x2, y, amp=0.18, n=6, color=S.INK, lw=4):
    seg = (x2 - x1) / (n * 2)
    pts = [(x1, y)]
    for i in range(n * 2):
        pts.append((x1 + seg * (i + 0.5), y + (amp if i % 2 == 0 else -amp)))
    pts.append((x2, y))
    D.wire(ax, pts, color=color, lw=lw, z=6)


def example():
    w, h = S.FIG_SPLIT
    fig, ax = D.new_fig(w, h)
    L, R, B, T = 1.3, 5.9, 1.6, 4.35
    # 회로선 (건전지·저항·전류계 자리는 비움)
    by = (B + T) / 2
    D.wire(ax, [(L, by + 0.12), (L, T), (2.95, T)], lw=5)
    D.wire(ax, [(4.25, T), (R, T), (R, by + 0.38)], lw=5)
    D.wire(ax, [(R, by - 0.38), (R, B), (L, B), (L, by - 0.12)], lw=5)
    # 건전지 기호 (긴 선 = +)
    ax.plot([L - 0.42, L + 0.42], [by + 0.12, by + 0.12], color=C(S.INK), lw=5, zorder=6)
    ax.plot([L - 0.22, L + 0.22], [by - 0.12, by - 0.12], color=C(S.INK), lw=9, zorder=6)
    D.text(ax, L + 0.62, by + 0.32, "+", size=18, color=S.RESIST, weight="bold")
    D.pill(ax, L - 0.75, by, "9V", fc=S.VOLT, size=18)
    # 저항
    zigzag(ax, 2.95, 4.25, T, color=S.RESIST, lw=5)
    D.pill(ax, 3.6, T + 0.5, "3Ω", fc=S.RESIST, size=18)
    # 전류계
    ax.add_patch(Circle((R, by), 0.38, fc="white", ec=C(S.CURRENT), lw=4, zorder=7))
    D.text(ax, R, by, "?", size=22, color=S.CURRENT, weight="bold")
    D.text(ax, R - 0.65, by, "전류는?", size=15, color=S.CURRENT, weight="bold", ha="right")
    # 전류 화살표
    for x in (4.6, 3.3, 2.0):
        D.arrow(ax, x + 0.5, B - 0.25, x, B - 0.25, color=S.CURRENT, lw=3, head=12)
    # 계산 띠
    y = 0.55
    D.pill(ax, 1.4, y, "9V", fc=S.VOLT, size=19)
    D.text(ax, 2.2, y, "÷", size=24, weight="bold")
    D.pill(ax, 3.0, y, "3Ω", fc=S.RESIST, size=19)
    D.text(ax, 3.8, y, "=", size=24, weight="bold")
    D.pill(ax, 4.65, y, "3A", fc=S.CURRENT, size=19)
    D.save(fig, "03_ohm_example")


def main():
    triangle()
    intuition()
    example()


if __name__ == "__main__":
    main()
