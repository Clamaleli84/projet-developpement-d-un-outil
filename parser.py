import urllib.request

def get_latest_cert_alert():
    url = "https://www.cert.ssi.gouv.fr/"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    with urllib.request.urlopen(req) as response:
        html = response.read().decode("utf-8")

    for ligne in html.split("\n"):
        if "CERTFR" in ligne and "href" in ligne:
            # Extraire l'URL
            debut_url = ligne.find('href="') + 6
            fin_url = ligne.find('"', debut_url)
            alerte_url = "https://www.cert.ssi.gouv.fr" + ligne[debut_url:fin_url]
            
            # Extraire le titre → chercher le 2ème >
            # Chercher le 3ème >
            premier = ligne.find(">")
            deuxieme = ligne.find(">", premier + 1)
            troisieme = ligne.find(">", deuxieme + 1)
            fin_titre = ligne.find("</a>")
            titre = ligne[troisieme + 1:fin_titre].strip()
            
            print(f"URL : {alerte_url}")
            print(f"Titre : '{titre}'")
            return

get_latest_cert_alert()
