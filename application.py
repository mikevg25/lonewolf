#Mike van Gils - 12363197

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp


# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///lonewolf.db")

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/notify", methods=["GET", "POST"])
def notify():
    if request.method == "POST":
        # pomp het in de database
        db.execute("INSERT INTO aanmeldingen(name, email) VALUES(:name, :email)", name=request.form.get("name"), email=request.form.get("email"))
        return render_template("thanks.html")

    else:
        return render_template("notify.html")