from flask import Flask, render_template
app  = Flask(__name__)
# Replace the existing home function with the one below
@app.route("/")
def index():
    return render_template("index.html")