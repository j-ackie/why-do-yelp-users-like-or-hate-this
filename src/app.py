from flask import Flask, render_template, request
from review import load_freqs


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        search = request.form.get("test")
        freqs = load_freqs(search)
        return render_template("test.html", what=freqs["positive"][0])
