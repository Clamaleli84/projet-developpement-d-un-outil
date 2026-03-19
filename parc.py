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
        # --- COLLECTE DISTANTE ---
        # On utilise des noms de variables très différents pour éviter tout mélange
        res_cpu = collecter_distant(host, "top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
        res_ram = collecter_distant(host, "free | grep Mem | awk '{print $3/$2 * 100.0}'")
        res_dis = collecter_distant(host, "df / | tail -1 | awk '{print $5}' | sed 's/%//'")

        try:
            # On remplace les virgules par des points (important pour le float)
            val_cpu = float(res_cpu.replace(',', '.')) if res_cpu else 0.1
            val_ram = float(res_ram.replace(',', '.')) if res_ram else 0.1
            val_dis = float(res_dis.replace(',', '.')) if res_dis else 0.1
            
            # SAUVEGARDE STRICTE
            storage.save("cpu", val_cpu, "%")
            storage.save("ram", val_ram, "%")
            storage.save("disque", val_dis, "%")
            print(f">>> DISTANT [{nom}] : CPU={val_cpu}, RAM={val_ram}")
        except Exception as e:
            print(f"Erreur distant {nom}: {e}")

    storage.save("cpu", cpu, "%")
    storage.save("ram", ram, "%")
    storage.save("disque", disque, "%")
    print(f"[{nom}] Données sauvegardées : CPU {cpu}%, RAM {ram}%, DISQUE {disque}%")

if __name__ == "__main__":
    for m in MACHINES:
        collecter_machine(m)
