from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    # Liste des machines correspondant à tes noms de fichiers
    liste_machines = ["vm_locale", "ordi_local"]
    return render_template("index.html", machines=liste_machines)

if __name__ == "__main__":
    # debug=True permet de voir les modifs sans relancer le script
    app.run(host="0.0.0.0", port=5000, debug=True)
