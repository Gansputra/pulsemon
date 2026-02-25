from datetime import datetime

class AlertManager:
    def __init__(self, cpu_threshold=90.0, ram_threshold=90.0):
        self.cpu_threshold = cpu_threshold
        self.ram_threshold = ram_threshold
        self.active_alerts = []

    def check_system_stats(self, stats):
        """
        Memeriksa statistik sistem terhadap threshold.
        """
        new_alerts = []
        
        # Check CPU
        if stats['cpu_percent'] > self.cpu_threshold:
            new_alerts.append({
                'type': 'CPU',
                'value': stats['cpu_percent'],
                'message': f"HIGH CPU USAGE: {stats['cpu_percent']}%",
                'time': datetime.now().strftime("%H:%M:%S")
            })
            
        # Check RAM
        if stats['ram']['percent'] > self.ram_threshold:
            new_alerts.append({
                'type': 'RAM',
                'value': stats['ram']['percent'],
                'message': f"HIGH RAM USAGE: {stats['ram']['percent']}%",
                'time': datetime.now().strftime("%H:%M:%S")
            })
            
        # Kita hanya simpan alert terbaru untuk ditampilkan
        self.active_alerts = new_alerts
        return self.active_alerts

    def get_latest_alerts(self):
        """Mengambil daftar alert aktif."""
        return self.active_alerts
