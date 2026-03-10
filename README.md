
```bash
pip install asciify
```

For video support:
```bash
pip install 'asciify[video]'
```

## Quick Start

```bash
# Convert an image with default style
asciify image photo.jpg

# Use the blocks style with colored background
asciify image photo.jpg -s blocks -c bg

# List all available styles
asciify styles
```

## Styles

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

## Examples

### Image conversion

```bash
# Basic conversion
asciify image input.png

# Detailed style with foreground color
asciify image input.png -s detailed -c fg

# Custom width and contrast
asciify image input.png -w 80 --contrast 1.5

# Save output to file
asciify image input.png -o output.txt
```

### Video playback

```bash
# Play video with default settings
asciify video clip.mp4

# Matrix style at 15 FPS
asciify video clip.mp4 -s matrix -f 15

# Loop video with colored background
asciify video clip.mp4 -c bg --loop
```

### Color modes

- `none` - Plain ASCII (default)
- `fg` - Colored foreground text
- `bg` - Colored background (pixel-like)
- `both` - Foreground + dimmed background

## Options

### Image command

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

### Video command

| Option | Short | Description |
|--------|-------|-------------|
| `--style` | `-s` | Art style (default: ascii) |
| `--color-mode` | `-c` | Color mode: none/fg/bg/both |
| `--width` | `-w` | Output width in characters |
| `--fps` | `-f` | Playback FPS |
| `--loop` | `-l` | Loop video |
| `--invert` | `-i` | Invert brightness |
| `--contrast` | - | Contrast multiplier (default: 1.2) |

## Help

```bash
asciify --help
asciify image --help
asciify video --help
```

## License

MIT
