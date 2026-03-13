import urllib.request

def get_latest_cert_alert():
    url = "https://www.cert.ssi.gouv.fr/"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    with urllib.request.urlopen(req) as response:
        html = response.read().decode("utf-8")

    for ligne in html.split("\n"):
        # Chercher les lignes avec une vraie alerte CERTFR
        if "CERTFR" in ligne and "href" in ligne:
            # Extraire l'URL
            debut_url = ligne.find('href="') + 6
            fin_url = ligne.find('"', debut_url)
            alerte_url = "https://www.cert.ssi.gouv.fr" + ligne[debut_url:fin_url]
            
            # Extraire le titre
            debut_titre = ligne.find(">", ligne.find('/>')) + 1
            fin_titre = ligne.find("</a>")
            titre = ligne[debut_titre:fin_titre].strip()
            
            if titre:  # si on a bien un titre
                return {"titre": titre, "url": alerte_url}

    return None

# Test
alerte = get_latest_cert_alert()
if alerte:
    print(f"Titre : {alerte['titre']}")
    print(f"URL   : {alerte['url']}")
