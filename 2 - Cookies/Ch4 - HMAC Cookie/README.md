# Challenge HMAC Cookie

### Obiettivo:
Ottieni accesso all'account **admin** per ottenere la flag.

### Vulnerabilità:
- Il sistema usa **Base64** per codificare i cookie, quindi si può decodificare facilmente.
- La **firma HMAC** è basata sul **ruolo** (`user` e `admin`).
- Se un attaccante conosce la chiave, può calcolare la firma per qualunque cookie.

### Suggerimenti:
1. Decodifica il cookie per vedere la struttura del payload.
2. Scopri come viene calcolata la firma.
3. Costruisci un nuovo cookie con `role: "admin"`, firmalo con la chiave giusta e autenticati.
4. Esistono dei tool come [CyberChef](https://gchq.github.io/CyberChef/) che possono aiutarti a codificare/decodificare determinati valori.

### Avviare il server:
```bash
docker build -t hmac_cookie_challenge .
docker run -p 80:80 hmac_cookie_challenge
```

### Codice (Python):
```python
import os
import hmac
import hashlib
import base64
import json
from flask import Flask, request, make_response, redirect, render_template

app = Flask(__name__)

USERS = {
    "admin": {"password": "", "role": "admin"},
}

FLAG = ""

def get_secret_key(role):
    return f"{role}".encode()

def generate_signed_cookie(username, role):
    payload = {"username": username, "password": USERS[username]["password"], "role": role}
    payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode()

    secret_key = get_secret_key(role)
    signature = hmac.new(secret_key, payload_b64.encode(), hashlib.sha256).hexdigest()

    return payload_b64, signature

def verify_signed_cookie(payload_b64, signature):
    try:
        payload_json = json.loads(base64.b64decode(payload_b64).decode())

        secret_key = get_secret_key(payload_json["role"])
        expected_signature = hmac.new(secret_key, payload_b64.encode(), hashlib.sha256).hexdigest()

        return expected_signature == signature, payload_json
    except Exception:
        return False, None

@app.route("/")
def index():
    username = request.cookies.get("auth_data")
    signature = request.cookies.get("auth_signature")

    if username and signature:
        return redirect("/profile")

    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in USERS:
            return "Questo username è già registrato!"

        USERS[username] = {"password": password, "role": "user"}

        # Genera cookie
        auth_data, auth_signature = generate_signed_cookie(username, "user")
        resp = make_response(redirect("/profile"))
        resp.set_cookie("auth_data", auth_data)
        resp.set_cookie("auth_signature", auth_signature)

        return resp

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = USERS.get(username)
        if user and user["password"] == password:
            auth_data, auth_signature = generate_signed_cookie(username, user["role"])
            resp = make_response(redirect("/profile"))
            resp.set_cookie("auth_data", auth_data)
            resp.set_cookie("auth_signature", auth_signature)
            return resp

        return "Credenziali errate!"

    return render_template("login.html")

@app.route("/profile")
def profile():
    payload_b64 = request.cookies.get("auth_data")
    signature = request.cookies.get("auth_signature")

    if not payload_b64 or not signature:
        return redirect("/login")

    valid, user_data = verify_signed_cookie(payload_b64, signature)

    if not valid:
        return "Cookie non valido!"

    username = user_data["username"]
    role = user_data["role"]
    is_admin = role == "admin"

    return render_template("profile.html", username=username, is_admin=is_admin, flag=FLAG if is_admin else None)

@app.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.set_cookie("auth_data", "", expires=0)
    resp.set_cookie("auth_signature", "", expires=0)
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
```

### Codice (Node.js):
```javascript
const express = require('express');
const cookieParser = require('cookie-parser');
const crypto = require('crypto');
const app = express();
const path = require('path');

app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'static')));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'templates'));

const USERS = {
    "admin": { password: "supersecret", role: "admin" }
};

const FLAG = "";

function getSecretKey(role) {
    return Buffer.from(role);
}

function generateSignedCookie(username, role) {
    const payload = {
        username: username,
        password: USERS[username].password,
        role: role
    };
    
    const payloadB64 = Buffer.from(JSON.stringify(payload)).toString('base64');
    const secretKey = getSecretKey(role);
    
    const hmac = crypto.createHmac('sha256', secretKey);
    hmac.update(payloadB64);
    const signature = hmac.digest('hex');
    
    return [payloadB64, signature];
}

function verifySignedCookie(payloadB64, signature) {
    try {
        const payload = JSON.parse(Buffer.from(payloadB64, 'base64').toString());
        const secretKey = getSecretKey(payload.role);
        
        const hmac = crypto.createHmac('sha256', secretKey);
        hmac.update(payloadB64);
        const expectedSignature = hmac.digest('hex');
        
        return [expectedSignature === signature, payload];
    } catch (e) {
        return [false, null];
    }
}

app.get('/', (req, res) => {
    const { auth_data, auth_signature } = req.cookies;
    
    if (auth_data && auth_signature) {
        return res.redirect('/profile');
    }
    
    res.render('index');
});

app.get('/register', (req, res) => {
    res.render('register');
});

app.post('/register', (req, res) => {
    const { username, password } = req.body;
    
    if (username in USERS) {
        return res.send("Questo username è già registrato!");
    }
    
    USERS[username] = { password, role: "user" };
    
    const [authData, authSignature] = generateSignedCookie(username, "user");
    res.cookie('auth_data', authData);
    res.cookie('auth_signature', authSignature);
    res.redirect('/profile');
});

app.get('/login', (req, res) => {
    res.render('login');
});

app.post('/login', (req, res) => {
    const { username, password } = req.body;
    const user = USERS[username];
    
    if (user && user.password === password) {
        const [authData, authSignature] = generateSignedCookie(username, user.role);
        res.cookie('auth_data', authData);
        res.cookie('auth_signature', authSignature);
        res.redirect('/profile');
    } else {
        res.send("Credenziali errate!");
    }
});

app.get('/profile', (req, res) => {
    const { auth_data: payloadB64, auth_signature: signature } = req.cookies;
    
    if (!payloadB64 || !signature) {
        return res.redirect('/login');
    }
    
    const [valid, userData] = verifySignedCookie(payloadB64, signature);
    
    if (!valid) {
        return res.send("Cookie non valido!");
    }
    
    const { username, role } = userData;
    const isAdmin = role === "admin";
    
    res.render('profile', {
        username,
        is_admin: isAdmin,
        flag: isAdmin ? FLAG : null
    });
});

app.get('/logout', (req, res) => {
    res.clearCookie('auth_data');
    res.clearCookie('auth_signature');
    res.redirect('/');
});

app.listen(80, '0.0.0.0', () => {
    console.log('Server in ascolto sulla porta 80');
});
```