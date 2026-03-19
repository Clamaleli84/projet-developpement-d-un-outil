import subprocess
from storage import StorageManager

CHEMIN = "~/Donnees_itinerantes_depuis_serveur_pedagogique/developpe_outil"

MACHINES = [
    {
        "nom": "vm_locale",
        "host": None
    },
    {
        "nom": "ordi_local",
        "host": "uapv2401108@pedago.univ-avignon.fr"
    }
]

def collecter_distant(host, commande):
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
        import psutil
        cpu = psutil.cpu_percent(interval=1)
        storage.save("cpu", cpu, "%")
        print(f"[{nom}] CPU : {cpu}%")

        import subprocess
        ram_result = subprocess.run(
            ["bash", "/home/leojaubert/projet-developpement-d-un-outil/ram.sh"],
            capture_output=True, text=True
        )
        ligne = ram_result.stdout.strip()
        try:
            ram = float(ligne.split(":")[1].strip().replace("%", ""))
            storage.save("ram", ram, "%")
            print(f"[{nom}] RAM : {ram}%")
        except Exception as e:
            print(f"[{nom}] Erreur RAM : {e}")

        disque_result = subprocess.run(
            ["bash", "/home/leojaubert/projet-developpement-d-un-outil/disque.sh"],
            capture_output=True, text=True
        )
        for ligne in disque_result.stdout.splitlines():
            if "utilisé" in ligne.lower():
                try:
                    partie = ligne.split(":")[1].strip()
                    pct = partie.split(",")[-1].replace("%", "").strip()
                    storage.save("disque", float(pct), "%")
                    print(f"[{nom}] Disque : {pct}%")
                except Exception as e:
                    print(f"[{nom}] Erreur disque : {e}")

    else:
        # CPU via bash
        cpu_str = collecter_distant(host, "top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
        print(f"[{nom}] CPU brut : '{cpu_str}'")
        try:
            cpu = float(cpu_str.replace("%", "").strip())
            storage.save("cpu", cpu, "%")
            print(f"[{nom}] CPU : {cpu}%")
        except Exception as e:
            print(f"[{nom}] Erreur CPU : {e}")

        # RAM
        ram_str = collecter_distant(host, f"bash {CHEMIN}/ram.sh")
        print(f"[{nom}] RAM brut : '{ram_str}'")
        try:
            ram = float(ram_str.split(":")[1].strip().replace("%", ""))
            storage.save("ram", ram, "%")
            print(f"[{nom}] RAM : {ram}%")
        except Exception as e:
            print(f"[{nom}] Erreur RAM : {e}")

        # Disque
        disque_str = collecter_distant(host, f"bash {CHEMIN}/disque.sh")
        print(f"[{nom}] Disque brut : '{disque_str}'")
        for ligne in disque_str.splitlines():
            if "utilisé" in ligne.lower():
                try:
                    partie = ligne.split(":")[1].strip()
                    pct = partie.split(",")[-1].replace("%", "").strip()
                    storage.save("disque", float(pct), "%")
                    print(f"[{nom}] Disque : {pct}%")
                except Exception as e:
                    print(f"[{nom}] Erreur disque : {e}")

if __name__ == "__main__":
    for machine in MACHINES:
        collecter_machine(machine)
