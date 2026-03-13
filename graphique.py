import pygal

# Créer un graphique en ligne
graphique = pygal.Line()
graphique.title = "CPU"
graphique.add("CPU %", [42.5, 43.0, 41.2, 45.0])  # les valeurs
graphique.render_to_file("cpu.svg")  # sauvegarder en fichier
print("Graphique généré : cpu.svg")
