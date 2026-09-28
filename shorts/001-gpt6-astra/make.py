"""GPT-6 Astra 쇼츠 데모: 슬라이드 PNG 생성 -> ffmpeg로 1080x1920 MP4 렌더링."""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg, koreanize_matplotlib

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
FD = os.path.join(os.path.dirname(koreanize_matplotlib.__file__), "fonts")
def F(size, w="ExtraBold"): return ImageFont.truetype(os.path.join(FD, f"NanumGothic{w}.ttf"), size)

W, H = 1080, 1920
BG, INK, SUB, ACC, ACC2, WARN = (10, 12, 20), (245, 246, 250), (150, 158, 178), (16, 163, 127), (99, 102, 241), (239, 68, 68)

def base(tag):
    im = Image.new("RGB", (W, H), BG)
    glow = Image.new("RGB", (W, H), BG); g = ImageDraw.Draw(glow)
    g.ellipse((-300, -200, 900, 800), fill=(18, 60, 52)); g.ellipse((400, 1300, 1400, 2200), fill=(30, 30, 80))
    im = Image.blend(im, glow.filter(ImageFilter.GaussianBlur(220)), 1.0)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((70, 150, 70 + d.textlength(tag, F(38)) + 60, 220), 35, fill=ACC)
    d.text((100, 185), tag, font=F(38), fill=BG, anchor="lm")
    d.text((W - 70, 185), "AI 30초 브리핑", font=F(34, "Bold"), fill=SUB, anchor="rm")
    return im, d

def lines(d, y, rows, gap=24):
    for text, font, color in rows:
        d.text((W // 2, y), text, font=font, fill=color, anchor="mt"); y += font.size + gap
    return y

def card(d, box, title, sub, color):
    d.rounded_rectangle(box, 36, fill=(24, 28, 42), outline=color, width=4)
    x0, y0, x1, y1 = box
    d.text((x0 + 50, y0 + 45), title, font=F(52), fill=INK)
    d.text((x0 + 50, y0 + 120), sub, font=F(38, "Bold"), fill=SUB)

def window(d, box):  # 브라우저 창 + 커서 일러스트
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 30, fill=(28, 32, 48), outline=(60, 66, 90), width=3)
    for i, c in enumerate([(239, 68, 68), (234, 179, 8), (34, 197, 94)]):
        d.ellipse((x0 + 30 + i * 40, y0 + 28, x0 + 56 + i * 40, y0 + 54), fill=c)
    for i, (lbl, done) in enumerate([("이름", 1), ("이메일", 1), ("주소", 0)]):
        yy = y0 + 110 + i * 110
        d.text((x0 + 50, yy + 38), lbl, font=F(34, "Bold"), fill=SUB, anchor="lm")
        d.rounded_rectangle((x0 + 190, yy, x1 - 50, yy + 76), 16, fill=(40, 46, 66), outline=ACC if done else ACC2, width=3)
        if done: d.line([(x1 - 110, yy + 38), (x1 - 94, yy + 54), (x1 - 66, yy + 22)], fill=ACC, width=7, joint="curve")
    cx, cy = x1 - 260, y0 + 350
    d.polygon([(cx, cy), (cx, cy + 90), (cx + 24, cy + 68), (cx + 44, cy + 108), (cx + 60, cy + 100), (cx + 40, cy + 62), (cx + 70, cy + 60)], fill=INK, outline=BG)

def doc_icon(d, x, y, color, kind):
    d.rounded_rectangle((x, y, x + 230, y + 290), 24, fill=(28, 32, 48), outline=color, width=5)
    if kind == "doc":
        for i in range(5): d.rounded_rectangle((x + 35, y + 50 + i * 42, x + 195 - (60 if i == 4 else 0), y + 66 + i * 42), 8, fill=color)
    elif kind == "sheet":
        for i in range(4):
            for j in range(3): d.rectangle((x + 30 + j * 58, y + 45 + i * 52, x + 80 + j * 58, y + 88 + i * 52), fill=color if i == 0 else (50, 56, 80))
    else:
        d.rounded_rectangle((x + 30, y + 50, x + 200, y + 160), 12, fill=color)
        for h, i in zip((60, 100, 80), range(3)): d.rectangle((x + 50 + i * 55, y + 250 - h, x + 85 + i * 55, y + 250), fill=(90, 96, 130))

slides = []

# 1. 훅
im, d = base("NEW MODEL")
lines(d, 560, [("GPT-6 나왔다", F(130), INK), ("", F(20), INK), ("이제 AI가", F(84), SUB), ("'직접' 일한다", F(110), ACC)])
d.text((W // 2, 1500), "OpenAI · GPT-6 Astra", font=F(46, "Bold"), fill=SUB, anchor="mm")
slides.append((im, 3.0))

# 2. 기본 정보
im, d = base("무엇?")
lines(d, 380, [("GPT-6 Astra", F(110), INK), ("OpenAI의 새 플래그십 모델", F(52, "Bold"), SUB)])
card(d, (90, 760, 990, 960), "2026.09.03 공개", "제한 프리뷰로 먼저 시작", ACC)
card(d, (90, 1010, 990, 1210), "ChatGPT 유료 플랜", "Plus · Pro · Business · Enterprise", ACC2)
card(d, (90, 1260, 990, 1460), "API로도 사용 가능", "개발자도 바로 붙여 쓸 수 있음", ACC)
slides.append((im, 4.0))

# 3. 컴퓨터 사용
im, d = base("할 수 있는 것 ①")
lines(d, 330, [("컴퓨터를", F(96), INK), ("직접 조작한다", F(110), ACC)])
window(d, (110, 700, 970, 1180))
lines(d, 1290, [("온라인 양식 작성", F(56), INK), ("CRM 고객 정보 업데이트", F(56), INK), ("캘린더 정리", F(56), INK)], gap=36)
slides.append((im, 5.0))

# 4. 문서 생성
im, d = base("할 수 있는 것 ②")
lines(d, 330, [("문서 · 엑셀 · PPT", F(92), INK), ("알아서 만든다", F(110), ACC)])
for i, (c, k) in enumerate([(ACC, "doc"), (ACC2, "sheet"), ((234, 179, 8), "slide")]): doc_icon(d, 95 + i * 330, 740, c, k)
lines(d, 1180, [("리서치 → 요약 초안까지", F(62), INK), ("메일·문서 편집기 안에서 바로", F(46, "Bold"), SUB)])
slides.append((im, 4.5))

# 5. 작업 중 수정
im, d = base("눈여겨볼 점")
lines(d, 380, [("일하는 도중에", F(96), INK), ("지시를 바꿔도 OK", F(100), ACC)])
for i, (t, c) in enumerate([("작업 진행 중", SUB), ("요구사항 변경", ACC2), ("완료된 작업은 유지", ACC)]):
    y = 820 + i * 230
    d.rounded_rectangle((170, y, 910, y + 150), 75, fill=(24, 28, 42), outline=c, width=5)
    d.text((W // 2, y + 75), t, font=F(56), fill=INK, anchor="mm")
    if i < 2: d.polygon([(W // 2 - 26, y + 168), (W // 2 + 26, y + 168), (W // 2, y + 210)], fill=SUB)
slides.append((im, 4.0))

# 6. 주의
im, d = base("주의")
lines(d, 360, [("OpenAI 모델 최초", F(70, "Bold"), SUB), ("사이버보안", F(110), INK), ("'Critical' 등급", F(110), WARN)])
sx, sy = W // 2, 1130
d.polygon([(sx, sy - 190), (sx + 170, sy - 120), (sx + 150, sy + 90), (sx, sy + 200), (sx - 150, sy + 90), (sx - 170, sy - 120)], fill=(60, 20, 24), outline=WARN)
d.text((sx, sy), "!", font=F(200), fill=WARN, anchor="mm")
lines(d, 1400, [("그만큼 강력하다는 뜻", F(56), INK), ("= 보안 취약점까지 찾아낼 수준", F(44, "Bold"), SUB)])
slides.append((im, 4.0))

# 7. CTA
im, d = base("FOLLOW")
lines(d, 620, [("AI 소식,", F(110), INK), ("30초면 충분", F(110), ACC), ("", F(40), INK), ("팔로우하고 매일 받아보기", F(58, "Bold"), SUB)])
d.rounded_rectangle((290, 1380, 790, 1510), 65, fill=WARN); d.text((W // 2, 1445), "구독", font=F(64), fill=INK, anchor="mm")
slides.append((im, 3.0))

# 렌더링: 각 슬라이드에 살짝 줌인 + 0.3초 크로스페이드
ff, FPS, XF = imageio_ffmpeg.get_ffmpeg_exe(), 30, 0.3
args, filt = [ff, "-y"], []
for i, (im, dur) in enumerate(slides):
    p = os.path.join(OUT, f"{i + 1:02d}.png"); im.save(p)
    args += ["-loop", "1", "-framerate", str(FPS), "-t", str(dur), "-i", p]
    n = int(dur * FPS)
    filt.append(f"[{i}:v]scale=1188:2112,zoompan=z='1+0.04*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={W}x{H}:fps={FPS},trim=duration={dur},setpts=PTS-STARTPTS,fps={FPS},format=yuv420p[v{i}]")
prev, t = "v0", slides[0][1]
for i in range(1, len(slides)):
    filt.append(f"[{prev}][v{i}]xfade=transition=fade:duration={XF}:offset={t - XF:.2f}[x{i}]")
    prev, t = f"x{i}", t + slides[i][1] - XF
mp4 = os.path.join(HERE, "gpt6-astra-short.mp4")
r = subprocess.run(args + ["-filter_complex", ";".join(filt), "-map", f"[{prev}]", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", mp4], check=True, capture_output=True, text=True)
print(f"done: {mp4} ({t:.1f}s)")
