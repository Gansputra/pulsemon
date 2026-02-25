import threading
import time
import msvcrt
import sys
from rich.live import Live
from rich.console import Console
from rich.prompt import Prompt
from .process import get_active_processes
from .monitor import get_system_stats, format_uptime
from .ui import create_process_table, create_stats_panel, create_layout, create_footer

class PulsemonApp:
    def __init__(self):
        self.console = Console()
        self.layout = create_layout()
        self.stop_event = threading.Event()
        self.sort_by = "cpu"
        self.filter_text = ""
        self.data = {
            "stats": None,
            "processes": [],
            "uptime_str": "Initializing..."
        }

    def fetch_data(self):
        """Worker thread function to fetch system data in the background."""
        while not self.stop_event.is_set():
            try:
                stats = get_system_stats()
                processes = get_active_processes()
                uptime_str = format_uptime(stats['uptime_seconds'])
                
                self.data["stats"] = stats
                self.data["processes"] = processes
                self.data["uptime_str"] = uptime_str
                
            except Exception:
                pass
            
            self.stop_event.wait(1)

    def handle_keyboard(self):
        """Handle non-blocking keyboard input."""
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8', errors='ignore').lower()
            if key == 'q':
                self.stop_event.set()
            elif key == 'c':
                self.sort_by = "cpu"
            elif key == 'm':
                self.sort_by = "ram"
            elif key == 'x':
                self.filter_text = ""
            elif key == 'f':
                return "prompt_filter"
        return None

    def run(self):
        # Initial fetch
        try:
            self.data["stats"] = get_system_stats()
            self.data["processes"] = get_active_processes()
            self.data["uptime_str"] = format_uptime(self.data["stats"]['uptime_seconds'])
        except Exception:
            pass

        data_thread = threading.Thread(target=self.fetch_data, daemon=True)
        data_thread.start()

        try:
            while not self.stop_event.is_set():
                with Live(self.layout, refresh_per_second=4, screen=True):
                    while not self.stop_event.is_set():
                        if self.data["stats"]:
                            self.layout["header"].update(
                                create_stats_panel(self.data["stats"], self.data["uptime_str"])
                            )
                            self.layout["body"].update(
                                create_process_table(self.data["processes"], self.sort_by, self.filter_text)
                            )
                            self.layout["footer"].update(
                                create_footer(self.sort_by, self.filter_text)
                            )
                        
                        action = self.handle_keyboard()
                        if action == "prompt_filter":
                            # Break out of Live to take input
                            break
                        
                        time.sleep(0.1)
                
                # Check if we broke out for filtering
                if not self.stop_event.is_set() and action == "prompt_filter":
                    # Clear screen briefly for prompt
                    self.console.print("\n" * 5)
                    self.filter_text = Prompt.ask("[bold yellow]Enter process name to filter[/bold yellow]")
                    # Live will restart on next iteration of outer loop
                
        except KeyboardInterrupt:
            self.stop_event.set()
        finally:
            self.stop_event.set()
            data_thread.join(timeout=0.5)

def main():
    app = PulsemonApp()
    app.run()

if __name__ == "__main__":
    main()
