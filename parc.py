import subprocess
from storage import StorageManager
import psutil

MACHINES = [{"nom": "vm_locale", "host": None}, {"nom": "ordi_local", "host": "uapv2401108@pedago.univ-avignon.fr"}]

def collecter_distant(host, commande):
    try:
        # On ajoute -o BatchMode=yes pour éviter que SSH ne bloque sur un mot de passe
        result = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", host, commande], 
                                capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception:
        return ""
        


def collecter_machine(machine):
    nom, host = machine["nom"], machine["host"]
    storage = StorageManager(db_path=f"metrics_{nom}.db")
    cpu, ram, disque = 0.0, 0.0, 0.0 # On initialise pour éviter les erreurs

    if host is None:
        cpu, ram = psutil.cpu_percent(interval=1), psutil.virtual_memory().percent
        disque = psutil.disk_usage('/').percent
    else:
        # On utilise des commandes SSH directes pour le serveur pedago
        c = lambda cmd: subprocess.run(["ssh", host, cmd], capture_output=True, text=True).stdout.strip()
        try:
            cpu = float(c("top -bn1 | grep 'Cpu(s)' | awk '{print $2}'").replace(',', '.'))
            ram = float(c("free | grep Mem | awk '{print $3/$2 * 100.0}'").replace(',', '.'))
            disque = float(c("df / | tail -1 | awk '{print $5}'").replace('%',''))
        except: pass

    storage.save("cpu", cpu, "%")
    storage.save("ram", ram, "%")
    storage.save("disque", disque, "%")
    print(f"[{nom}] OK : CPU {cpu}% | RAM {ram}%")

if __name__ == "__main__":
    for m in MACHINES: collecter_machine(m)
