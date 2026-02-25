import psutil
import time
from datetime import datetime

def get_system_stats():
    """
    Mengambil statistik sistem secara keseluruhan (CPU, RAM, Uptime).
    
    Returns:
        dict: Statistik sistem yang berisi cpu_total, ram_total, dan uptime.
    """
    # CPU usage total (%)
    # Menggunakan interval=0.1 untuk akurasi instan atau None jika dipanggil berkala
    cpu_percent = psutil.cpu_percent(interval=0.1)
    
    # RAM usage total
    virtual_mem = psutil.virtual_memory()
    ram_data = {
        'total_gb': round(virtual_mem.total / (1024**3), 2),
        'used_gb': round(virtual_mem.used / (1024**3), 2),
        'percent': virtual_mem.percent
    }
    
    # System Uptime
    boot_time_timestamp = psutil.boot_time()
    uptime_seconds = time.time() - boot_time_timestamp
    
    return {
        'cpu_percent': cpu_percent,
        'ram': ram_data,
        'uptime_seconds': int(uptime_seconds),
        'boot_time': datetime.fromtimestamp(boot_time_timestamp).strftime("%Y-%m-%d %H:%M:%S")
    }

def format_uptime(seconds):
    """
    Mengonversi detik ke format string yang mudah dibaca (H:M:S).
    """
    days, remaining = divmod(seconds, 86400)
    hours, remaining = divmod(remaining, 3600)
    minutes, seconds = divmod(remaining, 60)
    
    parts = []
    if days > 0:
        parts.append(f"{int(days)}d")
    if hours > 0:
        parts.append(f"{int(hours)}h")
    if minutes > 0:
        parts.append(f"{int(minutes)}m")
    parts.append(f"{int(seconds)}s")
    
    return " ".join(parts)
