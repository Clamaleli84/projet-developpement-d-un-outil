import urllib.request

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
