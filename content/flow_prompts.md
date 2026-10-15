# Google Flow 이미지 프롬프트

표지·마무리·섹션 구분 슬라이드의 **배경 사진** 10장입니다.
원리를 설명하는 그림은 정확해야 하므로 코드로 그린 그림을 그대로 씁니다.

## 만드는 방법
1. [Google Flow](https://labs.google/flow)에서 이미지 생성을 선택하고 **가로 16:9** 비율로 설정
2. 아래 프롬프트를 그대로 붙여 넣기 (영어 프롬프트가 결과가 더 안정적입니다)
3. 마음에 드는 결과를 내려받아 **표의 파일명 그대로** `assets/flow/` 폴더에 저장 (png·jpg·webp 모두 가능)
4. `python scripts/build_deck.py` 실행 → 파일이 있는 슬라이드만 자동으로 배경 사진으로 바뀜

파일이 없으면 지금의 기본 디자인(남색 배경 + 코드로 그린 아이콘)이 그대로 쓰입니다.
슬라이드 제목이 왼쪽에 오고 그 위에 어두운 덮개가 씌워지므로, **주인공은 오른쪽에, 왼쪽은 어둡고 비어 있게** 만드는 것이 핵심입니다.

## 공통 스타일 (모든 프롬프트 끝에 붙어 있음)
> cinematic photograph, deep navy blue and warm electric yellow color palette, soft glow, shallow depth of field, main subject on the right third, left half dark and empty for text, no text, no letters, no logos, no watermark, 16:9

## 프롬프트
| 파일명 | 슬라이드 | 프롬프트 |
|--------|---------|---------|
| `flow_cover` | 1 표지 | A single glowing vintage light bulb hanging in a dark room, a thin bright filament and tiny sparks of electricity around it, faint circuit-board lines fading into the darkness, cinematic photograph, deep navy blue and warm electric yellow color palette, soft glow, shallow depth of field, main subject on the right third, left half dark and empty for text, no text, no letters, no logos, no watermark, 16:9 |
| `flow_sec01` | 01 전기의 정체 | Macro view of glowing particles flowing like a stream of light through a translucent copper wire, abstract atoms with orbiting points of blue light, cinematic photograph, deep navy blue and warm electric yellow color palette, soft glow, shallow depth of field, main subject on the right third, left half dark and empty for text, no text, no letters, no logos, no watermark, 16:9 |
| `flow_sec02` | 02 전압·전류·저항 | A tall water tower and a clear pipe with rushing water at night, water glowing faintly blue with tiny electric sparks inside the stream, metaphor of electricity as flowing water, cinematic photograph, deep navy blue and warm electric yellow color palette, soft glow, shallow depth of field, main subject on the right third, left half dark and empty for text, no text, no letters, no logos, no watermark, 16:9 |
| `flow_sec03` | 03 옴의 법칙 | Close-up of a single electronic resistor with colored bands on a dark workbench, a soft beam of light passing through it and becoming dimmer on the other side, cinematic photograph, deep navy blue and warm electric yellow color palette, soft glow, shallow depth of field, main subject on the right third, left half dark and empty for text, no text, no letters, no logos, no watermark, 16:9 |
| `flow_sec04` | 04 회로의 기초 | A hand-made circuit on a wooden desk: a battery, copper wires and a small glowing light bulb forming a closed loop, warm light spilling on the desk, cinematic photograph, deep navy blue and warm electric yellow color palette, soft glow, shallow depth of field, main subject on the right third, left half dark and empty for text, no text, no letters, no logos, no watermark, 16:9 |
| `flow_sec05` | 05 전력과 전기요금 | A cozy apartment at night seen from outside, windows lit warmly, an electric meter glowing on the wall in the foreground, cinematic photograph, deep navy blue and warm electric yellow color palette, soft glow, shallow depth of field, main subject on the right third, left half dark and empty for text, no text, no letters, no logos, no watermark, 16:9 |
| `flow_sec06` | 06 직류와 교류 | High-voltage power lines and a transmission tower at dusk with a faint glowing wave of energy running along the cables, cinematic photograph, deep navy blue and warm electric yellow color palette, soft glow, shallow depth of field, main subject on the right third, left half dark and empty for text, no text, no letters, no logos, no watermark, 16:9 |
| `flow_sec07` | 07 전자 부품 5총사 | Macro photograph of a green printed circuit board with tiny capacitors, a black transistor and a lit red LED, golden solder joints catching the light, cinematic photograph, deep navy blue and warm electric yellow color palette, soft glow, shallow depth of field, main subject on the right third, left half dark and empty for text, no text, no letters, no logos, no watermark, 16:9 |
| `flow_sec08` | 08 전기 안전 | A modern home circuit breaker panel with switches, softly lit, a small green indicator light glowing, calm and safe atmosphere, cinematic photograph, deep navy blue and warm electric yellow color palette, soft glow, shallow depth of field, main subject on the right third, left half dark and empty for text, no text, no letters, no logos, no watermark, 16:9 |
| `flow_end` | 마지막 감사합니다 | A smartphone charging on a bedside table at night, the charger cable glowing softly, warm lamp light, peaceful mood, cinematic photograph, deep navy blue and warm electric yellow color palette, soft glow, shallow depth of field, main subject on the right third, left half dark and empty for text, no text, no letters, no logos, no watermark, 16:9 |

## 검수 체크리스트
- 사진 속에 **글자·숫자·로고가 없는지** (AI 이미지는 엉터리 글자를 넣는 경우가 많음 → 다시 생성)
- 주인공이 **오른쪽**에 있고 왼쪽이 어두운지 (제목이 잘 읽히는지)
- 10장의 색감이 서로 비슷한지 (남색 + 노란 빛)
- 감전·화재처럼 겁을 주는 장면이 아닌지 (안전 섹션도 "안심" 분위기로)
