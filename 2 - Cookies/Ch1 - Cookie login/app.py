from flask import Flask, request, make_response, redirect, render_template

app = Flask(__name__)

USERS = {
    "admin": "dnshjakjdhlsahjklnsdanlkdskohhellna"
}

FLAG = "flag{COOKIES_ARE_NOT_SAFE}"

@app.route("/")
def index():
    username = request.cookies.get("username")
    if username:
        return redirect("/profile")
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in USERS:
            return "Questo username è già registrato!"

        USERS[username] = password
        resp = make_response(redirect("/profile"))
        resp.set_cookie("username", username)
        resp.set_cookie("password", password)
        return resp

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if USERS.get(username) == password:
            resp = make_response(redirect("/profile"))
            resp.set_cookie("username", username)
            resp.set_cookie("password", password)
            return resp
        else:
            return "Credenziali errate!"

    return render_template("login.html")

@app.route("/profile")
def profile():
    username = request.cookies.get("username")

    if not username or username not in USERS:
        return redirect("/login")

    is_admin = username == "admin"

    return render_template("profile.html", username=username, is_admin=is_admin, flag=FLAG if is_admin else None)

@app.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.set_cookie("username", "", expires=0)
    resp.set_cookie("password", "", expires=0)
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
