import urllib.request

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
            ligne_suivante = lignes[i + 1].strip()
            print(f"LIGNE SUIVANTE : '{ligne_suivante}'")
            titre = ligne_suivante.replace("</a>", "").strip()
            print(f"URL   : {alerte_url}")
            print(f"Titre : {titre}")
            return

get_latest_cert_alert()
