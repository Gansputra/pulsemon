import time
from rich.live import Live
from rich.console import Console
from .process import get_active_processes
from .monitor import get_system_stats, format_uptime
from .ui import create_process_table, create_stats_panel, create_layout

def main():
    console = Console()
    layout = create_layout()
    
    with Live(layout, refresh_per_second=1, screen=True) as live:
        try:
            while True:
                # Ambil data terbaru
                stats = get_system_stats()
                processes = get_active_processes()
                uptime_str = format_uptime(stats['uptime_seconds'])
                
                # Update UI Components
                layout["header"].update(create_stats_panel(stats, uptime_str))
                layout["body"].update(create_process_table(processes))
                
                # Tunggu sebelum refresh berikutnya (psutil.cpu_percent sudah ada delay di monitor.py)
                time.sleep(0.9) # Sedikit di bawah 1 detik karena pemrosesan butuh waktu
                
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
