import psutil

def get_active_processes():
    """
    Mengambil daftar proses aktif dengan informasi PID, nama, CPU usage, dan RAM usage.
    
    Returns:
        list[dict]: Daftar proses dalam format {'pid', 'name', 'cpu_usage', 'ram_usage_mb'}
    """
    processes_data = []
    
    # Menggunakan process_iter dengan atribut yang ditentukan untuk efisiensi
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            # Ambil info dasar
            info = proc.info
            
            # Konversi RAM (RSS) dari bytes ke MB
            ram_mb = info['memory_info'].rss / (1024 * 1024)
            
            processes_data.append({
                'pid': info['pid'],
                'name': info['name'],
                'cpu_usage': info['cpu_percent'],
                'ram_usage_mb': round(ram_mb, 2)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Lewati proses yang sudah tidak ada atau tidak memiliki izin akses
            continue
            
    return processes_data

def kill_process(pid):
    """
    Menghentikan proses berdasarkan PID.
    
    Returns:
        tuple (bool, str): (Berhasil/Tidak, Pesan Status)
    """
    try:
        proc = psutil.Process(pid)
        name = proc.name()
        proc.terminate() # Mencoba menghentikan secara halus
        return True, f"Berhasil mengirim sinyal terminasi ke {name} (PID: {pid})"
    except psutil.NoSuchProcess:
        return False, f"Error: Proses dengan PID {pid} tidak ditemukan."
    except psutil.AccessDenied:
        return False, f"Error: Akses ditolak. Izin administrator diperlukan untuk PID {pid}."
    except Exception as e:
        return False, f"Error: Gagal menghentikan proses: {str(e)}"
