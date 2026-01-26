import os

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.table import Table
from rich.text import Text

console = Console()


def create_scan_progress():
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=None, complete_style="cyan", finished_style="green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console,
        expand=True,
        # transient=True,  # optional: removes bar after finish
    )


def display_errors(errors):
    if not errors:
        return

    table = Table(title="Scan Failures", header_style="bold red", border_style="red")
    table.add_column("File Path")
    table.add_column("Reason")

    for path, reason in errors.items():
        table.add_row(os.path.relpath(path), reason)

    console.print("\n")
    console.print(
        Panel(table, title="[bold red]Warning: Skipped Files[/]", expand=False)
    )


def display_comparison_status():
    console.print("\n[bold blue] Analyzing changes...[/]")


def display_header():
    header_text = Text("AEGIS - File Integrity Monitor", style="bold cyan")
    console.print(Panel(header_text, subtitle="v1.0.0", expand=False))


def display_results(changes):
    table = Table(title="Security Audit Results", header_style="bold magenta")
    table.add_column("Status", width=15)
    table.add_column("File Path")
    table.add_column("Details", width=30)

    def get_short_path(p):
        return os.path.relpath(p, os.getcwd())

    for path in changes["new"]:
        table.add_row("NEW", get_short_path(path), "", style="green")
    for path in changes["modified"]:
        table.add_row(
            "MODIFIED", get_short_path(path), "Content changes", style="yellow"
        )

    for item in changes["metadata_changed"]:
        path = item["path"]
        details = []
        if item["old_size"] != item["new_size"]:
            details.append(f"Size: {item['old_size']}->{item['new_size']}")
        if item["old_permissions"] != item["new_permissions"]:
            details.append(
                f"Permissions: {item['old_permissions']}->{item['new_permissions']}"
            )
        table.add_row(
            "METADATA", get_short_path(path), ", ".join(details), style="cyan"
        )

    for path in changes["deleted"]:
        table.add_row("DELETED", get_short_path(path), "", style="red")

    console.print(table)


def display_summary(total, new, modified, deleted, metadata=0):
    table = Table(show_header=True, header_style="bold blue", box=None)
    table.add_column("Total Files", justify="center")
    table.add_column("New", style="green", justify="center")
    table.add_column("Modified", style="yellow", justify="center")
    table.add_column("Metadata", style="cyan", justify="center")
    table.add_column("Deleted", style="red", justify="center")

    table.add_row(str(total), str(new), str(modified), str(metadata), str(deleted))

    console.print(Panel(table, title="Scan Summary", expand=False))


def display_metadata_diffs(metadata_changes):
    if not metadata_changes:
        return

    table = Table(title="Detailed Metadata Changes", header_style="bold cyan", box=None)
    table.add_column("File Path")
    table.add_column("Attribute")
    table.add_column("Old Value", style="red")
    table.add_column("New Value", style="green")

    for item in metadata_changes:
        path = os.path.relpath(item["path"])

        if item["old_size"] != item["new_size"]:
            table.add_row(
                path, "Size", f"{item['old_size']} B", f"{item['new_size']} B"
            )

        if item["old_permissions"] != item["new_permissions"]:
            table.add_row(
                path,
                "Permissions",
                f"{item['old_permissions']}",
                f"{item['new_permissions']}",
            )

    console.print("\n")
    console.print(
        Panel(table, title="[bold cyan]Metadata Audit Breakdown[/]", expand=False)
    )
