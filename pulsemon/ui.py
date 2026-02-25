from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console
from rich import box

def create_process_table(processes):
    """
    Membuat tabel Rich untuk daftar proses.
    """
    table = Table(
        title="Active Processes",
        box=box.ROUNDED,
        header_style="bold cyan",
        expand=True
    )

    table.add_column("PID", justify="right", style="dim")
    table.add_column("Name", style="bold white")
    table.add_column("CPU %", justify="center", style="green")
    table.add_column("RAM (MB)", justify="right", style="magenta")

    # Sort proses berdasarkan CPU usage (tertinggi di atas)
    sorted_procs = sorted(processes, key=lambda x: x['cpu_usage'], reverse=True)[:15]

    for proc in sorted_procs:
        table.add_row(
            str(proc['pid']),
            proc['name'],
            f"{proc['cpu_usage']:.1f}%",
            f"{proc['ram_usage_mb']:.2f}"
        )

    return table

def create_stats_panel(stats, uptime_str):
    """
    Membuat panel statistik sistem.
    """
    content = (
        f"[bold blue]CPU Usage:[/bold blue] [green]{stats['cpu_percent']}%[/green] | "
        f"[bold blue]RAM:[/bold blue] [magenta]{stats['ram']['percent']}%[/magenta] ({stats['ram']['used_gb']}/{stats['ram']['total_gb']} GB) | "
        f"[bold blue]Uptime:[/bold blue] [yellow]{uptime_str}[/yellow]"
    )
    return Panel(content, title="[bold white]System Pulse[/bold white]", border_style="bright_blue", box=box.DOUBLE)

def create_layout():
    """
    Membuat struktur layout dasar UI.
    """
    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body")
    )
    return layout
