from flask import Flask, render_template
import os
import shutil
import subprocess

app = Flask(__name__)

def rafraichir_tout():
    # On supprime les anciens PNG dans static avant de mettre les nouveaux
    for f in os.listdir('static'):
        if f.endswith(".png"):
            os.remove(os.path.join('static', f))
            
    # On lance les scripts
    subprocess.run(["python3", "parc.py"])
    subprocess.run(["python3", "graphique.py"])
    
    # On déplace les nouveaux
    for f in os.listdir('.'):
        if f.endswith(".png"):
            # On utilise shutil.move pour écraser proprement
            shutil.move(f, os.path.join('static', f))

@app.route("/")
def index():
    rafraichir_tout()
    machines = ["vm_locale", "ordi_local"]
    metriques = ["cpu", "ram", "disque"]
    return render_template("index.html", machines=machines, metriques=metriques)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
