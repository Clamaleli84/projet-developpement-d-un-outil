import json
import os
import smtplib
from email.message import EmailMessage
from storage import StorageManager

config_dir = "config"
config_file = os.path.join(config_dir, "crisis_config.json")
template_file = os.path.join(config_dir, "template_mail.html")
data_file = "derniere_alerte.json"

config_defaut = {
    "cpu_threshold": 0.0,
    "ram_threshold": 85.0,
    "disk_threshold": 90.0,
    "admin_email": "matteo.jaubert@alumni.univ-avignon.fr",
    "smtp_server": "pedago.univ-avignon.fr",
    "smtp_port": 465,
    "smtp_user": "leo.jaubert@alumni.univ-avignon.fr",
    "smtp_pass": "mdp"
}

template_defaut = """
<html>
<body style="font-family: Arial, sans-serif;">
    <h2 style="color: red;">SITUATION DE CRISE ATTEINTE: </h2>
    <p>Le module de crise a détecté un dépassement :</p>
    <ul>
        <li><strong>CPU :</strong> {cpu}%</li>
        <li><strong>RAM :</strong> {ram}%</li>
        <li><strong>Disque :</strong> {disk}%</li>
    </ul>
</body>
</html>
"""

def init_files():
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    if not os.path.exists(config_file):
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_defaut, f, indent=4)
    if not os.path.exists(template_file):
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(template_defaut)

def get_data_from_db():
    storage = StorageManager()
    rows = storage.get_latest()
    
    stats = {"cpu": None, "ram": None, "disk": None}
    
    for row in rows:
        id, sonde, valeur, unite, timestamp = row
        if sonde == "cpu" and stats["cpu"] is None:
            stats["cpu"] = valeur
        elif sonde == "ram" and stats["ram"] is None:
            stats["ram"] = valeur
        elif sonde == "disque" and stats["disk"] is None:
            stats["disk"] = valeur
    
    if None in stats.values():
        return None
    return stats

def send_mail(stats):
    with open(config_file, 'r') as f:
        config = json.load(f)
    with open(template_file, 'r') as f:
        content = f.read().format(**stats)

    msg = EmailMessage()
    msg.set_content(content, subtype='html')
    msg['Subject'] = "[AUTOMATIQUE] Crise : Alerte Ressources Serveur"
    msg['From'] = config["smtp_user"]
    msg['To'] = config["admin_email"]

    try:
        # Pour le port 465, on utilise SMTP_SSL directement
        with smtplib.SMTP_SSL(config["smtp_server"], config["smtp_port"]) as server:
            server.login(config["smtp_user"], config["smtp_pass"])
            server.send_message(msg)
        print("Mail envoyé avec succès via le serveur de l'université.")
    except Exception as e:
        print(f"Erreur d'envoi SMTP : {e}")

init_files()
stats = get_data_from_db()

if stats:
    with open(config_file, 'r') as f:
        config = json.load(f)

    is_crisis = (stats["cpu"] >= config["cpu_threshold"] or 
                 stats["ram"] >= config["ram_threshold"] or 
                 stats["disk"] >= config["disk_threshold"])

    if is_crisis:
        print(f"ALERTE CRISE ! CPU:{stats['cpu']} RAM:{stats['ram']} DISK:{stats['disk']}")
        send_mail(stats)
    else:
        print(f"OK. CPU:{stats['cpu']} RAM:{stats['ram']} DISK:{stats['disk']}")
else:
    print("Erreur : Impossible de lire les données DB.")
