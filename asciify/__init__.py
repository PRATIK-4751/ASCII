from .converter import ImageConverter
from .video import VideoConverter
from .styles import STYLES, list_styles
from .version import __version__

__all__ = ["ImageConverter", "VideoConverter", "STYLES", "list_styles", "__version__"]


def main():
    from .cli import app
    app()
