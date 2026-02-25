import threading
import time
import msvcrt
import sys
from rich.live import Live
from rich.console import Console
from rich.prompt import Prompt
from .process import get_active_processes, kill_process
from .monitor import get_system_stats, format_uptime
from .ui import create_process_table, create_stats_panel, create_layout, create_footer

class PulsemonApp:
    def __init__(self):
        self.console = Console()
        self.layout = create_layout()
        self.stop_event = threading.Event()
        self.sort_by = "cpu"
        self.filter_text = ""
        self.status_msg = ""
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
            elif key == 'k':
                return "prompt_kill"
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
                                create_footer(self.sort_by, self.filter_text, self.status_msg)
                            )
                        
                        action = self.handle_keyboard()
                        if action in ["prompt_filter", "prompt_kill"]:
                            break
                        
                        time.sleep(0.1)
                
                if self.stop_event.is_set():
                    break

                if action == "prompt_filter":
                    self.console.print("\n" * 5)
                    self.filter_text = Prompt.ask("[bold yellow]Enter process name to filter[/bold yellow]")
                    self.status_msg = f"Filter diatur ke: {self.filter_text}" if self.filter_text else "Filter dihapus"
                
                elif action == "prompt_kill":
                    self.console.print("\n" * 5)
                    pid_str = Prompt.ask("[bold red]Enter PID to kill[/bold red]")
                    try:
                        pid = int(pid_str)
                        confirm = Prompt.ask(f"[bold red]Are you sure you want to kill PID {pid}?[/bold red] (y/n)", choices=["y", "n"], default="n")
                        if confirm == "y":
                            success, msg = kill_process(pid)
                            self.status_msg = msg
                        else:
                            self.status_msg = "Aksi dibatalkan"
                    except ValueError:
                        self.status_msg = "Error: PID harus berupa angka"
                
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
