import subprocess
from storage import StorageManager

MACHINES = [
    {
        "nom": "vm_locale",
        "host": None  # None = machine locale
    },
    {
        "nom": "ordi_local",
        "host": "uapv2401108@pedago.univ-avignon.fr"
    }
]

def collecter_distant(host, commande):
    """Lance une commande sur une machine distante via SSH"""
    result = subprocess.run(
        ["ssh", host, commande],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def collecter_machine(machine):
    host = machine["host"]
    nom = machine["nom"]
    storage = StorageManager(db_path=f"metrics_{nom}.db")

    if host is None:
        # Machine locale — utilise psutil directement
        import psutil
        cpu = psutil.cpu_percent(interval=1)
        storage.save("cpu", cpu, "%")
        print(f"[{nom}] CPU : {cpu}%")
    else:
        # Machine distante — via SSH
        # CPU
        cpu_str = collecter_distant(host, "python3 ~/Donnees_itinerantes/developpe_outil/cpu.py")
        try:
            cpu = float(cpu_str.split(":")[1].replace("%", "").strip())
            storage.save("cpu", cpu, "%")
            print(f"[{nom}] CPU : {cpu}%")
        except Exception as e:
            print(f"[{nom}] Erreur CPU : {e}")

        # RAM
        ram_str = collecter_distant(host, "bash ~/Donnees_itinerantes/developpe_outil/ram.sh")
        try:
            ram = float(ram_str.split(":")[1].replace("%", "").strip())
            storage.save("ram", ram, "%")
            print(f"[{nom}] RAM : {ram}%")
        except Exception as e:
            print(f"[{nom}] Erreur RAM : {e}")

        # Disque
        disque_str = collecter_distant(host, "bash ~/Donnees_itinerantes/developpe_outil/disque.sh")
        print(f"[{nom}] Disque : {disque_str}")

if __name__ == "__main__":
    for machine in MACHINES:
        collecter_machine(machine)
