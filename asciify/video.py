from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Optional

import numpy as np

from .converter import render_frame, _compute_output_size, _terminal_size
from .styles import PALETTE, get_style


class VideoConverter:

    def __init__(
        self,
        style:      str            = "ascii",
        color_mode: str            = "none",
        width:      Optional[int]  = None,
        fps:        Optional[float]= None,
        loop:       bool           = False,
        invert:     bool           = False,
        contrast:   float          = 1.2,
        max_frames: Optional[int]  = None,
    ):
        self.style      = get_style(style)
        self.palette    = PALETTE[self.style.palette_key]
        self.color_mode = color_mode
        self.width      = width
        self.fps        = fps
        self.loop       = loop
        self.invert     = invert
        self.contrast   = contrast
        self.max_frames = max_frames

    def play(self, path: str | Path) -> None:
        try:
            import cv2
        except ImportError:
            print(
                "Video support requires opencv.\n"
                "Install it with: pip install 'asciify-art'"
            )
            sys.exit(1)

        path = str(path)
        cap  = cv2.VideoCapture(path)

        if not cap.isOpened():
            raise FileNotFoundError(f"Cannot open video file: {path}")

        native_fps  = cap.get(cv2.CAP_PROP_FPS) or 24.0
        target_fps  = self.fps or native_fps
        frame_budget = 1.0 / target_fps

        frame_count = 0
        art_height  = None
        out         = sys.stdout
        preset_size = None

        out.write("\033[?25l")
        out.flush()

        try:
            while True:
                t_start = time.perf_counter()

                ret, bgr = cap.read()

                if not ret:
                    if self.loop:
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        continue
                    break

                if preset_size is None:
                    vid_h, vid_w = bgr.shape[:2]
                    preset_size = _compute_output_size(vid_w, vid_h, self.width, None)
                
                out_w, out_h = preset_size

                bgr_resized = cv2.resize(
                    bgr, (out_w, out_h),
                    interpolation=cv2.INTER_LINEAR
                )

                rgb = cv2.cvtColor(bgr_resized, cv2.COLOR_BGR2RGB)

                if self.contrast != 1.0:
                    rgb = np.clip(
                        (rgb.astype(np.float32) - 128) * self.contrast + 128,
                        0, 255
                    ).astype(np.uint8)

                art = render_frame(rgb, self.palette, self.color_mode, self.invert)

                if art_height is None:
                    art_height = out_h
                else:
                    out.write(f"\033[{art_height}A")

                out.write(art)
                out.write("\n")
                out.flush()

                frame_count += 1
                if self.max_frames and frame_count >= self.max_frames:
                    break

                elapsed   = time.perf_counter() - t_start
                remaining = frame_budget - elapsed
                if remaining > 0:
                    time.sleep(remaining)

        except KeyboardInterrupt:
            pass

        finally:
            cap.release()
            out.write("\033[?25h")
            out.write("\033[0m\n")
            out.flush()
