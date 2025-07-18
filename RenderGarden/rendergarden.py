import asyncio
import os
from pyppeteer import launch
from PIL import Image, ImageChops
from moviepy.editor import ImageSequenceClip

# === High-Quality Settings ===
DURATION = 5               # seconds to record
FPS = 15                   # frames per second
VIEWPORT_WIDTH = 1600      # ⬅️ Higher resolution
VIEWPORT_HEIGHT = 1200
TEMP_FRAME_DIR = "frames_temp"

def autocrop(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    return im.crop(bbox) if bbox else im

async def capture_frames(html_path):
    if not os.path.exists(html_path):
        raise FileNotFoundError(f"❌ File not found: {html_path}")
    
    if not os.path.exists(TEMP_FRAME_DIR):
        os.makedirs(TEMP_FRAME_DIR)

    browser = await launch(headless=True, args=["--no-sandbox"])
    page = await browser.newPage()
    await page.setViewport({"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT})
    await page.goto("file://" + os.path.abspath(html_path))
    await asyncio.sleep(1)

    for i in range(DURATION * FPS):
        await page.screenshot({'path': f"{TEMP_FRAME_DIR}/frame_{i:03}.png"})
        await asyncio.sleep(1 / FPS)

    await browser.close()

def create_mp4(output_name, output_folder):
    print("🧹 Cropping frames and generating high-quality video...")

    images = []
    for i in range(DURATION * FPS):
        im_path = os.path.join(TEMP_FRAME_DIR, f"frame_{i:03}.png")
        img = Image.open(im_path)
        cropped = autocrop(img)
        images.append(cropped)

    cropped_paths = []
    for i, img in enumerate(images):
        path = os.path.join(TEMP_FRAME_DIR, f"cropped_{i:03}.png")
        img.save(path)
        cropped_paths.append(path)

    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f"{output_name}.mp4")
    
    clip = ImageSequenceClip(cropped_paths, fps=FPS)
    clip.write_videofile(
        output_path,
        codec="libx264",
        audio=False,
        bitrate="20000k",
        preset="slow"
    )

    print(f"\n✅ MP4 saved to: {output_path}")

def clean_up():
    for f in os.listdir(TEMP_FRAME_DIR):
        os.remove(os.path.join(TEMP_FRAME_DIR, f))
    os.rmdir(TEMP_FRAME_DIR)

def run():
    html_path = input("📄 Enter path to your HTML file (e.g., index.html): ").strip()
    if not os.path.exists(html_path):
        print(f"❌ Error: File not found: {html_path}")
        return

    output_name = input("🎬 Enter output video filename (without .mp4): ").strip()
    output_folder = input("📂 Enter output folder name (will be created if not exists): ").strip()

    asyncio.get_event_loop().run_until_complete(capture_frames(html_path))
    create_mp4(output_name, output_folder)
    clean_up()

if __name__ == "__main__":
    run()