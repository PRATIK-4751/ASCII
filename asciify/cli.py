from pathlib import Path
from typing import Optional
import re
import sys

import typer
from rich.console import Console

from .converter import ImageConverter
from .video import VideoConverter
from .styles import list_styles, STYLES

app = typer.Typer(
    name="asciify",
    help="Convert images and videos into ASCII / ANSI art in your terminal.",
    add_completion=False,
    no_args_is_help=True,
)

console = Console()

COLOR_MODES = ["none", "fg", "bg", "both"]


def _validate_style(style: str) -> None:
    if style not in STYLES:
        available = ", ".join(STYLES.keys())
        console.print(f"[red]Unknown style:[/red] '{style}'")
        console.print(f"[dim]Available:[/dim] {available}")
        raise typer.Exit(1)


def _validate_color_mode(color_mode: str) -> None:
    if color_mode not in COLOR_MODES:
        console.print(f"[red]Unknown color mode:[/red] '{color_mode}'")
        console.print(f"[dim]Available:[/dim] {', '.join(COLOR_MODES)}")
        raise typer.Exit(1)


@app.command("image")
def cmd_image(
    path: Path = typer.Argument(
        ...,
        help="Path to the image file (jpg, png, gif, bmp, webp …)",
        exists=True,
        readable=True,
    ),
    style: str = typer.Option(
        "ascii", "--style", "-s",
        help="Art style. Run `asciify styles` to see all options.",
    ),
    color_mode: Optional[str] = typer.Option(
        None, "--color-mode", "-c",
        help="Colour mode: none | fg | bg | both. Auto-enabled for 'color' style.",
    ),
    width: Optional[int] = typer.Option(
        None, "--width", "-w",
        help="Output width in characters. Default: terminal width.",
    ),
    invert: bool = typer.Option(
        False, "--invert", "-i",
        help="Invert brightness mapping.",
    ),
    contrast: float = typer.Option(
        1.2, "--contrast",
        help="Contrast multiplier. 1.0 = off, 1.5 = medium, 2.0 = strong.",
    ),
    sharpen: bool = typer.Option(
        False, "--sharpen",
        help="Apply a sharpen filter before converting.",
    ),
    edge: bool = typer.Option(
        False, "--edge",
        help="Apply an edge-enhance filter before converting.",
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o",
        help="Save art to a text file instead of printing to terminal.",
    ),
):
    _validate_style(style)
    
    # Auto-enable color mode for 'color' style
    if color_mode is None:
        if style == "color":
            color_mode = "fg"
        else:
            color_mode = "none"
    
    _validate_color_mode(color_mode)

    try:
        conv = ImageConverter(
            style=style,
            color_mode=color_mode,
            width=width,
            invert=invert,
            contrast=contrast,
            sharpen=sharpen,
            edge=edge,
        )
        art = conv.convert_file(path)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    if output:
        clean = re.sub(r"\033\[[0-9;]*m", "", art)
        output.write_text(clean, encoding="utf-8")
        console.print(f"[green]Saved to[/green] {output}")
    else:
        sys.stdout.write(art)
        sys.stdout.write("\n")
        sys.stdout.flush()


@app.command("video")
def cmd_video(
    path: Path = typer.Argument(
        ...,
        help="Path to the video file (mp4, avi, mov, mkv …)",
        exists=True,
        readable=True,
    ),
    style: str = typer.Option(
        "ascii", "--style", "-s",
        help="Art style. Run `asciify styles` to see all options.",
    ),
    color_mode: Optional[str] = typer.Option(
        None, "--color-mode", "-c",
        help="Colour mode: none | fg | bg | both. Auto-enabled for 'color' style.",
    ),
    width: Optional[int] = typer.Option(
        None, "--width", "-w",
        help="Output width in characters. Default: terminal width.",
    ),
    fps: Optional[float] = typer.Option(
        None, "--fps", "-f",
        help="Playback FPS. Default: video's native FPS.",
    ),
    loop: bool = typer.Option(
        False, "--loop", "-l",
        help="Loop the video. Press Ctrl+C to stop.",
    ),
    invert: bool = typer.Option(
        False, "--invert", "-i",
        help="Invert brightness mapping.",
    ),
    contrast: float = typer.Option(
        1.2, "--contrast",
        help="Contrast multiplier. 1.0 = off, 1.5 = medium, 2.0 = strong.",
    ),
):
    _validate_style(style)
    
    # Auto-enable color mode for 'color' style
    if color_mode is None:
        if style == "color":
            color_mode = "fg"
        else:
            color_mode = "none"
    
    _validate_color_mode(color_mode)

    try:
        vc = VideoConverter(
            style=style,
            color_mode=color_mode,
            width=width,
            fps=fps,
            loop=loop,
            invert=invert,
            contrast=contrast,
        )
        vc.play(path)

    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command("styles")
def cmd_styles():
    list_styles()


@app.command("version")
def cmd_version():
    try:
        from importlib.metadata import version
        v = version("asciify")
    except Exception:
        v = "unknown"
    console.print(f"asciify [bold cyan]{v}[/bold cyan]")


if __name__ == "__main__":
    app()
