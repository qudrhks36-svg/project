"""에피소드 HTML을 Chromium으로 프레임 단위 캡처해 1080x1920 MP4로 렌더링한다.

사용법: python3 shorts/_assets/render.py shorts/001-gpt6-astra/episode.html [--still]
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

        mp4 = os.path.join(out_dir, f"{name}.mp4")
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
        browser.close()
        print(f"done: {mp4} ({total:.1f}s, {frames} frames)")


if __name__ == "__main__":
    main(sys.argv[1], still="--still" in sys.argv)
