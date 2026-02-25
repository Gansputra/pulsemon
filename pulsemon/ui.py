from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console
from rich import box
from rich.text import Text

def create_process_table(processes, sort_by="cpu", filter_text=""):
    """
    Membuat tabel Rich untuk daftar proses dengan fitur sorting dan filtering.
    """
    title = f"Active Processes (Sorted by {sort_by.upper()})"
    if filter_text:
        title += f" [Filter: '{filter_text}']"

    table = Table(
        title=title,
        box=box.ROUNDED,
        header_style="bold cyan",
        expand=True
    )

    table.add_column("PID", justify="right", style="dim")
    table.add_column("Name", style="bold white")
    table.add_column("CPU %", justify="center", style="green")
    table.add_column("RAM (MB)", justify="right", style="magenta")

    # Filtering
    filtered_procs = processes
    if filter_text:
        filtered_procs = [p for p in processes if filter_text.lower() in p['name'].lower()]

    # Sorting
    sort_key = 'cpu_usage' if sort_by == 'cpu' else 'ram_usage_mb'
    sorted_procs = sorted(filtered_procs, key=lambda x: x[sort_key], reverse=True)[:15]

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

def create_footer(sort_by, filter_text, status_msg=""):
    """
    Membuat footer navigasi bantuan.
    """
    help_line = Text.from_markup(
        "[bold yellow]C[/bold yellow]: CPU | "
        "[bold yellow]M[/bold yellow]: RAM | "
        "[bold yellow]F[/bold yellow]: Filter | "
        "[bold yellow]K[/bold yellow]: [bold red]Kill[/bold red] | "
        "[bold yellow]X[/bold yellow]: Clear | "
        "[bold yellow]Q[/bold yellow]: Quit"
    )
    
    current_state = f" [Dim: Sort={sort_by.upper()}, Filter='{filter_text}']"
    
    footer_content = help_line + Text(current_state, style="dim italic")
    
    if status_msg:
        color = "green" if "Berhasil" in status_msg else "red"
        footer_content += Text(f"\nStatus: {status_msg}", style=f"bold {color}")
        
    return Panel(footer_content, border_style="dim")

def create_layout():
    """
    Membuat struktur layout dasar UI.
    """
    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=5)
    )
    return layout
