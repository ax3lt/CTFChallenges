# Challenge BruteForce Cookie

### Obiettivo:
Accedi all'account **admin** ottenendo il cookie di sessione corretto tramite bruteforce.

### Vulnerabilità:
Il cookie "session_token" è generato da un set finito di numeri rendendo l'intero spazio di possibili token (0–50) estremamente ridotto.
Questo permette di forzare manualmente o via script il token admin.

### Avvio:
```bash
docker pull ghcr.io/ax3lt/cookie-ch2
docker run -p 80:80 ghcr.io/ax3lt/cookie-ch2
```

### Codice (Python):
```python
import random
from flask import Flask, request, make_response, redirect, render_template

app = Flask(__name__)

USERS = {

}
SESSIONS = {}

FLAG = ""

def generate_session_token():
    token = random.randint(0, 50)
    print(f"generated token: {token}")
    return f"session_{token}"

adminToken = generate_session_token()
SESSIONS[adminToken] = "admin"

@app.route("/")
def index():
    token = request.cookies.get("session_token")
    if token and token in SESSIONS:
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
        token = generate_session_token()

        while token in SESSIONS:
            token = generate_session_token()

        SESSIONS[token] = username
        resp = make_response(redirect("/profile"))
        resp.set_cookie("session_token", token)
        return resp

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in USERS and USERS[username] == password:
            token = generate_session_token()
            SESSIONS[token] = username
            resp = make_response(redirect("/profile"))
            resp.set_cookie("session_token", token)
            return resp
        else:
            return "Credenziali errate!"

    return render_template("login.html")

@app.route("/profile")
def profile():
    token = request.cookies.get("session_token")
    if not token or token not in SESSIONS:
        return redirect("/login")

    username = SESSIONS[token]
    is_admin = username == "admin"
    return render_template("profile.html", username=username, is_admin=is_admin, flag=FLAG if is_admin else None)

@app.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.set_cookie("session_token", "", expires=0)
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
```

### Codice (Node.js):
```javascript
const express = require('express');
const cookieParser = require('cookie-parser');
const app = express();
const path = require('path');

app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'static')));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'templates'));

const USERS = {};
const SESSIONS = {};
const FLAG = "";

function generateSessionToken() {
  const token = Math.floor(Math.random() * 51); // 0-50
  console.log(`generated token: ${token}`);
  return `session_${token}`;
}

// Crea token admin all'avvio
const adminToken = generateSessionToken();
SESSIONS[adminToken] = "admin";

app.get('/', (req, res) => {
  const token = req.cookies.session_token;
  if (token && SESSIONS[token]) {
    return res.redirect('/profile');
  }
  return res.render('index');
});

app.get('/register', (req, res) => {
  res.render('register');
});

app.post('/register', (req, res) => {
  const { username, password } = req.body;
  
  if (USERS[username]) {
    return res.send("Questo username è già registrato!");
  }

  USERS[username] = password;
  let token = generateSessionToken();
  
  // Assicuriamoci che il token non sia già in uso
  while (SESSIONS[token]) {
    token = generateSessionToken();
  }
  
  SESSIONS[token] = username;
  res.cookie('session_token', token);
  res.redirect('/profile');
});

app.get('/login', (req, res) => {
  res.render('login');
});

app.post('/login', (req, res) => {
  const { username, password } = req.body;

  if (USERS[username] && USERS[username] === password) {
    const token = generateSessionToken();
    SESSIONS[token] = username;
    res.cookie('session_token', token);
    res.redirect('/profile');
  } else {
    res.send("Credenziali errate!");
  }
});

app.get('/profile', (req, res) => {
  const token = req.cookies.session_token;
  
  if (!token || !SESSIONS[token]) {
    return res.redirect('/login');
  }

  const username = SESSIONS[token];
  const is_admin = username === "admin";
  
  res.render('profile', {
    username: username,
    is_admin: is_admin,
    flag: is_admin ? FLAG : null
  });
});

app.get('/logout', (req, res) => {
  res.clearCookie('session_token');
  res.redirect('/');
});

app.listen(80, '0.0.0.0', () => {
  console.log('Server in ascolto sulla porta 80');
});
```