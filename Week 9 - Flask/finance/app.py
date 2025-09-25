import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


def render_with_theme(template, **kwargs):
    theme = "light"
    if "user_id" in session:
        user = db.execute("SELECT theme FROM users WHERE id = ?", session["user_id"])
        if user:
            theme = user[0]["theme"]
    return render_template(template, theme=theme, **kwargs)


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
    user_id = session["user_id"]

    # Group user’s transactions by symbol to get total shares owned
    rows = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol",
        user_id
    )

    holdings = []
    total_value = 0

    for row in rows:
        if row["total_shares"] > 0:  # only show positive shares
            stock = lookup(row["symbol"])
            price = stock["price"]
            shares = row["total_shares"]
            total = price * shares
            total_value += total
            holdings.append({
                "symbol": row["symbol"],
                "name": stock["name"],
                "shares": shares,
                "price": price,
                "total": total
            })

    # Get user cash
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
    total_value += cash

    return render_with_theme("index.html", holdings=holdings, cash=cash, total_value=total_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate input
        if not symbol:
            return apology("must provide symbol")
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("shares must be a positive integer")

        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol")

        shares = int(shares)
        price = stock["price"]
        cost = price * shares

        # Query user cash
        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        if cost > cash:
            return apology("can't afford")

        # Deduct cash
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, user_id)

        # Record transaction
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            user_id, stock["symbol"], shares, price
        )

        flash("Bought!")
        return redirect("/")

    else:
        return render_with_theme("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]

    transactions = db.execute(
        "SELECT symbol, shares, price, transacted FROM transactions WHERE user_id = ? ORDER BY transacted DESC",
        user_id
    )

    return render_with_theme("history.html", transactions=transactions)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_with_theme("login.html")


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
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol")

        stock = lookup(symbol)

        if stock is None:
            return apology("invalid symbol")

        return render_with_theme("quoted.html", name=stock["name"], symbol=stock["symbol"], price=stock["price"])

    else:
        return render_with_theme("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate input
        if not username:
            return apology("must provide username", 400)
        elif not password:
            return apology("must provide password", 400)
        elif password != confirmation:
            return apology("passwords do not match", 400)

        hash_pw = generate_password_hash(password)

        try:
            new_user = db.execute(
                "INSERT INTO users (username, hash) VALUES(?, ?)", username, hash_pw
            )
        except Exception:
            return apology("username already taken", 400)

        session["user_id"] = new_user

        # Redirect to home
        return redirect("/")

    else:
        return render_with_theme("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate inputs
        if not symbol:
            return apology("must provide symbol")
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("shares must be a positive integer")

        shares = int(shares)

        # Check how many shares the user owns
        owned = db.execute(
            "SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol",
            user_id, symbol
        )

        if len(owned) != 1 or owned[0]["total_shares"] < shares:
            return apology("too many shares")

        # Get stock price
        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol")

        price = stock["price"]
        revenue = price * shares

        # Update user’s cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", revenue, user_id)

        # Record the sale (insert negative shares)
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            user_id, symbol, -shares, price
        )

        flash("Sold!")
        return redirect("/")

    else:
        # Get list of symbols user currently owns
        rows = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
            user_id
        )
        symbols = [row["symbol"] for row in rows]
        return render_with_theme("sell.html", symbols=symbols)

# new feature


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    if request.method == "POST":
        try:
            amount = float(request.form.get("amount"))
        except:
            return apology("must provide valid amount", 400)

        if amount <= 0:
            return apology("amount must be positive", 400)

        # Update user's cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", amount, session["user_id"])
        flash("Cash added successfully!")
        return redirect("/")

    return render_with_theme("addcash.html")


# new feature3
@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        new_username = request.form.get("username")

        if not new_username:
            return apology("must provide username", 400)

        exists = db.execute("SELECT * FROM users WHERE username = ?", new_username)
        if exists:
            return apology("username already taken", 400)

        db.execute("UPDATE users SET username = ? WHERE id = ?", new_username, session["user_id"])
        flash("Username updated successfully!")
        return redirect("/")

    return render_with_theme("settings.html")


@app.route("/toggle_theme")
@login_required
def toggle_theme():
    user = db.execute("SELECT theme FROM users WHERE id = ?", session["user_id"])
    current_theme = user[0]["theme"] if user else "light"

    # Flip between light/dark
    new_theme = "dark" if current_theme == "light" else "light"

    db.execute("UPDATE users SET theme = ? WHERE id = ?", new_theme, session["user_id"])

    return redirect("/")
