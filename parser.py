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
