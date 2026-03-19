import pygal
from storage import StorageManager
import cairosvg

MACHINES = ["vm_locale", "ordi_local"]

def generer_graphique(sonde, nom_machine):
    # CRITIQUE : Vérifie bien que nom_machine est utilisé ici
    storage = StorageManager(db_path=f"metrics_{nom_machine}.db")
    rows = storage.get_history(sonde)
    
    if not rows:
        return

    valeurs = [row[0] for row in rows]
    timestamps = [row[1] for row in rows]

    graphique = pygal.Line()
    graphique.title = f"Historique {sonde} - {nom_machine}"
    graphique.x_labels = timestamps
    graphique.add(sonde, valeurs)

    # Sauvegarde avec le nom complet pour ne pas écraser l'autre machine
    nom_fich = f"{sonde}_{nom_machine}"
    graphique.render_to_file(f"{nom_fich}.svg")
    cairosvg.svg2png(url=f"{nom_fich}.svg", write_to=f"{nom_fich}.png")

for machine in MACHINES:
    generer_graphique("cpu", machine)
    generer_graphique("ram", machine)
    generer_graphique("disque", machine)
