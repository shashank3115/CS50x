from cs50 import SQL
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
db = SQL("sqlite:///birthdays.db")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        if not name or not month or not day:
            return redirect("/")

        try:
            month = int(month)
            day = int(day)
        except ValueError:
            return redirect("/")

        if month < 1 or month > 12 or day < 1 or day > 31:
            return redirect("/")

        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)
        return redirect("/")
    else:
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays=birthdays)


# DELETE 
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    db.execute("DELETE FROM birthdays WHERE id = ?", id)
    return redirect("/")


# EDIT
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        if not name or not month or not day:
            return redirect("/")

        try:
            month = int(month)
            day = int(day)
        except ValueError:
            return redirect("/")

        if month < 1 or month > 12 or day < 1 or day > 31:
            return redirect("/")

        db.execute("UPDATE birthdays SET name = ?, month = ?, day = ? WHERE id = ?", name, month, day, id)
        return redirect("/")
    else:
        birthday = db.execute("SELECT * FROM birthdays WHERE id = ?", id)[0]
        return render_template("edit.html", birthday=birthday)
