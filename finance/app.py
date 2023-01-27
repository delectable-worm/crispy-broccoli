import os
#pk_39c515c6664f4bb19bcf9079096bce99

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API symbol is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    owned = db.execute("SELECT key, shares FROM owned WHERE user_id=?", session["user_id"]);
    sum = 0
    for item in owned:
        getsymbol=lookup(item["key"])
        item["price"] = usd(getsymbol["price"])
        sum+=getsymbol["price"]*item["shares"]
        item["value"] = usd(getsymbol["price"]*item["shares"])
        item["name"]=getsymbol["name"]
    available=db.execute("SELECT cash FROM users where id=?", session["user_id"])[0]["cash"]
    total=usd(available+sum)
    available=usd(available)
    return render_template("index.html", id=session["user_id"], owned=owned, available=available, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        #get values
        try:
            shares = float(request.form.get("shares"))
        except:
            return apology("not number")
        symbol = request.form.get("symbol")
        if not symbol or not shares:
            return apology("Missing...")

        #check symbol
        getsymbol=lookup(symbol)
        if not getsymbol:
                return apology("invalid symbol")
        #check money
        if shares <= 0 or not shares%1 == 0:
            return apology("invalid share count")

        row = db.execute("SELECT cash FROM users where id=?", session["user_id"])

        available = float(row[0]["cash"])
        if shares * getsymbol["price"] > available:
            return apology("can't afford", 400)

        #change values
        time = datetime.now().strftime("%d/%m/%y, %H:%M:%S")
        available = available - shares * getsymbol["price"]
        db.execute("INSERT INTO trades(user_id, key,shares, price, time) VALUES(?,?,?,?,?)", session["user_id"], symbol, shares, getsymbol["price"], time) #list of transactions
        db.execute("UPDATE users SET cash = ? WHERE id = ?", available, session["user_id"])

        #owned table for easy manipulation
        checksymbolExists=db.execute("SELECT shares FROM owned WHERE key=?",symbol)
        if len(checksymbolExists) == 1:
            sharesOwned=checksymbolExists[0]["shares"]
            db.execute("UPDATE owned SET shares =? where user_id=? AND key=?", sharesOwned+shares, session["user_id"], symbol)
        else:
            db.execute("INSERT INTO owned (user_id, key, shares) VALUES (?,?,?)", session["user_id"], symbol, shares)

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    trades = db.execute("select * from trades where user_id=?", session["user_id"])
    for trade in trades:
        trade["current"] = lookup(trade["key"])["price"]
    return render_template("history.html", trades=trades)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id .... user id used for seession and things... access db..?
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "GET":
        return render_template("quote.html")

    else:
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("no symbol :(")

        getsymbol = lookup(symbol)
        if not getsymbol:
            return apology("no such symbol", 400)

        name=getsymbol["name"]
        price=usd(getsymbol["price"])
        return render_template("quoted.html", name=name, price=price, symbol=symbol)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    #inputs exist?
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("username invalid", 400)
        elif not request.form.get("password") or not request.form.get("confirmation") or not request.form.get("confirmation") == request.form.get("password"):
            return apology("password invalid", 400)


        username = request.form.get("username")
        password = request.form.get("password")
        used = db.execute("SELECT username FROM users WHERE username=?", username)

        #unique username?
        if len(used) != 0:
            return apology("repeated username", 400)

        #insert!
        db.execute("INSERT INTO users(username, hash) VALUES(?,?)",username, generate_password_hash(password,method='pbkdf2:sha256',salt_length=8))
        return redirect("/login")

    else:
        return render_template("register.html") #just render template vs do stuff w/ form (don't do stuff w/ empty form)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        time = datetime.now().strftime("%d/%m/%y, %H:%M:%S")
        #get values
        try:
            shares = float(request.form.get("shares"))
        except:
            return apology("invalid")
        symbol = request.form.get("symbol")
        if not symbol or not shares:
            return apology("Missing...")
      #validate input
        getsymbol = lookup(symbol)
        if not getsymbol or shares<1:
            return apology("Inavlid inpit")
        ownedShares = db.execute("SELECT shares FROM owned WHERE key=?", symbol)[0]["shares"]
        if ownedShares < shares:
            return apology("invalid input")
        available=db.execute("SELECT cash FROM users where id=?", session["user_id"])[0]["cash"]
        db.execute("INSERT INTO trades(user_id, key, shares, price, time) VALUES (?,?,?,?,?)", session["user_id"], symbol, shares, getsymbol["price"], time)
        db.execute("UPDATE owned SET shares=? where user_id=? and key=?", ownedShares-shares, session["user_id"], symbol)
        db.execute("UPDATE users SET cash=? where id=?", available+(getsymbol["price"]*shares), session["user_id"])
        return redirect("/")
    else:
        list=db.execute("SELECT key FROM owned WHERE user_id=?", session["user_id"])
        return render_template("sell.html", list=list)