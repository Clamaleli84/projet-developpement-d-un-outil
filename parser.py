import urllib.request

def get_latest_cert_alert():
    url = "https://www.cert.ssi.gouv.fr/"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    with urllib.request.urlopen(req) as response:
        html = response.read().decode("utf-8")

    lignes = html.split("\n")
    for i, ligne in enumerate(lignes):
        if "CERTFR" in ligne and "href" in ligne:
            print(f"ligne {i}   : '{ligne.strip()}'")
            print(f"ligne {i+1} : '{lignes[i+1].strip()}'")
            print(f"ligne {i+2} : '{lignes[i+2].strip()}'")
            print(f"ligne {i+3} : '{lignes[i+3].strip()}'")
            print(f"ligne {i+4} : '{lignes[i+4].strip()}'")
            return

get_latest_cert_alert()
