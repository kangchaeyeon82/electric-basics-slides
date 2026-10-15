# 전자전기 기초 특강 (비전공자용)

전기·전자를 처음 접하는 사람을 위한 **48장짜리 PowerPoint 강의 자료**입니다.
수식 대신 **물 비유와 그림**으로 전기의 기본기를 설명합니다. 그림은 Python 코드로 직접 그렸고, 핵심 그래프 5개는 **manim 애니메이션 영상**으로 넣었습니다.

👉 완성본: [`output/전자전기기초_특강.pptx`](output/전자전기기초_특강.pptx) (슬라이드마다 발표자 노트에 설명 대본 포함)

| 파일 | 내용 |
|------|------|
| [`전자전기기초_특강.pptx`](output/전자전기기초_특강.pptx) | **최신 48장** — 클릭 애니메이션 + manim 그래프 영상 5개 |
| [`전자전기기초_특강_v1.pptx`](output/전자전기기초_특강_v1.pptx) | 첫 버전 45장 — 애니메이션·영상 없는 정적 버전 (인쇄·PDF용으로 편리) |

| | |
|---|---|
| ![표지](docs/cover.png) | ![물 비유](docs/water.png) |
| ![옴의 법칙 그래프 영상](docs/ohm_graph.png) | ![충전기 파형 영상](docs/charger_wave.png) |
| ![다이오드](docs/diode.png) | ![충전기](docs/charger.png) |

## 강의 구성
| # | 섹션 | 핵심 메시지 |
|---|------|------------|
| 01 | 전기의 정체 | 전기 = 전자의 이동, 금속은 잘 흐르고 고무는 막는다 |
| 02 | 전압·전류·저항 | 미는 힘 · 흐르는 양 · 방해하는 정도 (물탱크 · 물줄기 · 좁은 관) |
| 03 | 옴의 법칙 | V = I × R — 세게 밀면 많이, 많이 막으면 적게 흐른다 |
| 04 | 회로 | 닫혀야 흐른다, 직렬과 병렬, 우리 집은 병렬 |
| 05 | 전력과 전기요금 | W = V × A, 요금은 전력 × 시간 (kWh) |
| 06 | 직류와 교류 | 건전지는 한 방향, 콘센트는 1초에 60번 방향 전환 |
| 07 | 전자 부품 5총사 | 저항 · 커패시터 · 다이오드 · LED · 트랜지스터 |
| 08 | 전기 안전 | 작은 전류도 위험, 누전차단기가 지켜 준다 |
| — | 정리 | 휴대폰 충전기 속 5단계, 핵심 요약, O/X 퀴즈 |

색 규칙: 🟧 전압 · 🟦 전류 · 🟥 저항/위험 · 🟩 안전

## 애니메이션
| 종류 | 들어간 곳 | 동작 |
|------|----------|------|
| 클릭 애니메이션 | 오른쪽 포인트 카드, 아이콘 카드, 퀴즈 정답 (21장) | 클릭할 때마다 하나씩 페이드인 |
| manim 그래프 영상 | 5장 (아래 표) | 슬라이드가 열리면 자동 재생 |
| Google Flow 배경 사진 | 표지·마무리·섹션 구분 (10장) | 이미지를 넣으면 배경으로 자동 적용 ([프롬프트](content/flow_prompts.md)) |

| 슬라이드 | 영상 | 내용 |
|---------|------|------|
| 5 전기 = 전자의 행진 | `m01_electron_flow` | 전자가 회로를 돌고 전구가 켜짐 |
| 16 그래프로 보는 옴의 법칙 | `m03_ohm_graph` | 전압 0→9V를 올리면 전류가 0→3A, 저항별 기울기 비교 |
| 29 직류와 교류 | `m06_dc_ac` | 직류·교류 파형과 전류 방향 화살표 |
| 34 커패시터의 충전과 방전 | `m07_capacitor` | 물통 수위와 전압 그래프가 함께 오르내림 |
| 44 충전기 속 파형의 변신 | `m09_charger_waveforms` | 교류 → 변압 → 정류 → 평활 → 직류 5V |

> Google Flow 이미지는 아직 들어 있지 않습니다. [`content/flow_prompts.md`](content/flow_prompts.md)의 프롬프트로 생성해 `assets/flow/`에 넣고 다시 빌드하면 됩니다. 이미지가 없으면 기본 디자인(남색 배경 + 아이콘)이 쓰입니다.

## 폴더
```
content/          강의 기획서(outline.md), 슬라이드 내용(slides.yaml), Flow 프롬프트(flow_prompts.md)
scripts/
  common/         색상·폰트 스타일, 공통 도형 함수 (전구, 건전지, 물탱크 …)
  figures/        섹션별 그림 생성 코드 (fig_00 ~ fig_09)
  manim/          그래프 애니메이션 장면 (scenes.py)
  make_figures.py 그림 전부(또는 일부) 다시 그리기
  make_videos.py  manim 영상 전부(또는 일부) 다시 렌더링
  anim.py         슬라이드 애니메이션(OOXML timing) 생성
  build_deck.py   slides.yaml + 그림 + 영상 → pptx 조립
  build_all.py    그림 → 영상 → pptx 를 한 번에
  preview.ps1     PowerPoint로 슬라이드 미리보기 PNG 생성
assets/
  figures/ icons/ 코드로 그린 그림·아이콘 (자동 생성)
  videos/         manim 영상 mp4 + 포스터 png (자동 생성)
  flow/           Google Flow 배경 사진 (직접 넣음)
output/           완성된 pptx
```

## 사용한 외부 도구
| 도구 | 용도 | 필수 여부 |
|------|------|----------|
| [Python](https://www.python.org/) 3.10+ | 모든 스크립트 실행 | 필수 |
| [matplotlib](https://matplotlib.org/) | 그림·아이콘을 코드로 그려 PNG로 저장 (`scripts/figures/`) | 필수 |
| [python-pptx](https://python-pptx.readthedocs.io/) | pptx 조립, 막대 차트·영상·발표자 노트 삽입 | 필수 |
| [PyYAML](https://pyyaml.org/) | `content/slides.yaml` 읽기 | 필수 |
| [manim](https://www.manim.community/) (Community Edition) | 그래프 애니메이션 영상 렌더링 (`scripts/manim/`). LaTeX 없이 `Text`만 사용 | 영상을 다시 만들 때 필수 |
| 맑은 고딕 (Malgun Gothic) | 그림·영상·슬라이드의 한글 글꼴 (Windows 기본 탑재) | 필수 |
| [Google Flow](https://labs.google/flow) | 표지·섹션 배경 사진 생성 (프롬프트만 제공, 직접 생성) | 선택 |
| Microsoft PowerPoint | `scripts/preview.ps1`이 COM으로 pptx를 열어 슬라이드를 PNG로 내보냄 (검수용) | 선택 (Windows) |
| [GitHub CLI](https://cli.github.com/) (`gh`) | 이 저장소 생성·업로드 | 선택 |
| [Claude Code](https://claude.com/claude-code) | 기획, 그림·영상 코드, 조립 스크립트 작성과 미리보기 검수 | 제작 시 사용 |

외부 웹 API나 유료 서비스, 저작권 있는 이미지는 쓰지 않았습니다. 그림과 영상은 모두 이 저장소의 코드로 다시 만들 수 있습니다.

## 빌드
```
pip install -r requirements.txt
python scripts/build_all.py              # 그림 → 영상(약 3분) → pptx
python scripts/build_all.py --no-videos  # 영상은 그대로 두고 그림·pptx만
```

## 부분 수정
- 문구만: `content/slides.yaml` 수정 → `python scripts/build_deck.py`
- 그림만: `scripts/figures/fig_07_*.py` 수정 → `python scripts/make_figures.py 07` → `python scripts/build_deck.py`
- 영상만: `scripts/manim/scenes.py` 수정 → `python scripts/make_videos.py m03_ohm_graph` → `python scripts/build_deck.py`
- 애니메이션 끄기: 해당 슬라이드에 `static: true`
- 미리보기(Windows + PowerPoint 필요): `powershell -ExecutionPolicy Bypass -File scripts\preview.ps1` → `preview/`
