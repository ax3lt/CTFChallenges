from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify

app = Flask(__name__)

ITEMS = {
    "pizza": 10,
    "birra": 5,
    "panino": 7,
    "patatine": 4,
    "flag": 9999
}

USERS = {}

INITIAL_BALANCE = 15

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in USERS and USERS[username] == password:
            response = make_response(redirect(url_for("shop")))
            response.set_cookie("balance", str(INITIAL_BALANCE))
            return response
        return "Credenziali errate!", 403
    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username not in USERS:
            USERS[username] = password
            return redirect(url_for("login"))
        return "Username già in uso!", 400
    return render_template("register.html")

@app.route('/shop')
def shop():
    balance = request.cookies.get("balance", str(INITIAL_BALANCE))
    response = make_response(render_template("shop.html", items=ITEMS, balance=balance))
    response.set_cookie("balance", balance)

    return response

@app.route('/checkout', methods=["POST"])
def checkout():
    try:
        balance = int(request.cookies.get("balance", 0))
        total = int(request.cookies.get("total", 0))
        cart = request.json.get("cart", [])

        if total <= balance:
            if "flag" in cart:
                return jsonify({"message": "Complimenti! Ecco la tua flag: FLAG{cookie_hacking_master}"})
            return jsonify({"message": "Acquisto riuscito! Ma niente flag per te..."})
        else:
            return jsonify({"message": "Fondi insufficienti! Cerca di essere più... creativo!"})
    except Exception as e:
        return jsonify({"message": f"Errore nel processo di checkout! {e}"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
