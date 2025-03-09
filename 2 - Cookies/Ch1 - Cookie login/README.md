# Challenge HTTP e Cookie

### Obiettivo:
Ottieni accesso all'account **admin** per ottenere la flag.

### Vulnerabilità:
- **I cookie memorizzano la password in chiaro**, permettendo di **modificarli manualmente**.
- Nessuna protezione contro la **manipolazione dei cookie**.

### Suggerimenti:
1. Prova a cambiare i valori dei cookie direttamente nel browser (con la console o strumenti DevTools).
2. Esplora il codice per trovare la vulnerabilità.

### Avviare il server:
```bash
docker build -t cookie_challenge .
docker run -p 8080:80 cookie_challenge //TODO update this with image link
```

### Codice:
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
const FLAG = "";

app.get('/', (req, res) => {
  const username = req.cookies.username;
  if (username) {
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
  res.cookie('username', username);
  res.cookie('password', password);
  res.redirect('/profile');
});

app.get('/login', (req, res) => {
  res.render('login');
});

app.post('/login', (req, res) => {
  const { username, password } = req.body;

  if (USERS[username] === password) {
    res.cookie('username', username);
    res.cookie('password', password);
    res.redirect('/profile');
  } else {
    res.send("Credenziali errate!");
  }
});

app.get('/profile', (req, res) => {
  const username = req.cookies.username;

  if (!username || !USERS[username]) {
    return res.redirect('/login');
  }

  const is_admin = username === "admin";
  
  res.render('profile', {
    username: username,
    is_admin: is_admin,
    flag: is_admin ? FLAG : null
  });
});

app.get('/logout', (req, res) => {
  res.clearCookie('username');
  res.clearCookie('password');
  res.redirect('/');
});

app.listen(80, '0.0.0.0', () => {
  console.log('Server in ascolto sulla porta 80');
});
```