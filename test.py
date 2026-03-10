# from PIL import Image, ImageEnhance, ImageFilter
# import os, sys, time
# import numpy as np

# PALETTE = {
#     "ascii":    " .:-=+*#%@",
#     "detailed": " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$",
#     "blocks":   " ░▒▓█",
#     "minimal":  " .:oO0@",
#     "braille":  " ⠁⠃⠇⠏⠟⠿⣿",
#     "matrix":   "ｦｧｨｩｪｫｬｭｮｯｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ",
#     "dots":     " ·:;",
#     "shade":    " ·∘○◎●",
# }

# def terminal_size(fallback_w=120, fallback_h=40):
#     try:
#         s = os.get_terminal_size()
#         return s.columns, s.lines
#     except OSError:
#         return fallback_w, fallback_h

# def compute_size(img_w, img_h, width, height):
#     term_w, term_h = terminal_size()
#     w = width or term_w
#     font_ratio = 0.55
#     h = height or max(1, int(img_h * (w / img_w) * font_ratio))
#     h = min(h, term_h - 2)
#     return w, h

# # ── THE KEY CHANGE: build entire frame as one string using numpy, zero Python pixel loops ──

# def render_frame(rgb: np.ndarray, palette: str, color_mode: str, invert: bool) -> str:
#     h, w, _ = rgb.shape
#     r = rgb[:, :, 0].astype(np.int32)
#     g = rgb[:, :, 1].astype(np.int32)
#     b = rgb[:, :, 2].astype(np.int32)

#     # perceptual luminance → char indices, all at once
#     lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
#     if invert:
#         lum = 1.0 - lum
#     pal_len = len(palette)
#     idx = np.clip((lum * (pal_len - 1)).astype(int), 0, pal_len - 1)

#     # map indices → character grid (numpy fancy indexing)
#     pal_array = np.array(list(palette))
#     char_grid = pal_array[idx]   # shape (h, w), each cell is one char

#     if color_mode == "none":
#         # fastest path: just join chars, no escape codes at all
#         lines = ["".join(row) for row in char_grid]
#         return "\n".join(lines)

#     # build escape-code strings vectorized using numpy string operations
#     if color_mode == "fg":
#         # \033[38;2;R;G;Bm{char}\033[0m
#         prefix = np.char.add(np.char.add(np.char.add(
#             np.char.add("\033[38;2;", r.astype(str)),
#             np.char.add(";", g.astype(str))),
#             np.char.add(";", b.astype(str))),
#             "m")
#         cells = np.char.add(np.char.add(prefix, char_grid), "\033[0m")

#     elif color_mode == "bg":
#         # background block — char is always a space
#         prefix = np.char.add(np.char.add(np.char.add(
#             np.char.add("\033[48;2;", r.astype(str)),
#             np.char.add(";", g.astype(str))),
#             np.char.add(";", b.astype(str))),
#             "m")
#         cells = np.char.add(prefix, " \033[0m")

#     elif color_mode == "both":
#         dr, dg, db = r // 3, g // 3, b // 3
#         fg = np.char.add(np.char.add(np.char.add(
#             np.char.add("\033[38;2;", r.astype(str)),
#             np.char.add(";", g.astype(str))),
#             np.char.add(";", b.astype(str))),
#             "m")
#         bg = np.char.add(np.char.add(np.char.add(
#             np.char.add("\033[48;2;", dr.astype(str)),
#             np.char.add(";", dg.astype(str))),
#             np.char.add(";", db.astype(str))),
#             "m")
#         cells = np.char.add(np.char.add(np.char.add(bg, fg), char_grid), "\033[0m")

#     lines = ["".join(row) for row in cells]
#     return "\n".join(lines)


# def convert(img: Image.Image, style="ascii", width=None, height=None,
#             invert=False, contrast=1.2, sharpen=False, edge=False,
#             color_mode="none") -> str:
#     w, h = compute_size(img.width, img.height, width, height)
#     img = img.resize((w, h), Image.LANCZOS)

#     if contrast != 1.0:
#         img = ImageEnhance.Contrast(img).enhance(contrast)
#     if sharpen:
#         img = img.filter(ImageFilter.SHARPEN)
#     if edge:
#         img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

#     rgb = np.array(img.convert("RGB"), dtype=np.uint8)
#     palette = PALETTE.get(style, PALETTE["ascii"])
#     return render_frame(rgb, palette, color_mode, invert)


# def convert_file(path, **kwargs) -> str:
#     return convert(Image.open(path).convert("RGB"), **kwargs)


# def play_video(path, style="ascii", width=None, fps=None,
#                invert=False, contrast=1.2, loop=False, color_mode="none"):
#     try:
#         import cv2
#     except ImportError:
#         print("pip install opencv-python-headless")
#         sys.exit(1)

#     cap = cv2.VideoCapture(path)
#     if not cap.isOpened():
#         print(f"Cannot open: {path}")
#         sys.exit(1)

#     native_fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
#     target_fps = fps or native_fps
#     delay = 1.0 / target_fps

#     palette = PALETTE.get(style, PALETTE["ascii"])
#     art_height = None
#     out = sys.stdout

#     out.write("\033[?25l")   # hide cursor
#     out.flush()

#     try:
#         while True:
#             t_frame_start = time.perf_counter()

#             ret, bgr = cap.read()
#             if not ret:
#                 if loop:
#                     cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
#                     continue
#                 break

#             # ── resize directly in OpenCV (faster than Pillow resize) ──
#             vid_h, vid_w = bgr.shape[:2]
#             term_w, term_h = terminal_size()
#             out_w = width or term_w
#             font_ratio = 0.55
#             out_h = min(max(1, int(vid_h * (out_w / vid_w) * font_ratio)), term_h - 2)

#             bgr_resized = cv2.resize(bgr, (out_w, out_h), interpolation=cv2.INTER_LINEAR)
#             rgb = cv2.cvtColor(bgr_resized, cv2.COLOR_BGR2RGB)

#             # ── apply contrast in numpy (skip Pillow entirely for video) ──
#             if contrast != 1.0:
#                 rgb = np.clip((rgb.astype(np.float32) - 128) * contrast + 128, 0, 255).astype(np.uint8)

#             art = render_frame(rgb, palette, color_mode, invert)

#             if art_height is None:
#                 art_height = art_height = out_h
#             else:
#                 out.write(f"\033[{art_height}A")   # move cursor up

#             out.write(art)
#             out.write("\n")
#             out.flush()

#             # ── precise frame timing ──
#             elapsed = time.perf_counter() - t_frame_start
#             remaining = delay - elapsed
#             if remaining > 0:
#                 time.sleep(remaining)

#     except KeyboardInterrupt:
#         pass
#     finally:
#         cap.release()
#         out.write("\033[?25h\033[0m\n")
#         out.flush()


# def usage():
#     print("""
# ╔══════════════════════════════════════════════════╗
# ║              ASCII / ANSI Art CLI                ║
# ╚══════════════════════════════════════════════════╝

# Usage:
#   python test.py image <file> [style] [color]
#   python test.py video <file> [style] [color] [fps]

# Styles:   ascii  detailed  blocks  minimal  braille  matrix  dots  shade
# Colors:   none   fg   bg   both

# Examples:
#   python test.py image eye.jpg
#   python test.py image eye.jpg detailed both
#   python test.py image eye.jpg blocks bg

#   python test.py video clip.mp4
#   python test.py video clip.mp4 ascii fg 24
#   python test.py video clip.mp4 blocks bg 15
# """)


# if __name__ == "__main__":
#     args = sys.argv[1:]
#     if not args:
#         usage()
#         sys.exit(0)

#     mode = args[0]

#     if mode == "image":
#         if len(args) < 2: usage(); sys.exit(1)
#         path       = args[1]
#         style      = args[2] if len(args) > 2 else "ascii"
#         color_mode = args[3] if len(args) > 3 else "none"
#         print(convert_file(path, style=style, color_mode=color_mode,
#                            sharpen=True, contrast=1.3))

#     elif mode == "video":
#         if len(args) < 2: usage(); sys.exit(1)
#         path       = args[1]
#         style      = args[2] if len(args) > 2 else "ascii"
#         color_mode = args[3] if len(args) > 3 else "none"
#         fps        = float(args[4]) if len(args) > 4 else None
#         play_video(path, style=style, color_mode=color_mode, fps=fps)

#     else:
#         print(f"Unknown mode: '{mode}'")
#         usage()