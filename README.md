<h1 align="center">asciify-art</h1>

<p align="center">
  <strong>Convert images and videos to stunning ASCII and ANSI art right in your terminal!</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/pypi/v/asciify-art.svg" alt="PyPI version">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Supported Python versions">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
</p>

---

`asciify-art` is a blazing fast command-line tool built in Python. Transform any image or video into beautiful text art with rich color support, various art styles, and incredibly optimized performance.

## ✨ Features

- **Single Install:** Everything is included—image and video processing works immediately.
- **Multiple Styles:** Choose from classic ASCII, detailed character palettes, braille patterns, matrix falling code, and more!
- **True Color Support:** Full 24-bit ANSI color formatting for foreground, background, or both.
- **Video Playback:** Super smooth and optimized video rendering directly in your terminal/console.
- **Image Processing Filters:** Tweak contrast, invert colors, or apply sharpen and edge enhance filters.

## 🚀 Installation

It's just one command away:

```bash
pip install asciify-art
```

*Note: The CLI command remains `asciify` for convenience and speed!*

## 📖 Quick Start

```bash
# Convert a simple image
asciify image photo.jpg

# Apply the "blocks" style with a colored background
asciify image photo.jpg -s blocks -c bg

# View all available art styles
asciify styles
```

## 🎨 Styles

| Style | Description | Best for |
|-------|-------------|----------|
| `ascii` | Classic ` .:-=+*#%@` | Simple, clean output |
| `detailed` | 70+ character palette | High-detail images |
| `blocks` | `░▒▓█` shading | Pixel-art aesthetic |
| `minimal` | Sparse ` .:oO0@` | Clean, modern look |
| `braille` | Braille patterns | Dense, textured output |
| `matrix` | Katakana characters | Matrix effect |
| `dots` | Minimal dot art | Subtle conversions |
| `shade` | Circle progression `·∘○◎●` | Smooth gradients |
| `color` | True 24-bit ANSI | Full color output |

## 💡 Examples

### Image Conversion

```bash
# Basic conversion
asciify image input.png

# Detailed style with foreground color
asciify image input.png -s detailed -c fg

# Custom width (80 characters) and high contrast
asciify image input.png -w 80 --contrast 1.5

# Save the output to a text file
asciify image input.png -o output.txt
```

### Video Playback

```bash
# Play a video with default settings
asciify video clip.mp4

# Matrix style rendering at 15 FPS
asciify video clip.mp4 -s matrix -f 15

# Loop a video infinitely with a distinct colored background
asciify video clip.mp4 -c bg --loop
```

### Color Modes

- `none` - Plain text (default)
- `fg` - Colored foreground text characters
- `bg` - Colored background cells (resembling pixel-art)
- `both` - Foreground + dimmed background combination

## ⚙️ Options

### Image Command Options

| Option | Short | Description |
|--------|-------|-------------|
| `--style` | `-s` | Art style (default: ascii) |
| `--color-mode` | `-c` | Color mode: none/fg/bg/both |
| `--width` | `-w` | Output width in characters |
| `--invert` | `-i` | Invert brightness |
| `--contrast` | - | Contrast multiplier (default: 1.2) |
| `--sharpen` | - | Apply sharpen filter |
| `--edge` | - | Apply edge enhance |
| `--output` | `-o` | Save to file |

### Video Command Options

| Option | Short | Description |
|--------|-------|-------------|
| `--style` | `-s` | Art style (default: ascii) |
| `--color-mode` | `-c` | Color mode: none/fg/bg/both |
| `--width` | `-w` | Output width in characters |
| `--fps` | `-f` | Playback FPS |
| `--loop` | `-l` | Loop video |
| `--invert` | `-i` | Invert brightness |
| `--contrast` | - | Contrast multiplier (default: 1.2) |

## ❓ Help

Need more details? Access built-in documentation anytime:

```bash
asciify --help
asciify image --help
asciify video --help
```

## 📄 License

Distributed under the MIT License.
