# #001 GPT-6 아스트라 — 뭐가 달라졌을까?

- 길이 28.1초 · 1080x1920 · 30fps · 무음 → 음성은 캡컷 '텍스트 읽기'로 입힘 (아래 참고)
- 렌더: `python3 shorts/_assets/render.py shorts/001-gpt6-astra/episode.html`
  - 결과물: `001-gpt6-astra.mp4`(자막 포함), `001-gpt6-astra_nocap.mp4`(자막 없음), `001-gpt6-astra.srt`
  - 디자인만 빠르게 확인: 뒤에 `--still` (비트별 PNG → `stills/`)

## 레이아웃 (레퍼런스 쇼츠 구조)
- 상단 검정 헤더 바: 질문형 제목 고정 + 진행 바
- 가운데: 비트마다 큰 비주얼 하나
- 하단: 외곽선 굵은 자막 (존댓말, 강조 단어 라임/레드)

## 비트 & 자막
| # | 초 | 비주얼 | 자막 |
|---|---|---|---|
| 1 | 1.8 | GPT-6 Astra 로고타입 | 드디어 GPT의 신모델 |
| 2 | 1.8 | 큰 물음표 | 뭐가 그렇게 달라졌을까요? |
| 3 | 2.4 | 달력 09.03 | 9월 3일, 프리뷰로 먼저 공개됐고요 |
| 4 | 2.1 | 요금제 칩 + API | 유료 플랜 과 API 로 쓸 수 있어요 |
| 5 | 2.3 | 브라우저 자동 입력 | 가장 큰 변화, 컴퓨터를 직접 조작 해요 |
| 6 | 2.5 | 체크리스트 | 양식 입력, CRM 업데이트, 일정 정리까지 |
| 7 | 2.1 | DOCX/XLSX/PPTX | 문서·엑셀·PPT 도 알아서 만들고 |
| 8 | 2.1 | 검색 → 요약 | 리서치해서 요약 초안 까지 써줘요 |
| 9 | 2.1 | 작업 중 지시 변경 | 일하는 도중에 지시를 바꿔도 되고 |
| 10 | 2.1 | 완료 작업 유지 | 이미 끝낸 작업은 그대로 유지 돼요 |
| 11 | 2.1 | 위험도 게이지 | 다만 보안 위험도 최고 등급 첫 모델 |
| 12 | 2.3 | 취약점 코드 | 보안 취약점 까지 찾아낼 수준이에요 |
| 13 | 2.4 | 팔로우 CTA | 매일 AI 소식, 팔로우 하고 받아보세요 |

장면 길이는 자막 음절 수 × 0.125초 + 0.4초(최소 1.8초)로 잡아서, 캡컷 TTS 기본~1.1배속으로 읽으면 장면 안에 들어간다.

## 캡컷에서 음성 입히기
1. `001-gpt6-astra.mp4`(자막 포함)를 타임라인에 올린다.
2. 텍스트 → 로컬 자막 → `001-gpt6-astra.srt` 가져오기 → 장면 타이밍대로 자막 13개가 깔린다.
3. 자막 클립 전체 선택 → 텍스트 읽기(Text to speech) → 목소리 선택 → 생성.
4. 음성이 오디오 트랙으로 생기면 SRT 자막 클립은 삭제하거나 투명도 0으로 (영상에 이미 디자인된 자막이 있으므로).
   - 캡컷 자막 스타일을 쓰고 싶으면 대신 `_nocap.mp4`를 쓰고 SRT 자막을 그대로 둔다.
5. 음성이 장면보다 길면 해당 음성만 1.1~1.2배속, BGM은 음성 아래 -20dB 정도로 깐다.

## 업로드 문구 (초안)
- 제목: GPT-6 아스트라, 뭐가 달라졌을까? #shorts
- 해시태그: #GPT6 #OpenAI #AI뉴스 #AI툴 #shorts

## 출처 (2026-09-28 확인)
- OpenAI — GPT-6 Astra: https://openai.com/index/gpt-6-astra/
- OpenAI — Safety overview: https://openai.com/index/safety-overview-gpt-6-astra/
- Fox Business: https://www.foxbusiness.com/technology/openai-unveils-gpt-6-astra-major-advances-ai-capabilities
- DataCamp: https://www.datacamp.com/blog/gpt-6-astra
