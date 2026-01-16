from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def display_header():
    header_text = Text("AEGIS - File Integrity Monitor", style="bold cyan")
    console.print(Panel(header_text, subtitle="v0.1.1", expand=False))
