from flask import Flask, render_template, request
from review import load_freqs


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        search = request.form.get("test")
        result = load_freqs(search)
        business_name = result[0]
        freqs = result[1]
        if len(freqs["positive"]) < 10:
            pos_freqs = freqs["positive"][0:len(freqs["positive"])]
        else:
            pos_freqs = freqs["positive"][0:10]

        if len(freqs["negative"]) < 10:
            neg_freqs = freqs["negative"][0:len(freqs["negative"])]
        else:
            neg_freqs = freqs["negative"][0:10]

        return render_template("results.html", business_name=business_name, pos_freqs=pos_freqs, neg_freqs=neg_freqs)
