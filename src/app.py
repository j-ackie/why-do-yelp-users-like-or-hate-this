from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        search = request.form.get("test")
        return render_template("test.html", what=search)
