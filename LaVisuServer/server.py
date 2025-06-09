
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
import os, json, uuid
requests

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("FLASK_SECRET", "change_this_secret")
CORS(app)

git add requirements.txt
git commit -m "Ajout du fichier requirements.txt"
git push

KEYS_FILE = "keys.json"
ADMIN_PASS = os.getenv("ADMIN_PASS", "monmotdepasse")

def load_keys():
    if os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_keys(data):
    with open(KEYS_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/validate", methods=["POST"])
def validate_key():
    data = request.get_json(force=True)
    key = data.get("key", "")
    keys = load_keys()
    valid = keys.get(key, False)
    return jsonify({"valid": valid})

@app.route("/login", methods=["GET","POST"])
def login():
    if session.get("logged"):
        return redirect(url_for("admin"))
    err = None
    if request.method=="POST":
        if request.form.get("password") == ADMIN_PASS:
            session["logged"] = True
            return redirect(url_for("admin"))
        err = "Mot de passe incorrect"
    return render_template("login.html", error=err)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/admin", methods=["GET","POST"])
def admin():
    if not session.get("logged"):
        return redirect(url_for("login"))
    keys = load_keys()
    if request.method == "POST":
        action = request.form.get("action")
        if action == "generate":
            newkey = uuid.uuid4().hex[:16]
            keys[newkey] = True
        elif action=="toggle":
            k = request.form.get("key")
            if k in keys:
                keys[k] = not keys[k]
        save_keys(keys)
    return render_template("admin.html", keys=keys)
    if __name__ == '__main__':     app.run()
