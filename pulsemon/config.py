import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "refresh_rate": 1.0,
    "cpu_threshold": 85.0,
    "ram_threshold": 85.0,
    "default_sort": "cpu",
    "max_processes": 15
}

class Config:
    def __init__(self):
        self.settings = DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        """Memuat konfigurasi dari file JSON."""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    loaded_config = json.load(f)
                    self.settings.update(loaded_config)
            except (json.JSONDecodeError, IOError):
                pass # Gunakan default jika gagal baca

    def save(self):
        """Menyimpan konfigurasi ke file JSON."""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except IOError:
            pass

    def get(self, key):
        """Mengambil nilai konfigurasi."""
        return self.settings.get(key, DEFAULT_CONFIG.get(key))

    def set(self, key, value):
        """Mengatur nilai konfigurasi."""
        if key in self.settings:
            self.settings[key] = value
            self.save()

# Instance global untuk akses mudah
config = Config()
