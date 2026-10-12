"""덱 전체에서 공유하는 색상·폰트·크기 규칙.

색에는 의미가 있다 (그림과 슬라이드 모두 같은 규칙):
  VOLT  = 전압 (주황)      CURRENT = 전류·전자 (청록)
  RESIST = 저항·위험 (빨강)  SAFE = 정상·안전 (초록)
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT_DIR = ROOT / "content"
FIG_DIR = ROOT / "assets" / "figures"
ICON_DIR = ROOT / "assets" / "icons"
OUTPUT_DIR = ROOT / "output"
PREVIEW_DIR = ROOT / "preview"

# ── 색상 (hex, # 없이) ─────────────────────────────
INK = "1F2433"        # 본문 글자
INK_SOFT = "5B6378"   # 보조 글자
NIGHT = "141B2D"      # 어두운 슬라이드 배경 (표지·구분 슬라이드)
NIGHT_2 = "222B44"    # 어두운 배경 위 카드
PAPER = "FFFFFF"      # 밝은 슬라이드 배경
PANEL = "F3F5FA"      # 카드 배경
LINE = "D9DEE8"       # 옅은 테두리

SPARK = "FFC21A"      # 브랜드 강조색 (번개 노랑)
VOLT = "F29A07"       # 전압
CURRENT = "1FA2D8"    # 전류·전자
RESIST = "E5533D"     # 저항·위험
SAFE = "2BAE66"       # 안전·정상
WATER = "6EC6F0"      # 물 비유
WATER_DARK = "2E8BC0"
COPPER = "C8763A"     # 구리선
METAL = "A7AFBF"      # 금속 부품
GLOW = "FFE680"       # 켜진 전구 빛

# ── 폰트 ──────────────────────────────────────────
FONT = "Malgun Gothic"     # 한글 기본 (Windows 기본 탑재)
FONT_PPT = "맑은 고딕"

# ── 그림 크기 (인치) : 슬라이드 위 실제 크기와 같다 ──
# 그림 속 글자 pt = 슬라이드 위 글자 pt 이므로 본문 14pt 이상 유지
FIG_FULL = (12.0, 4.9)    # layout: full
FIG_SPLIT = (7.2, 5.3)    # layout: split (왼쪽 그림)
FIG_CARD_ICON = (1.6, 1.6)
FIG_SECTION_ICON = (3.0, 3.0)
DPI = 200


def rgb(hex_str):
    """'1F2433' -> (r, g, b) 0~1 (matplotlib 용)."""
    h = hex_str.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def mpl(hex_str):
    return "#" + hex_str.lstrip("#")
