import subprocess
from storage import StorageManager
import psutil

MACHINES = [
    {"nom": "vm_locale", "host": None},
    {"nom": "ordi_local", "host": "uapv2401108@pedago.univ-avignon.fr"}
]

def collecter_distant(host, commande):
    try:
        result = subprocess.run(["ssh", "-o", "ConnectTimeout=5", host, commande], 
                                capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except:
        return ""

def collecter_machine(machine):
    nom = machine["nom"]
    host = machine["host"]
    storage = StorageManager(db_path=f"metrics_{nom}.db")

    if host is None:
        # LOCAL
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory().percent
        disque = psutil.disk_usage('/').percent
    else:
        # DISTANT (SSH) - On utilise des commandes directes pour éviter les scripts manquants
        cpu_raw = collecter_distant(host, "uptime | awk '{print $NF}' | sed 's/,/./'")
        ram_raw = collecter_distant(host, "free | grep Mem | awk '{print $3/$2 * 100.0}'")
        disque_raw = collecter_distant(host, "df / | tail -1 | awk '{print $5}' | sed 's/%//'")
        
        try:
            cpu = float(cpu_raw) if cpu_raw else 0.0
            ram = float(ram_raw) if ram_raw else 0.0
            disque = float(disque_raw) if disque_raw else 0.0
        except:
            cpu, ram, disque = 0.0, 0.0, 0.0

    storage.save("cpu", cpu, "%")
    storage.save("ram", ram, "%")
    storage.save("disque", disque, "%")
    print(f"[{nom}] Données sauvegardées : CPU {cpu}%, RAM {ram}%, DISQUE {disque}%")

if __name__ == "__main__":
    for m in MACHINES:
        collecter_machine(m)
