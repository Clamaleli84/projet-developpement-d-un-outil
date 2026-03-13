import subprocess
import psutil
from stockage import StorageManager

stockage = StorageManager()

def collecter_cpu():
    """Sonde CPU via psutil (ton cpu.py)"""
    cpu = psutil.cpu_percent(interval=1)
    storage.save(sonde="cpu", valeur=cpu, unite="%")
    print(f"CPU : {cpu}%")

def collecter_ram():
    """Sonde RAM via ton ram.sh"""
    result = subprocess.run(
        ["bash", "ram.sh"],
        capture_output=True, text=True
    )
    # Extraire le pourcentage depuis la sortie "Utilisation de la RAM : 42.50%"
    ligne = result.stdout.strip()
    try:
        pourcentage = float(ligne.split(":")[1].strip().replace("%", ""))
        storage.save(sonde="ram", valeur=pourcentage, unite="%")
        print(f"RAM : {pourcentage}%")
    except Exception as e:
        print(f"Erreur RAM : {e}")

def collecter_disque():
    """Sonde disque via ton disque.sh"""
    result = subprocess.run(
        ["bash", "disque.sh"],
        capture_output=True, text=True
    )
    print(result.stdout.strip())
    # Extraire "utilisé : 12G,45%"
    for ligne in result.stdout.splitlines():
        if "utilisé" in ligne.lower():
            try:
                # Format : "Espace disque utilisé : 12G,45%"
                partie = ligne.split(":")[1].strip()
                # Garder le pourcentage
                pct = partie.split(",")[-1].replace("%", "").strip()
                storage.save(sonde="disque", valeur=float(pct), unite="%",)
            except Exception as e:
                print(f"Erreur disque : {e}")

if __name__ == "__main__":
    print("=== Collecte des métriques ===")
    collecter_cpu()
    collecter_ram()
    collecter_disque()
    print("\n=== Dernières valeurs stockées ===")
    for row in storage.get_latest():
        sonde, valeur, unite, ts = row
        print(f"[{ts}] {sonde:8s} → {valeur:.1f}{unite}")
