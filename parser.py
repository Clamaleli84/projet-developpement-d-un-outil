import requests
import xml.etree.ElementTree as ET
import json
import os
from stockage import StorageManager

url = "https://www.cert.ssi.gouv.fr/feed/"
json_file = "derniere_alerte.json"

response = requests.get(url, timeout=10)
response.raise_for_status()
root = ET.fromstring(response.content)
item = root.find('.//item')

if item is not None:
    titre = item.find('title').text
    date_pub = item.find('pubDate').text
    link = item.find('link').text
    
    etat = "Clôturé" if "clôture" in titre.lower() else "Actif"
    
    nouvelle_alerte = {
        "titre": titre,
        "date": date_pub,
        "url": link,
        "etat": etat
    }

    # Vérifier si une alerte existe déjà
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            ancienne_alerte = json.load(f)
        if ancienne_alerte.get("titre") == titre:
            print("Aucune nouvelle alerte.")
            exit()

    # Enregistrer la nouvelle alerte en JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(nouvelle_alerte, f, indent=4, ensure_ascii=False)

    print(f"Nouvelle alerte enregistrée : '{titre[:30]}...'")

    # Envoi au moteur de stockage
    storage = StorageManager()
    storage.save("CERT", 0, titre)
