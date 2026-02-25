import threading
import time
from rich.live import Live
from rich.console import Console
from .process import get_active_processes
from .monitor import get_system_stats, format_uptime
from .ui import create_process_table, create_stats_panel, create_layout

class PulsemonApp:
    def __init__(self):
        self.console = Console()
        self.layout = create_layout()
        self.stop_event = threading.Event()
        self.data = {
            "stats": None,
            "processes": [],
            "uptime_str": "Initializing..."
        }

    def fetch_data(self):
        """Worker thread function to fetch system data in the background."""
        while not self.stop_event.is_set():
            try:
                # Ambil data terbaru dari hardware
                stats = get_system_stats()
                processes = get_active_processes()
                uptime_str = format_uptime(stats['uptime_seconds'])
                
                # Update shared data state
                self.data["stats"] = stats
                self.data["processes"] = processes
                self.data["uptime_str"] = uptime_str
                
            except Exception:
                # Keep thread alive on intermittent errors
                pass
            
            # Sleep using event wait for graceful interruption
            self.stop_event.wait(1)

    def run(self):
        # Initial fetch to populate UI immediately
        try:
            self.data["stats"] = get_system_stats()
            self.data["processes"] = get_active_processes()
            self.data["uptime_str"] = format_uptime(self.data["stats"]['uptime_seconds'])
        except Exception:
            pass

        # Start background thread for continuous data fetching
        data_thread = threading.Thread(target=self.fetch_data, daemon=True)
        data_thread.start()

        try:
            # Live display rendering loop
            with Live(self.layout, refresh_per_second=4, screen=True):
                while not self.stop_event.is_set():
                    if self.data["stats"]:
                        # Update UI elements with latest shared data
                        self.layout["header"].update(
                            create_stats_panel(self.data["stats"], self.data["uptime_str"])
                        )
                        self.layout["body"].update(
                            create_process_table(self.data["processes"])
                        )
                    # UI refresh loop heartbeat
                    time.sleep(0.1)
        except KeyboardInterrupt:
            # Graceful shutdown on Ctrl+C
            self.stop_event.set()
        finally:
            self.stop_event.set()
            data_thread.join(timeout=0.5)

def main():
    app = PulsemonApp()
    app.run()

if __name__ == "__main__":
    main()
