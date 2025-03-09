# Challenge Cookie Hacking

### Obiettivo:
Ottieni la flag manipolando i cookie per effettuare un acquisto con fondi insufficienti.

### Vulnerabilità:
L'applicazione utilizza i cookie per memorizzare il saldo dell'utente e il totale del carrello. Tuttavia, questi valori possono essere modificati manualmente dall'utente per bypassare il controllo sui fondi e acquistare l'oggetto "flag".

### Avvio:
```bash
docker pull ghcr.io/ax3lt/cookie-ch3
docker run -p 80:80 ghcr.io/ax3lt/cookie-ch3

```

### Codice (Python):
```python
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
                return jsonify({"message": "Complimenti! Ecco la tua flag: FLAG{}"})
            return jsonify({"message": "Acquisto riuscito! Ma niente flag per te..."})
        else:
            return jsonify({"message": "Fondi insufficienti! Cerca di essere più... creativo!"})
    except Exception as e:
        return jsonify({"message": f"Errore nel processo di checkout! {e}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
```

### Codice (Node.js):
```javascript
const express = require('express');
const cookieParser = require('cookie-parser');
const app = express();
const path = require('path');

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'static')));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'templates'));

const ITEMS = {
    "pizza": 10,
    "birra": 5,
    "panino": 7,
    "patatine": 4,
    "flag": 9999
};

const USERS = {};

const INITIAL_BALANCE = 15;

app.get('/', (req, res) => {
    res.render('index');
});

app.get('/login', (req, res) => {
    res.render('login');
});

app.post('/login', (req, res) => {
    const { username, password } = req.body;
    if (USERS[username] && USERS[username] === password) {
        res.cookie('balance', INITIAL_BALANCE.toString());
        res.redirect('/shop');
    } else {
        res.status(403).send('Credenziali errate!');
    }
});

app.get('/register', (req, res) => {
    res.render('register');
});

app.post('/register', (req, res) => {
    const { username, password } = req.body;
    if (!(username in USERS)) {
        USERS[username] = password;
        res.redirect('/login');
    } else {
        res.status(400).send('Username già in uso!');
    }
});

app.get('/shop', (req, res) => {
    const balance = req.cookies.balance || INITIAL_BALANCE.toString();
    res.cookie('balance', balance);
    res.render('shop', { items: ITEMS, balance });
});

app.post('/checkout', (req, res) => {
    try {
        const balance = parseInt(req.cookies.balance || '0');
        const total = parseInt(req.cookies.total || '0');
        const cart = req.body.cart || [];

        if (total <= balance) {
            if (cart.includes('flag')) {
                res.json({ message: 'Complimenti! Ecco la tua flag: FLAG{}' });
            } else {
                res.json({ message: 'Acquisto riuscito! Ma niente flag per te...' });
            }
        } else {
            res.json({ message: 'Fondi insufficienti! Cerca di essere più... creativo!' });
        }
    } catch (e) {
        res.json({ message: `Errore nel processo di checkout! ${e}` });
    }
});

app.listen(80, '0.0.0.0', () => {
    console.log('Server in ascolto sulla porta 80');
});