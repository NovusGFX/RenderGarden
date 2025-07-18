# HTML to MP4 Converter 🎞️

Convert animated `.html` files into high-quality `.mp4` videos using headless Chromium and Python.

## Features
- Headless rendering of animated HTML
- Frame-by-frame capture with auto-cropping
- High-resolution MP4 export with adjustable FPS and bitrate
- Fully interactive CLI (choose input HTML, output name, and folder)

## Requirements

Install dependencies via pip:

```bash
pip install -r requirements.txt
```

Also make sure [FFmpeg](https://ffmpeg.org/download.html) is installed and in your system path.

## Usage

```bash
python html_to_mp4.py
```

You'll be prompted for:
- Input HTML file path
- Output video name (without `.mp4`)
- Output folder name

Example:

```
📄 Enter path to your HTML file (e.g., index.html): index.html
🎬 Enter output video filename (without .mp4): animation
📂 Enter output folder name (will be created if not exists): videos
```

This will produce:

```
videos/animation.mp4
```

## License
MIT