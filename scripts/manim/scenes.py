"""manim 그래프 애니메이션 5개.

화면 = 12.0 x 4.9 (1 단위 = 슬라이드 위 1 인치). 슬라이드 제목 아래 영상 칸을 그대로 채운다.
LaTeX 가 없으므로 MathTex/DecimalNumber 대신 Text 만 쓴다.
렌더: python scripts/make_videos.py [장면이름]
"""
import sys
from pathlib import Path

import numpy as np
from manim import (DOWN, LEFT, RIGHT, UP, WHITE, Arrow, Axes, Circle, Create, DashedLine, Dot,
                   FadeIn, FadeOut, GrowArrow, Line, ReplacementTransform, Rectangle, RoundedRectangle, Scene,
                   Text, Transform, ValueTracker, VGroup, VMobject, always_redraw, config, linear,
                   smooth)

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))
import style as S  # noqa: E402

config.pixel_width = 1920
config.pixel_height = 784
config.frame_width = 12.0
config.frame_height = 4.9
config.frame_rate = 30
config.background_color = WHITE


def c(h):
    return "#" + h


INK, INK_SOFT = c(S.INK), c(S.INK_SOFT)
VOLT, CURRENT, RESIST, SAFE = c(S.VOLT), c(S.CURRENT), c(S.RESIST), c(S.SAFE)
SPARK, GLOW, WATER, PANEL, METAL = c(S.SPARK), c(S.GLOW), c(S.WATER), c(S.PANEL), c(S.METAL)
FONT = S.FONT


def T(s, size=26, color=INK, weight="NORMAL"):
    """한글 글자. size 22 ≈ 슬라이드 위 20pt."""
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def chip(s, fill, size=24, color=WHITE):
    t = T(s, size, color, "BOLD")
    bg = RoundedRectangle(corner_radius=0.12, width=t.width + 0.4, height=t.height + 0.24,
                          fill_color=fill, fill_opacity=1, stroke_width=0)
    t.move_to(bg)
    return VGroup(bg, t)


def axes(x_range, y_range, x_len, y_len, tips=True):
    return Axes(x_range=x_range, y_range=y_range, x_length=x_len, y_length=y_len, tips=tips,
                axis_config={"color": INK, "stroke_width": 3, "include_ticks": True,
                             "tip_width": 0.18, "tip_height": 0.18})


def electron(r=0.12):
    dot = Circle(radius=r, fill_color=CURRENT, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
    minus = Line(LEFT * r * 0.5, RIGHT * r * 0.5, color=WHITE, stroke_width=3)
    return VGroup(dot, minus)


# ─────────────────────────────────────────────────────────
class m01_electron_flow(Scene):
    """전선 고리를 따라 전자가 − 단자에서 나와 + 단자로 들어가고, 전구가 켜진다."""

    def construct(self):
        L, R, B, Tp = -4.6, 4.6, -1.35, 1.35
        bx = 0.9  # 건전지 반폭
        # 전자는 − 단자(왼쪽)에서 나와 고리를 한 바퀴 돌아 + 단자(오른쪽)로 들어간다
        path = VMobject(stroke_color=INK, stroke_width=6)
        path.set_points_as_corners([[-bx, B, 0], [L, B, 0], [L, Tp, 0], [R, Tp, 0], [R, B, 0], [bx, B, 0]])

        # 건전지 (가로, + 가 오른쪽)
        body = Rectangle(width=1.3, height=0.62, fill_color=INK, fill_opacity=1, stroke_width=0)
        body.move_to([-0.2, B, 0])
        band = Rectangle(width=0.42, height=0.62, fill_color=SPARK, fill_opacity=1, stroke_width=0)
        band.move_to([0.42 + 0.0, B, 0])
        cap = Rectangle(width=0.16, height=0.26, fill_color=METAL, fill_opacity=1, stroke_width=0)
        cap.move_to([0.71, B, 0])
        plus = T("+", 34, RESIST, "BOLD").move_to([0.62, B + 0.62, 0])
        minus = T("−", 34, INK_SOFT, "BOLD").move_to([-0.62, B + 0.62, 0])
        bat_label = T("건전지", 24, INK).move_to([0, B - 0.62, 0])
        battery = VGroup(body, band, cap, plus, minus, bat_label)

        # 전구 (위쪽 전선 가운데)
        glow = VGroup(*[Circle(radius=r, fill_color=SPARK, fill_opacity=o, stroke_width=0)
                        for r, o in ((0.72, 0.18), (0.56, 0.3))]).move_to([0, Tp, 0])
        glass = Circle(radius=0.42, fill_color="#E6E9F0", fill_opacity=1, stroke_color=INK, stroke_width=4)
        glass.move_to([0, Tp, 0])
        fil = VMobject(stroke_color=INK_SOFT, stroke_width=3)
        fil.set_points_as_corners([[-0.14, Tp - 0.2, 0], [-0.07, Tp + 0.08, 0], [0, Tp - 0.06, 0],
                                   [0.07, Tp + 0.08, 0], [0.14, Tp - 0.2, 0]])
        bulb_label = T("전구", 24, INK).move_to([1.15, Tp + 0.45, 0])
        # 겹침 순서: 빛 < 전선 < 전자 < 전구 유리 < 글자
        glow.set_z_index(0)
        path.set_z_index(1)
        VGroup(glass, fil).set_z_index(3)
        battery.set_z_index(3)

        self.play(Create(path), FadeIn(battery), FadeIn(glass), FadeIn(fil), FadeIn(bulb_label), run_time=1.6)

        # 전자 행진
        n = 22
        t = ValueTracker(0)
        els = VGroup(*[electron() for _ in range(n)]).set_z_index(2)

        def place(group):
            for k, e in enumerate(group):
                e.move_to(path.point_from_proportion((t.get_value() + k / n) % 1))

        els.add_updater(place)
        place(els)

        arrow = Arrow([-1.6, B + 0.75, 0], [-3.9, B + 0.75, 0], color=CURRENT, stroke_width=7,
                      buff=0, max_tip_length_to_length_ratio=0.15)
        label = T("전자의 이동", 30, CURRENT, "BOLD").next_to(arrow, UP, buff=0.18)
        hint = T("− 에서 나와 + 로 들어간다", 24, INK_SOFT).next_to(label, RIGHT, buff=0.6)

        self.play(FadeIn(els), run_time=0.5)
        self.play(t.animate.set_value(0.25), FadeIn(glow), glass.animate.set_fill(GLOW),
                  fil.animate.set_stroke(VOLT), GrowArrow(arrow), FadeIn(label),
                  run_time=1.5, rate_func=linear)
        self.play(t.animate.set_value(1.6), FadeIn(hint, run_time=1.0), run_time=6.5, rate_func=linear)
        els.clear_updaters()
        self.wait(1.5)


def GrowArrow(arrow):
    from manim import GrowArrow
    return GrowArrow(arrow)


# ─────────────────────────────────────────────────────────
class m03_ohm_graph(Scene):
    """전압을 올리면 전류가 비례해서 늘고, 저항에 따라 기울기가 달라진다."""

    def construct(self):
        ax = axes([0, 10, 1], [0, 5, 1], 6.0, 3.5)
        ax.move_to([-2.75, -0.12, 0])
        xt = VGroup(*[T(str(v), 22, INK_SOFT).next_to(ax.c2p(v, 0), DOWN, buff=0.14) for v in (0, 3, 6, 9)])
        yt = VGroup(*[T(str(v), 22, INK_SOFT).next_to(ax.c2p(0, v), LEFT, buff=0.14) for v in (1, 2, 3, 4)])
        xl = T("전압(V)", 24, VOLT, "BOLD").next_to(ax.x_axis.get_end(), RIGHT, buff=0.15)
        yl = T("전류(A)", 24, CURRENT, "BOLD").next_to(ax.y_axis.get_end(), RIGHT, buff=0.15)
        self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), run_time=1.4)

        v = ValueTracker(0.0)
        line3 = ax.plot(lambda x: x / 3, x_range=[0, 10], color=CURRENT, stroke_width=6)
        traced = always_redraw(lambda: ax.plot(lambda x: x / 3, x_range=[0, max(v.get_value(), 0.001)],
                                               color=CURRENT, stroke_width=6))
        dot = always_redraw(lambda: Dot(ax.c2p(v.get_value(), v.get_value() / 3), radius=0.1, color=CURRENT))
        guides = always_redraw(lambda: VGroup(
            DashedLine(ax.c2p(v.get_value(), 0), ax.c2p(v.get_value(), v.get_value() / 3),
                       color=VOLT, stroke_width=3, dash_length=0.08),
            DashedLine(ax.c2p(0, v.get_value() / 3), ax.c2p(v.get_value(), v.get_value() / 3),
                       color=CURRENT, stroke_width=3, dash_length=0.08)))

        px = 1.75  # 오른쪽 패널 왼쪽 끝
        r_text = T("저항 3Ω", 28, INK, "BOLD").move_to([px, 1.75, 0], aligned_edge=LEFT)
        v_text = always_redraw(lambda: T(f"전압 {v.get_value():.1f} V", 30, VOLT, "BOLD")
                               .move_to([px, 1.2, 0], aligned_edge=LEFT))
        i_text = always_redraw(lambda: T(f"전류 {v.get_value() / 3:.1f} A", 30, CURRENT, "BOLD")
                               .move_to([px, 0.65, 0], aligned_edge=LEFT))
        self.add(traced, guides, dot)
        self.play(FadeIn(r_text), FadeIn(v_text), FadeIn(i_text), run_time=0.6)
        self.play(v.animate.set_value(9), run_time=4.0, rate_func=smooth)

        result = chip("9V ÷ 3Ω = 3A", INK, 26).move_to([px, 0.0, 0], aligned_edge=LEFT)
        self.play(FadeIn(result, shift=UP * 0.15), run_time=0.6)
        self.wait(0.6)

        # 다른 저항 비교
        self.remove(traced)
        self.add(line3)
        line_lo = ax.plot(lambda x: x / 1.5, x_range=[0, 7.5], color=SAFE, stroke_width=6)
        line_hi = ax.plot(lambda x: x / 6, x_range=[0, 10], color=RESIST, stroke_width=6)
        tag3 = T("3Ω", 24, CURRENT, "BOLD").next_to(ax.c2p(10, 10 / 3), RIGHT, buff=0.1)

        def legend(color, s, y):
            seg = Line(np.zeros(3), RIGHT * 0.45, color=color, stroke_width=7)
            txt = T(s, 24, INK)
            g = VGroup(seg, txt).arrange(RIGHT, buff=0.18)
            return g.move_to([px, y, 0], aligned_edge=LEFT)

        lg_head = T("저항이 작을수록 가파르다", 22, INK_SOFT).move_to([px, -0.7, 0], aligned_edge=LEFT)
        lg_lo = legend(SAFE, "1.5Ω → 가파름", -1.2)
        lg_hi = legend(RESIST, "6Ω → 완만", -1.7)
        self.play(FadeOut(guides), FadeOut(dot), FadeIn(tag3), run_time=0.4)
        self.play(Create(line_lo), FadeIn(lg_head), FadeIn(lg_lo), run_time=1.4)
        self.play(Create(line_hi), FadeIn(lg_hi), run_time=1.4)
        self.wait(1.6)


# ─────────────────────────────────────────────────────────
class m06_dc_ac(Scene):
    """직류는 한 방향·일정, 교류는 방향이 계속 바뀐다."""

    def construct(self):
        t = ValueTracker(0.0)
        panels = []
        for cx, name, color, f, cap in (
                (-3.0, "직류 DC", INK, lambda x: 1.0, "한 방향 · 일정"),
                (3.0, "교류 AC", INK, lambda x: np.sin(2 * np.pi * 2.75 * x / 10), "방향이 계속 바뀜 (1초에 60번)")):
            bg = RoundedRectangle(corner_radius=0.18, width=5.6, height=4.6, fill_color=PANEL,
                                  fill_opacity=1, stroke_width=0).move_to([cx, 0, 0])
            head = chip(name, color, 26).move_to([cx, 1.88, 0])
            ax = axes([0, 10, 10], [-1.3, 1.3, 1], 4.2, 1.9)
            ax.move_to([cx - 0.3, 0.45, 0])
            tl = T("시간", 20, INK_SOFT).next_to(ax.x_axis.get_end(), RIGHT, buff=0.12)
            pl = T("+", 24, RESIST, "BOLD").next_to(ax.c2p(0, 1), LEFT, buff=0.12)
            mi = T("−", 24, INK_SOFT, "BOLD").next_to(ax.c2p(0, -1), LEFT, buff=0.12)
            wire = Line([cx - 2.1, -1.15, 0], [cx + 2.1, -1.15, 0], color=c(S.COPPER), stroke_width=10)
            capt = T(cap, 24, INK, "BOLD").move_to([cx, -1.85, 0])
            self.add(bg)
            panels.append(dict(ax=ax, f=f, cx=cx, parts=VGroup(head, ax, tl, pl, mi, wire, capt)))

        self.play(*[FadeIn(p["parts"]) for p in panels], run_time=1.2)

        for p in panels:
            ax, f, cx = p["ax"], p["f"], p["cx"]
            curve = always_redraw(lambda ax=ax, f=f: ax.plot(f, x_range=[0, max(t.get_value(), 0.001), 0.02],
                                                             color=CURRENT, stroke_width=6))
            dot = always_redraw(lambda ax=ax, f=f: Dot(ax.c2p(t.get_value(), f(t.get_value())),
                                                       radius=0.09, color=CURRENT))

            def arrow(ax=ax, f=f, cx=cx):
                s = f(t.get_value())
                if abs(s) < 0.12:
                    return VMobject()
                half = 1.6 * abs(s)
                d = 1 if s > 0 else -1
                return Arrow([cx - d * half, -1.15, 0], [cx + d * half, -1.15, 0], color=CURRENT,
                             stroke_width=9, buff=0, max_tip_length_to_length_ratio=0.3,
                             max_stroke_width_to_length_ratio=12)

            self.add(curve, dot, always_redraw(arrow))

        self.play(t.animate.set_value(10), run_time=8.5, rate_func=linear)
        self.wait(1.5)


# ─────────────────────────────────────────────────────────
class m07_capacitor(Scene):
    """커패시터 = 물통. 충전되며 차오르고, 방전되며 비워진다."""

    def construct(self):
        tau, t_split, t_end = 1.0, 5.0, 10.0
        t = ValueTracker(0.0)

        def volt(x):
            if x <= t_split:
                return 1 - np.exp(-x / tau)
            return (1 - np.exp(-t_split / tau)) * np.exp(-(x - t_split) / tau)

        # 왼쪽: 물통
        tx, tb, tw, th = -3.95, -1.35, 1.7, 2.5
        water = always_redraw(lambda: Rectangle(
            width=tw, height=max(th * volt(t.get_value()), 0.001), fill_color=WATER, fill_opacity=1,
            stroke_width=0).move_to([tx, tb, 0], aligned_edge=DOWN))
        walls = VMobject(stroke_color=INK, stroke_width=5)
        walls.set_points_as_corners([[tx - tw / 2, tb + th, 0], [tx - tw / 2, tb, 0],
                                     [tx + tw / 2, tb, 0], [tx + tw / 2, tb + th, 0]])
        tank_label = T("커패시터 = 물통", 22, INK).move_to([tx, tb - 0.38, 0])

        # 오른쪽: 전압-시간 그래프
        ax = axes([0, 10, 1], [0, 1.1, 1], 6.6, 3.2, tips=True)
        ax.move_to([1.85, -0.15, 0])
        yl = T("전압", 24, VOLT, "BOLD").next_to(ax.y_axis.get_end(), RIGHT, buff=0.15)
        xl = T("시간 →", 22, INK_SOFT).next_to(ax.x_axis.get_end(), DOWN, buff=0.12).shift(LEFT * 0.35)
        full = DashedLine(ax.c2p(0, 1), ax.c2p(10, 1), color=INK_SOFT, stroke_width=2, dash_length=0.1)
        full_l = T("가득", 20, INK_SOFT).next_to(ax.c2p(0, 1), LEFT, buff=0.22)

        self.play(Create(walls), FadeIn(tank_label), Create(ax), FadeIn(yl), FadeIn(xl),
                  FadeIn(full), FadeIn(full_l), run_time=1.3)
        self.add(water)

        charge = always_redraw(lambda: ax.plot(volt, x_range=[0, min(max(t.get_value(), 0.001), t_split), 0.02],
                                               color=CURRENT, stroke_width=6))
        dis = always_redraw(lambda: ax.plot(volt, x_range=[t_split, max(t.get_value(), t_split + 0.001), 0.02],
                                            color=VOLT, stroke_width=6) if t.get_value() > t_split else VMobject())
        dot = always_redraw(lambda: Dot(ax.c2p(t.get_value(), volt(t.get_value())), radius=0.09,
                                        color=CURRENT if t.get_value() <= t_split else VOLT))
        self.add(charge, dis, dot)

        phase = chip("충전 중", CURRENT, 24).move_to([tx, 1.75, 0])
        inflow = VGroup(Arrow([tx - 1.45, 1.25, 0], [tx - 0.5, 0.75, 0], color=CURRENT, stroke_width=8, buff=0),
                        T("모으기", 22, CURRENT, "BOLD").move_to([tx - 1.4, 1.6, 0]))
        outflow = VGroup(Arrow([tx + tw / 2 + 0.05, tb + 0.3, 0], [tx + tw / 2 + 1.0, tb + 0.3, 0], color=VOLT,
                               stroke_width=8, buff=0),
                         T("내보내기", 22, VOLT, "BOLD").move_to([tx + tw / 2 + 0.8, tb + 0.7, 0]))
        self.play(FadeIn(phase), FadeIn(inflow), run_time=0.4)
        self.play(t.animate.set_value(t_split), run_time=3.6, rate_func=linear)
        c_lab = T("충전", 26, CURRENT, "BOLD").move_to(ax.c2p(2.6, 0.55))
        self.play(FadeIn(c_lab), run_time=0.3)

        phase2 = chip("방전 중", VOLT, 24).move_to([tx, 1.75, 0])
        self.play(Transform(phase, phase2), FadeOut(inflow), FadeIn(outflow), run_time=0.4)
        self.play(t.animate.set_value(t_end), run_time=3.6, rate_func=linear)
        d_lab = T("방전", 26, VOLT, "BOLD").move_to(ax.c2p(7.6, 0.55))
        self.play(FadeIn(d_lab), run_time=0.3)
        self.wait(1.5)


# ─────────────────────────────────────────────────────────
class m09_charger_waveforms(Scene):
    """충전기 속에서 교류 220V 가 직류 5V 로 바뀌는 과정."""

    def construct(self):
        steps = ["① 콘센트", "② 변압기", "③ 다이오드", "④ 커패시터", "⑤ 트랜지스터"]
        caps = ["교류 220V", "전압 낮추기", "한 방향으로", "매끈하게", "딱 5V"]
        cols = [CURRENT, CURRENT, SAFE, CURRENT, VOLT]
        w, gap = 2.05, 0.22
        x0 = -(5 * w + 4 * gap) / 2 + w / 2

        def chips(active):
            g = VGroup()
            for i, s in enumerate(steps):
                on = i == active
                bg = RoundedRectangle(corner_radius=0.14, width=w, height=0.62,
                                      fill_color=INK if on else PANEL, fill_opacity=1, stroke_width=0)
                txt = T(s, 22, WHITE if on else INK_SOFT, "BOLD" if on else "NORMAL").move_to(bg)
                g.add(VGroup(bg, txt).move_to([x0 + i * (w + gap), 1.95, 0]))
            return g

        ax = axes([0, 4 * np.pi, np.pi], [-1.2, 1.2, 1], 9.6, 2.7, tips=True)
        ax.move_to([0, -0.15, 0])
        zero_l = T("0", 20, INK_SOFT).next_to(ax.c2p(0, 0), LEFT, buff=0.12)
        tl = T("시간 →", 20, INK_SOFT).next_to(ax.x_axis.get_end(), DOWN, buff=0.1).shift(LEFT * 0.3)

        def ripple(x):
            p = np.pi
            return 0.5 - 0.12 * ((x % p) / p)

        fns = [lambda x: 1.0 * np.sin(x), lambda x: 0.5 * np.sin(x), lambda x: abs(0.5 * np.sin(x)),
               ripple, lambda x: 0.42]

        def curve(i):
            return ax.plot(fns[i], x_range=[0, 4 * np.pi, 0.01], color=cols[i], stroke_width=6,
                           use_smoothing=False)

        def caption(i):
            return T(caps[i], 30, cols[i], "BOLD").move_to([0, -1.95, 0])

        ch = chips(0)
        cv = curve(0)
        cp = caption(0)
        self.play(FadeIn(ch), Create(ax), FadeIn(zero_l), FadeIn(tl), run_time=1.0)
        self.play(Create(cv), FadeIn(cp), run_time=1.4)
        self.wait(0.5)
        for i in range(1, 5):
            new_cv, new_cp = curve(i), caption(i)
            self.play(Transform(ch, chips(i)), ReplacementTransform(cv, new_cv),
                      ReplacementTransform(cp, new_cp), run_time=1.3)
            cv, cp = new_cv, new_cp
            self.wait(0.6)
        five = T("5V", 26, VOLT, "BOLD").next_to(ax.c2p(4 * np.pi, 0.42), UP, buff=0.12).shift(LEFT * 0.3)
        final = T("휴대폰으로 → 직류 5V", 30, VOLT, "BOLD").move_to([0, -1.95, 0])
        self.play(FadeIn(five), ReplacementTransform(cp, final), run_time=0.8)
        self.wait(1.6)
