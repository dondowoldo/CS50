import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

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

# Make sure API key is set
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
    transactions = db.execute(
        "SELECT symbol, name, SUM(quantity), buy_price FROM transactions WHERE user_id = ? GROUP BY symbol", session["user_id"])
    wallet = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    for row in transactions:
        current_price = 0
        current_price = lookup(row["symbol"])["price"]

        # Save the latest prices into the database to the prices table
        symbol_check = db.execute("SELECT symbol FROM prices WHERE symbol = ?", row["symbol"])
        if len(symbol_check) != 1:
            db.execute("INSERT INTO prices(symbol, price) VALUES (?, ?)", row["symbol"], current_price)
        else:
            db.execute("UPDATE prices SET price = ? WHERE symbol = ?", current_price, row["symbol"])

    # Convert list of dictionaries into a dictionary with symbol as key to be able to iterate over in index
    prices = db.execute("SELECT symbol, price FROM prices")
    prices_dict = {stock['symbol']: stock for stock in prices}

    # Iterating through symbols of shares that user has, multiplying its current value with amount of these shares and adding together with total cash
    overall_value = 0
    for shares_value in transactions:
        quant = db.execute("SELECT SUM(quantity) FROM transactions WHERE symbol = ? AND user_id = ?",
                           shares_value["symbol"], session["user_id"])
        overall_value += (lookup(shares_value["symbol"])["price"]) * int(quant[0]["SUM(quantity)"])

    grand_total = overall_value + wallet

    return render_template("index.html", transactions=transactions, wallet=wallet, price=prices_dict, total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        try:
            int(request.form.get("shares"))
        except:
            return apology("must provide a whole number", 400)
        if not request.form.get("symbol"):
            return apology("must provide a stock symbol", 400)

        elif not request.form.get("shares"):
            return apology("must provide an amount of shares", 400)

        elif int(request.form.get("shares")) < 0:
            return apology("must provide a positive number of shares", 400)

        elif lookup(request.form.get("symbol")) is None:
            return apology("Invalid stock symbol", 400)

        else:
            price = float(lookup(request.form.get("symbol"))["price"])
            quantity = int(request.form.get("shares"))
            credit = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            if (price * quantity) >= credit[0]["cash"]:
                return apology("not enough funds", 403)
            else:
                new_balance = credit[0]["cash"] - (price * quantity)
                db.execute("UPDATE users SET cash = ? WHERE id = ?", new_balance, session["user_id"])

                db.execute("INSERT INTO transactions (symbol, buy_price, user_id, quantity, name, type) VALUES (?, ?, ?, ?, ?, ?)",
                           request.form.get("symbol"), lookup(request.form.get("symbol"))["price"],
                           session["user_id"], int(request.form.get("shares")), lookup(request.form.get("symbol"))["name"], "buy")

                flash("Bought!")
                return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT symbol, quantity, buy_price, sell_price, type, date, time FROM transactions WHERE user_id = ?", session["user_id"])
    return render_template("history.html", transactions=transactions)


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

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if lookup(request.form.get("symbol")) is None:
            return apology("Invalid stock symbol")
        else:
            stock = lookup(request.form.get("symbol"))
            return render_template("quoted.html", stock=stock)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 0:
            return apology("This username already exists. Please choose another one or log-in.", 400)

        # Check if password and password confirmation match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match.", 400)

        # Hash the passoword and insert the user into database

        hashpass = generate_password_hash(request.form.get("password"))
        username = request.form.get("username")
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashpass)

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    held_shares = db.execute(
        "SELECT symbol, SUM(quantity) AS amount FROM transactions WHERE user_id = ? GROUP BY symbol", session["user_id"])
    held_shares_dict = {stock['symbol']: stock for stock in held_shares}

    if request.method == "POST":
        if not request.form.get("shares"):
            return apology("Input amount of shares", 400)
        elif not request.form.get("symbol"):
            return apology("Select a symbol", 403)
        elif int(request.form.get("shares")) > held_shares_dict[request.form.get("symbol")]["amount"]:
            return apology("Not enough shares")
        else:
            price = float(lookup(request.form.get("symbol"))["price"])
            quantity = int(request.form.get("shares"))
            credit = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            new_balance = credit[0]["cash"] + (price * quantity)

            db.execute("INSERT INTO transactions (symbol, sell_price, user_id, quantity, name, type) VALUES (?, ?, ?, ?, ?, ?)",
                       request.form.get("symbol"), price, session["user_id"], (quantity * -1), lookup(request.form.get("symbol"))["name"], "sell")

            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_balance, session["user_id"])

            flash("Sold!")

            return redirect("/")

    else:
        return render_template("sell.html", symbols=held_shares)


@app.route("/pass", methods=["GET", "POST"])
@login_required
def passchange():
    """ Change a password """
    # Ensure all fields submitted
    if request.method == "POST":
        if not request.form.get("password_old"):
            return apology("must enter current password")
        elif not request.form.get("password_new"):
            return apology("must enter new password")
        elif not request.form.get("confirmation"):
            return apology("must enter new password confirmation")

        # Make sure current password matches // new password matches confirmation and update if so
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password_old")):
            return apology("invalid password", 403)
        elif request.form.get("password_new") != request.form.get("confirmation"):
            return apology("Confirmation doesn't match with the new password")
        else:
            db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(
                request.form.get("password_new")), session["user_id"])
            session.clear()
            return redirect("/")
    else:
        return render_template("pass.html")