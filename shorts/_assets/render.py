"""에피소드 HTML을 Chromium으로 프레임 단위 캡처해 1080x1920 MP4로 렌더링한다.

사용법: python3 shorts/_assets/render.py shorts/001-gpt6-astra/episode.html [--still]
  기본   : <폴더명>.mp4 (자막 포함) + <폴더명>_nocap.mp4 (자막 없음) + <폴더명>.srt
           → 캡컷에서 SRT를 불러와 '텍스트 읽기'로 음성을 만든다
  --still : 각 비트 중간 프레임만 PNG로 저장 (디자인 확인용)
준비물: pip install playwright imageio-ffmpeg  (Chromium은 /opt/pw-browsers 에 설치된 것을 사용)
"""
import os, subprocess, sys
import imageio_ffmpeg
from playwright.sync_api import sync_playwright

FPS = 30
CHROME = os.environ.get("CHROME_PATH", "/opt/pw-browsers/chromium")


def main(html, still=False):
    html = os.path.abspath(html)
    out_dir = os.path.dirname(html)
    name = os.path.basename(out_dir)
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None)
        page = browser.new_page(viewport={"width": 1080, "height": 1920})
        page.goto(f"file://{html}")
        page.evaluate("document.fonts.ready")
        total = page.evaluate("TOTAL")

        if still:
            mids = page.evaluate("""() => { let s = 0; return [...document.querySelectorAll('.beat')]
                .map(b => { const d = +b.dataset.d, m = s + d * 0.8; s += d; return m; }); }""")
            os.makedirs(os.path.join(out_dir, "stills"), exist_ok=True)
            for i, t in enumerate(mids):
                page.evaluate(f"setTime({t})")
                page.screenshot(path=os.path.join(out_dir, "stills", f"{i + 1:02d}.png"))
            print(f"stills: {len(mids)}")
            return

        write_srt(page, os.path.join(out_dir, f"{name}.srt"))
        render(page, total, os.path.join(out_dir, f"{name}.mp4"))
        page.add_style_tag(content=".captions { display: none !important; }")
        render(page, total, os.path.join(out_dir, f"{name}_nocap.mp4"))
        browser.close()


def srt_time(t):
    ms = round(t * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def write_srt(page, path):
    """비트 타이밍 그대로 자막을 SRT로 내보낸다 (줄바꿈 없이 한 줄 = TTS가 자연스럽게 읽음)."""
    cues = page.evaluate("""() => { let s = 0; const caps = [...document.querySelectorAll('.cap')];
        return [...document.querySelectorAll('.beat')].map((b, i) => { const d = +b.dataset.d, c = [s, s + d,
          (caps[i]?.innerHTML || '').replace(/<br\\s*\\/?>/g, ' ').replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').replace(/\\s+/g, ' ').trim()];
          s += d; return c; }); }""")
    with open(path, "w", encoding="utf-8") as f:
        for i, (a, b, text) in enumerate(cues, 1):
            f.write(f"{i}\n{srt_time(a)} --> {srt_time(b - 0.05)}\n{text}\n\n")
    print(f"srt: {path} ({len(cues)} cues)")


def render(page, total, mp4):
    ff = subprocess.Popen(
        [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error",
         "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
         "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", mp4],
        stdin=subprocess.PIPE)
    frames = int(total * FPS)
    for f in range(frames):
        page.evaluate(f"setTime({f / FPS})")
        ff.stdin.write(page.screenshot(type="jpeg", quality=95))
    ff.stdin.close(); ff.wait()
    print(f"done: {mp4} ({total:.1f}s, {frames} frames)")


if __name__ == "__main__":
    main(sys.argv[1], still="--still" in sys.argv)
