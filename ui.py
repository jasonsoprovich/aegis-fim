import os

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


def display_header():
    header_text = Text("AEGIS - File Integrity Monitor", style="bold cyan")
    console.print(Panel(header_text, subtitle="v0.1.1", expand=False))


def display_results(changes):
    table = Table(title="Security Audit Results", header_style="bold magenta")
    table.add_column("Status", width=12)
    table.add_column("File Path")

    def get_short_path(p):
        return os.path.relpath(p, os.getcwd())

    for path in changes["new"]:
        table.add_row("NEW", get_short_path(path), style="green")
    for path in changes["modified"]:
        table.add_row("MODIFIED", get_short_path(path), style="yellow")
    for path in changes["deleted"]:
        table.add_row("DELETED", get_short_path(path), style="red")

    console.print(table)
