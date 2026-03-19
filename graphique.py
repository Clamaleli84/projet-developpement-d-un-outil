import pygal
from storage import StorageManager
import cairosvg

MACHINES = ["vm_locale", "ordi_local"]

def generer_graphique(sonde, nom_machine):
    storage = StorageManager(db_path=f"metrics_{nom_machine}.db")
    rows = storage.get_history(sonde)
    if not rows:
        print(f"Aucune donnée pour {sonde} sur {nom_machine}")
        return
    valeurs = [row[0] for row in rows]
    timestamps = [row[1] for row in rows]
    graphique = pygal.Line()
    graphique.title = f"Historique {sonde} - {nom_machine}"
    graphique.x_labels = timestamps
    graphique.add(sonde, valeurs)
    graphique.render_to_file(f"{sonde}_{nom_machine}.svg")
    cairosvg.svg2png(url=f"{sonde}_{nom_machine}.svg", write_to=f"{sonde}_{nom_machine}.png")
    print(f"Graphique généré : {sonde}_{nom_machine}.png")

for machine in MACHINES:
    generer_graphique("cpu", machine)
    generer_graphique("ram", machine)
    generer_graphique("disque", machine)
