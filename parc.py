import subprocess
from storage import StorageManager
import psutil

MACHINES = [
    {"nom": "vm_locale", "host": None},
    {"nom": "ordi_local", "host": "uapv2401108@pedago.univ-avignon.fr"}
]

def collecter_distant(host, commande):
    try:
        # On ajoute -o BatchMode=yes pour éviter que SSH ne bloque sur un mot de passe
        result = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", host, commande], 
                                capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception:
        return ""

def collecter_machine(machine):
    nom = machine["nom"]
    host = machine["host"]
    storage = StorageManager(db_path=f"metrics_{nom}.db")

    # Initialisation des variables pour éviter l'UnboundLocalError
    cpu, ram, disque = 0.0, 0.0, 0.0

    if host is None:
        # --- COLLECTE LOCALE ---
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory().percent
        disque = psutil.disk_usage('/').percent
        print(f"[{nom}] Local - CPU: {cpu}%, RAM: {ram}%")
    else:
        # --- COLLECTE DISTANTE ---
        res_cpu = collecter_distant(host, "top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
        res_ram = collecter_distant(host, "free | grep Mem | awk '{print $3/$2 * 100.0}'")
        res_dis = collecter_distant(host, "df / | tail -1 | awk '{print $5}' | sed 's/%//'")
        
        try:
            # On utilise float(x.replace(',', '.')) car les systèmes FR utilisent la virgule
            cpu = float(res_cpu.replace(',', '.')) if res_cpu else 0.5
            ram = float(res_ram.replace(',', '.')) if res_ram else 15.0
            disque = float(res_dis.replace(',', '.')) if res_dis else 10.0
            print(f">>> [{nom}] Distant - CPU: {cpu}%, RAM: {ram}%")
        except Exception as e:
            print(f"[{nom}] Erreur conversion SSH: {e}")
            # Valeurs par défaut différentes pour bien voir la distinction sur le graphe
            cpu, ram, disque = 1.0, 20.0, 30.0

    # Sauvegarde dans la base spécifique
    storage.save("cpu", cpu, "%")
    storage.save("ram", ram, "%")
    storage.save("disque", disque, "%")

if __name__ == "__main__":
    for m in MACHINES:
        collecter_machine(m)
