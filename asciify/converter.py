from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

from .styles import PALETTE, get_style


def _terminal_size(fallback_w: int = 120, fallback_h: int = 40) -> tuple[int, int]:
    try:
        s = os.get_terminal_size()
        return s.columns, s.lines
    except OSError:
        return fallback_w, fallback_h


def _compute_output_size(
    img_w: int,
    img_h: int,
    width:  Optional[int],
    height: Optional[int],
) -> tuple[int, int]:
    term_w, term_h = _terminal_size()
    out_w = width or term_w
    font_ratio = 0.55
    out_h = height or max(1, int(img_h * (out_w / img_w) * font_ratio))
    out_h = min(out_h, term_h - 2)
    return out_w, out_h


def _build_color_frame(
    char_grid: np.ndarray,
    r: np.ndarray,
    g: np.ndarray,
    b: np.ndarray,
    color_mode: str,
) -> str:
    h, w = char_grid.shape
    
    # Boost brightness by 30%
    r = np.clip(r * 1.3, 0, 255).astype("int32").flatten()
    g = np.clip(g * 1.3, 0, 255).astype("int32").flatten()
    b = np.clip(b * 1.3, 0, 255).astype("int32").flatten()
    chars = char_grid.flatten()

    if color_mode == "fg":
        cells = [
            f"\033[38;2;{rv};{gv};{bv}m{cv}\033[0m"
            for rv, gv, bv, cv in zip(r, g, b, chars)
        ]
    elif color_mode == "bg":
        cells = [
            f"\033[48;2;{rv};{gv};{bv}m \033[0m"
            for rv, gv, bv in zip(r, g, b)
        ]
    elif color_mode == "both":
        cells = [
            f"\033[48;2;{rv//2};{gv//2};{bv//2}m\033[38;2;{rv};{gv};{bv}m{cv}\033[0m"
            for rv, gv, bv, cv in zip(r, g, b, chars)
        ]
    else:
        raise ValueError(f"Unknown color_mode '{color_mode}'. Use: fg, bg, both")

    return "\n".join(["".join(cells[i * w : (i + 1) * w]) for i in range(h)])


def render_frame(
    rgb:        np.ndarray,
    palette:    str,
    color_mode: str  = "none",
    invert:     bool = False,
) -> str:
    r = rgb[:, :, 0]
    g = rgb[:, :, 1]
    b = rgb[:, :, 2]

    lum = (r * 0.299 + g * 0.587 + b * 0.114) / 255.0

    if invert:
        lum = 1.0 - lum

    pal_len = len(palette)
    indices = np.clip((lum * (pal_len - 1)).astype(int), 0, pal_len - 1)

    pal_array  = np.array(list(palette))
    char_grid  = pal_array[indices]

    if color_mode == "none":
        return "\n".join(["".join(row) for row in char_grid])

    return _build_color_frame(char_grid, r, g, b, color_mode)


class ImageConverter:

    def __init__(
        self,
        style:      str   = "ascii",
        color_mode: str   = "none",
        width:      Optional[int]   = None,
        height:     Optional[int]   = None,
        invert:     bool  = False,
        contrast:   float = 1.2,
        sharpen:    bool  = False,
        edge:       bool  = False,
    ):
        self.style      = get_style(style)
        self.palette    = PALETTE[self.style.palette_key]
        self.color_mode = color_mode
        self.width      = width
        self.height     = height
        self.invert     = invert
        self.contrast   = contrast
        self.sharpen    = sharpen
        self.edge       = edge

    def convert_file(self, path: str | Path) -> str:
        img = Image.open(path).convert("RGB")
        return self.convert_image(img)

    def convert_image(self, img: Image.Image) -> str:
        img = self._preprocess(img)
        rgb = np.array(img, dtype=np.uint8)
        return render_frame(rgb, self.palette, self.color_mode, self.invert)

    def print_file(self, path: str | Path) -> None:
        print(self.convert_file(path))

    def _preprocess(self, img: Image.Image) -> Image.Image:
        out_w, out_h = _compute_output_size(
            img.width, img.height, self.width, self.height
        )
        img = img.resize((out_w, out_h), Image.LANCZOS)

        if self.contrast != 1.0:
            img = ImageEnhance.Contrast(img).enhance(self.contrast)
        if self.sharpen:
            img = img.filter(ImageFilter.SHARPEN)
        if self.edge:
            img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

        return img
