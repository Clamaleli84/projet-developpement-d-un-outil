from flask import Flask, render_template
import os
import shutil
import subprocess

app = Flask(__name__)

def rafraichir_tout():
    """Lance la collecte, la génération et déplace les images."""
    try:
        # 1. Lancer la collecte du parc (parc.py)
        subprocess.run(["python3", "parc.py"], check=True)
        # 2. Lancer la génération des graphiques (graphique.py)
        subprocess.run(["python3", "graphique.py"], check=True)
        
        # 3. Déplacer les PNG vers static/
        if not os.path.exists('static'):
            os.makedirs('static')
        for f in os.listdir('.'):
            if f.endswith(".png"):
                shutil.move(f, os.path.join('static', f))
    except Exception as e:
        print(f"Erreur lors du rafraîchissement : {e}")

@app.route("/")
def index():
    rafraichir_tout()
    machines = ["vm_locale", "ordi_local"]
    metriques = ["cpu", "ram", "disque"]
    return render_template("index.html", machines=machines, metriques=metriques)

if __name__ == "__main__":
    # On utilise le port 5000 (pense à la redirection de port VirtualBox)
    app.run(host="0.0.0.0", port=5000, debug=True)
