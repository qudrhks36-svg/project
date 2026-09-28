# AI 쇼츠 제작

에피소드 하나 = 폴더 하나 (`NNN-slug/episode.html`). 공통 디자인·엔진은 `_assets/`.

- `_assets/shorts.css` — 디자인 시스템 (컬러 토큰, Pretendard, 헤더 바/비주얼/자막 레이아웃)
- `_assets/shorts.js` — 타임라인 엔진 (`.beat[data-d]`, `.cap`, `.pop[data-at]`, `[data-type]` 등)
- `_assets/render.py` — Chromium으로 프레임 캡처 → MP4

컬러: 배경 #07070C · 바이올렛 #8B5CF6 → 시안 #22D3EE 그라데이션 · 강조 라임 #D4FF3A · 경고 #FF4D6D

준비물: `pip install playwright imageio-ffmpeg` (+ Chromium)
