from flask import Flask, redirect, render_template, request, session
from database import DatabaseOperations
from repo.transaction_repo import TransactionRepo
from repo.user_repo import UserRepo


app = Flask(__name__)
app.secret_key = "97783c40901c1d89a451930ae8be5766950cd90f063f24035305ac6ddf64bced"
DatabaseOperations.init_db()


@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = UserRepo.create_user(email=request.form["email"], phone=request.form["phone"])
        if user_id is not None:
            session["user_id"] = user_id
            return redirect("/data")
        else:
            return redirect("/login")

    return render_template("login.html")
   

@app.route("/data", methods = ["GET"])
def dataPage():
    if session.get("user_id") is None:
            return redirect("/login")
    transactions = TransactionRepo.get_transactions(user_id= session.get("user_id"))
    return render_template("data_page.html", context=transactions)

@app.route("/create", methods = ["GET","POST"])
def create():
    if session.get("user_id") is None:
        return redirect("/login")
    if request.method == "POST":
        try:
            TransactionRepo.create_transactions(amount=request.form["amount"], category=request.form["category"], user_id=session.get("user_id"))
        except ValueError:
            return render_template("create_transaction.html", error="Please enter an amount greater than 0, like 50 or 19.99.")
        return redirect("/data")
    return render_template("create_transaction.html")
        

@app.route("/logout", methods = ["GET","POST"])
def logout():
    session.pop("user_id", None)
    return redirect("/login")




if __name__ == "__main__":
    app.run(debug=True, port=5001)