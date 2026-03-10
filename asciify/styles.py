from dataclasses import dataclass

PALETTE: dict[str, str] = {
    "ascii":    " .:-=+*#%@",
    "detailed": " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$",
    "blocks":   " ░▒▓█",
    "minimal":  " .:oO0@",
    "braille":  " ⠁⠃⠇⠏⠟⠿⣿",
    "matrix":   "ｦｧｨｩｪｫｬｭｮｯｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ",
    "dots":     " ·:;",
    "shade":    " ·∘○◎●",
    "color":    " .:-=+*#%@",
}

@dataclass(frozen=True)
class Style:
    name:        str
    description: str
    palette_key: str
    color:       bool = False


STYLES: dict[str, Style] = {
    "ascii":    Style("ascii",    "Classic ASCII art",                 "ascii"),
    "detailed": Style("detailed", "High-detail ASCII — 70+ chars",     "detailed"),
    "blocks":   Style("blocks",   "Unicode block shading  ░▒▓█",       "blocks"),
    "minimal":  Style("minimal",  "Clean, sparse ASCII",               "minimal"),
    "braille":  Style("braille",  "Braille dot patterns — very dense", "braille"),
    "matrix":   Style("matrix",   "Katakana chars — Matrix aesthetic", "matrix"),
    "dots":     Style("dots",     "Minimal dot art",                   "dots"),
    "shade":    Style("shade",    "Circle shade progression",          "shade"),
    "color":    Style("color",    "True color with foreground ANSI codes (auto-enables-c fg)",    "color",  color=True),
}


def get_style(name: str) -> Style:
    if name not in STYLES:
        available = ", ".join(STYLES.keys())
        raise ValueError(f"Unknown style '{name}'. Available: {available}")
    return STYLES[name]


def list_styles() -> None:
    from rich.table import Table
    from rich.console import Console

    console = Console()
    table = Table(
        title="[bold cyan]asciify — available styles[/bold cyan]",
        border_style="dim",
        show_lines=False,
    )
    table.add_column("Name",        style="bold green", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_column("Colour",      style="yellow",     justify="center")

    for s in STYLES.values():
        table.add_row(s.name, s.description, "✓" if s.color else "")

    console.print(table)
