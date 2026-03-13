import urllib.request

def get_latest_cert_alert():
    url = "https://www.cert.ssi.gouv.fr/"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    with urllib.request.urlopen(req) as response:
        html = response.read().decode("utf-8")

    lignes = html.split("\n")
    for i, ligne in enumerate(lignes):
        if "CERTFR" in ligne and "href" in ligne:
            # Extraire l'URL
            debut_url = ligne.find('href="') + 6
            fin_url = ligne.find('"', debut_url)
            alerte_url = "https://www.cert.ssi.gouv.fr" + ligne[debut_url:fin_url]

            # Le titre est sur la ligne suivante
            ligne_suivante = lignes[i + 1].strip()
            titre = ligne_suivante.replace("</a>", "").strip()

            print(f"URL   : {alerte_url}")
            print(f"Titre : {titre}")
            return

get_latest_cert_alert()import urllib.request

def get_latest_cert_alert():
    url = "https://www.cert.ssi.gouv.fr/"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    with urllib.request.urlopen(req) as response:
        html = response.read().decode("utf-8")

    for ligne in html.split("\n"):
        if "CERTFR" in ligne and "href" in ligne:
            print(f"LIGNE BRUTE : '{ligne}'")
            return

get_latest_cert_alert()
