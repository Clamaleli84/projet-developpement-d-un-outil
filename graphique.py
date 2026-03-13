import pygal
from storage import StorageManager

def generer_graphique(sonde):
    storage = StorageManager()
    rows = storage.get_history(sonde)

    if not rows:
        print(f"Aucune donnée pour {sonde}")
        return

    valeurs = [row[0] for row in rows]
    timestamps = [row[1] for row in rows]

    graphique = pygal.Line()
    graphique.title = f"Historique {sonde}"
    graphique.x_labels = timestamps
    graphique.add(sonde, valeurs)
    graphique.render_to_file(f"{sonde}.svg")
    print(f"Graphique généré : {sonde}.svg")

# Générer pour chaque sonde
generer_graphique("cpu")
generer_graphique("ram")
generer_graphique("disque")
