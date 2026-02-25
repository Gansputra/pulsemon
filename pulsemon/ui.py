from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console
from rich import box
from rich.text import Text

def create_process_table(processes, sort_by="cpu", filter_text="", max_rows=15):
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
    sorted_procs = sorted(filtered_procs, key=lambda x: x[sort_key], reverse=True)[:max_rows]

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
    Membuat panel statistik sistem dengan gaya premium.
    """
    content = (
        f"[bold cyan]CPU[/bold cyan] [white]━━[/white] [bold green]{stats['cpu_percent']:>5}%[/bold green]   "
        f"[bold magenta]RAM[/bold magenta] [white]━━[/white] [bold magenta]{stats['ram']['percent']:>5}%[/bold magenta] [dim]({stats['ram']['used_gb']}/{stats['ram']['total_gb']} GB)[/dim]   "
        f"[bold yellow]UPTIME[/bold yellow] [white]━━[/white] [bold yellow]{uptime_str}[/bold yellow]"
    )
    return Panel(content, title="[bold white] PULSEMON SYSTEM MONITOR [dim]by GANSPUTRA[/dim][/bold white]", border_style="bright_blue", box=box.ROUNDED)

def create_alerts_panel(alerts):
    """
    Membuat panel untuk menampilkan peringatan sistem.
    """
    if not alerts:
        return Panel(Text("No active alerts", style="dim green"), title="[bold]Alerts[/bold]", border_style="green")
    
    alert_texts = []
    for alert in alerts:
        alert_texts.append(f"[{alert['time']}] [bold red]⚠ {alert['message']}[/bold red]")
    
    content = "\n".join(alert_texts)
    return Panel(content, title="[bold red]System Alerts[/bold red]", border_style="red", box=box.HEAVY)

def create_footer(sort_by, filter_text, status_msg=""):
    """
    Membuat footer navigasi bantuan yang lebih mudah dipahami user.
    """
    # Menampilkan shortcut dan state aktif secara langsung
    sort_info = f"[bold cyan][S][/bold cyan] Sort: [bold white]{sort_by.upper()}[/bold white]"
    filter_info = f"[bold cyan][F][/bold cyan] Filter: [bold white]{filter_text or '-'}[/bold white]"
    kill_info = "[bold cyan][K][/bold cyan] [bold red]Kill PID[/bold red]"
    clear_info = "[bold cyan][X][/bold cyan] Clear"
    quit_info = "[bold cyan][Q][/bold cyan] Quit"
    
    # Gabungkan dengan separator yang bersih
    footer_content = Text.from_markup(f"{sort_info}  │  {filter_info}  │  {kill_info}  │  {clear_info}  │  {quit_info}")
    
    if status_msg:
        # Menambahkan pesan status dengan pemisah di bawahnya
        color = "green" if "Berhasil" in status_msg else "red"
        # Pastikan status_msg tidak terlalu panjang
        status_line = Text.from_markup(f"\n[dim]System:[/dim] [bold {color}]{status_msg}[/bold {color}]")
        return Panel(footer_content + status_line, border_style="dim", box=box.ROUNDED)
    
    return Panel(footer_content, border_style="dim", box=box.ROUNDED)

def create_layout():
    """
    Membuat struktur layout dasar UI.
    """
    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="alerts", size=5),
        Layout(name="body"),
        Layout(name="footer", size=5)
    )
    return layout
