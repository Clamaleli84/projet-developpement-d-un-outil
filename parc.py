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

CHEMIN = "~/Donnees_itinerantes_depuis_serveur_pedagogique/developpe_outil"

def collecter_machine(machine):
    host = machine["host"]
    nom = machine["nom"]
    storage = StorageManager(db_path=f"metrics_{nom}.db")
    if host is None:
        import psutil
        cpu = psutil.cpu_percent(interval=1)
        storage.save("cpu", cpu, "%")
        print(f"[{nom}] CPU : {cpu}%")
    else:
        # CPU
        cpu_str = collecter_distant(host, f"python3 {CHEMIN}/cpu.py")
        print(f"[{nom}] CPU brut : '{cpu_str}'")

        # RAM
        ram_str = collecter_distant(host, f"bash {CHEMIN}/ram.sh")
        print(f"[{nom}] RAM brut : '{ram_str}'")

        # Disque
        disque_str = collecter_distant(host, f"bash {CHEMIN}/disque.sh")
        print(f"[{nom}] Disque brut : '{disque_str}'")
if __name__ == "__main__":
    for machine in MACHINES:
        collecter_machine(machine)
