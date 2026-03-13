import urllib.request

url = "https://www.cert.ssi.gouv.fr/"

req = urllib.request.Request(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req) as response:
    html = response.read().decode("utf-8")

# Afficher seulement les lignes avec "alerte"
for ligne in html.split("\n"):
    if "alerte" in ligne.lower():
        print(ligne.strip())
