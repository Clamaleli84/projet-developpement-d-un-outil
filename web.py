from flask import Flask, render_template
import graphique  # On importe ton script graphique.py
import os
import shutil

app = Flask(__name__)

def rafraichir_graphiques():
    # 1. Lancer la génération des graphiques
    # Comme ton graphique.py exécute déjà la boucle à la fin du fichier, 
    # l'importer va lancer la génération automatiquement.
    
    # 2. Déplacer les fichiers vers le dossier static
    if not os.path.exists('static'):
        os.makedirs('static')
    
    for file in os.listdir('.'):
        if file.endswith(".png"):
            # On déplace (ou copie) le fichier dans static/
            shutil.copy(file, os.path.join('static', file))

@app.route("/")
def index():
    # On met à jour les images avant de charger la page
    rafraichir_graphiques()
    
    liste_machines = ["vm_locale", "ordi_local"]
    # On ajoute "disque" à la liste des types pour le HTML
    types_metriques = ["cpu", "ram", "disque"] 
    
    return render_template("index.html", machines=liste_machines, metriques=types_metriques)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
