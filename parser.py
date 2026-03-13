import requests
import xml.etree.ElementTree as ET
import json
import os
import subprocess

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

        # Comparaison du titre
        if ancienne_alerte.get("titre") == titre:
            print("Aucune nouvelle alerte.")
            exit()

    # Enregistrer la nouvelle alerte
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(nouvelle_alerte, f, indent=4, ensure_ascii=False)

    print(f"Nouvelle alerte enregistrée : '{titre[:30]}...'")

    # Envoi au moteur de stockage
    subprocess.run([
        "./stockage.sh",
        "CERT",
        titre,
        date_pub,
        link,
        etat
    ])import requests
import xml.etree.ElementTree as ET
import json
import os
import subprocess

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

        # Comparaison du titre
        if ancienne_alerte.get("titre") == titre:
            print("Aucune nouvelle alerte.")
            exit()

    # Enregistrer la nouvelle alerte
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(nouvelle_alerte, f, indent=4, ensure_ascii=False)

    print(f"Nouvelle alerte enregistrée : '{titre[:30]}...'")

    # Envoi au moteur de stockage
    subprocess.run([
        "./stockage.sh",
        "CERT",
        titre,
        date_pub,
        link,
        etat
    ])import urllib.request

def get_latest_cert_alert():
    url = "https://www.cert.ssi.gouv.fr/"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    with urllib.request.urlopen(req) as response:
        html = response.read().decode("utf-8")

    lignes = html.split("\n")
    for i, ligne in enumerate(lignes):
        if "CERTFR" in ligne and "href" in ligne:
            debut_url = ligne.find('href="') + 6
            fin_url = ligne.find('"', debut_url)
            alerte_url = "https://www.cert.ssi.gouv.fr" + ligne[debut_url:fin_url]

            for j in range(i, i + 10):
                if "item-title" in lignes[j]:
                    ligne_titre = lignes[j + 1].strip()
                    debut = ligne_titre.rfind(">") + 1
                    fin = ligne_titre.find("</a>")
                    titre = ligne_titre[debut:fin].strip()
                    print(f"URL   : {alerte_url}")
                    print(f"Titre : {titre}")
                    return

get_latest_cert_alert()
