from flask import Flask, render_template, request, redirect, url_for
from review import load_freqs


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        return redirect(url_for("results", search_term=request.form.get("search_term")))


@app.route("/<search_term>")
def results(search_term):
    result = load_freqs(search_term)
    business_name = result[0]
    business_url = result[1]
    freqs = result[2]
    if len(freqs["positive"]) < 10:
        pos_freqs = freqs["positive"][0:len(freqs["positive"])]
    else:
        pos_freqs = freqs["positive"][0:10]

    if len(freqs["negative"]) < 10:
        neg_freqs = freqs["negative"][0:len(freqs["negative"])]
    else:
        neg_freqs = freqs["negative"][0:10]
    return render_template("results.html", business_name=business_name, business_url=business_url,
                           pos_freqs=pos_freqs, neg_freqs=neg_freqs)

