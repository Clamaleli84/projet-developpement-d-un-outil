import urllib.request

url = "https://www.cert.ssi.gouv.fr/"

req = urllib.request.Request(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req) as response:
    html = response.read().decode("utf-8")

print(html[:500])
