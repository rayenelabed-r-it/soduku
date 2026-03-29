import psutil
import time


def start_timer():
    """Démarre le chronomètre et retourne le temps initial."""
    return time.time()


def stop_timer(debut_chrono):
    """Calcule et retourne le temps écoulé depuis debut_chrono."""
    fin_chrono = time.time()
    temps_total = fin_chrono - debut_chrono
    return temps_total


def get_system_stats():
    """Récupère les informations CPU et RAM pour les afficher dans l'interface."""
    # --- Infos CPU ---
    core = psutil.cpu_count()
    # On utilise un petit intervalle (0.1s) pour ne pas figer l'interface graphique
    cpu_usage = psutil.cpu_percent(interval=0.1)

    # --- Infos RAM ---
    ram = psutil.virtual_memory()
    ram_used_gb = ram.used / (1024**3)
    ram_total_gb = ram.total / (1024**3)
    ram_percent = ram.percent  # psutil donne déjà le pourcentage exact

    # On retourne un dictionnaire propre, facile à lire par le GUI
    return {
        "cpu_cores": core,
        "cpu_usage": f"{cpu_usage}%",
        "ram_used": f"{ram_used_gb:.2f} GB",
        "ram_total": f"{ram_total_gb:.2f} GB",
        "ram_percent": f"{ram_percent}%",
    }
