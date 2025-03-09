# 📘 Manuale Docente - CTF Platform

## 📋 Indice
- [Requisiti di Sistema](#requisiti-di-sistema)
- [Gestione Docker](#gestione-docker)
  - [Avvio e Login](#avvio-e-login)
  - [Creazione Immagini](#creazione-immagini)
  - [Push su Docker Hub](#push-su-docker-hub)
- [Convenzioni di Naming](#convenzioni-di-naming)
- [Verifica e Troubleshooting](#verifica-e-troubleshooting)
- [Esempio Pratico](#esempio-pratico)
  - [Server Express](#server-express)
  - [Dockerfile](#dockerfile)
  - [Build e Push](#build-e-push)

## 🔧 Requisiti di Sistema
Prima di iniziare, assicurati di avere:
- Docker installato sul sistema operativo
- Account su Docker Hub (registrazione gratuita su https://hub.docker.com)
- Almeno 2GB di spazio libero su disco
- 4GB di RAM consigliati
- Docker Desktop versione 4.0 o superiore

## 🐳 Gestione Docker

### Avvio e Login

1. **Avvio di Docker**
```bash
# 1. Avvia Docker Desktop
# 2. Attendi che l'icona smetta di animarsi
# 3. Verifica lo stato: "Docker Desktop is running"
```

2. **Login su Docker Hub**
```bash
# Esegui il login
docker login

# Inserisci le credenziali quando richiesto
# Username: il tuo username Docker Hub
# Password: la tua password Docker Hub

# Verifica il messaggio "Login Succeeded"
```

### Creazione Immagini

```bash
# Sintassi generale
docker build -t nomeaccount/ctfplatform:nome-sfida ".\ChallengeCTF\categoria\nome-cartella-sfida"

# Esempio pratico
docker build -t docente/ctfplatform:intro-ch1 ".\ChallengeCTF\1 - Introduzione\Ch1"
```

### Push su Docker Hub

```bash
# Sintassi generale
docker push nomeaccount/ctfplatform:nome-sfida

# Esempio pratico
docker push docente/ctfplatform:intro-ch1
```

## 📝 Convenzioni di Naming

| Categoria | Pattern | Esempi |
|-----------|---------|--------|
| Introduzione | intro-ch[n] | intro-ch1, intro-ch2 |
| Cookies | cookies-ch[n] | cookies-ch1, cookies-ch2 |
| CSRF | csrf-ch[n] | csrf-ch1 |
| SSRF | ssrf-ch[n] | ssrf-ch1 |
| XSS | xss-ch[n] | xss-ch1, xss-ch2 |
| SQLI | sqli-ch[n] | sqli-ch1, sqli-ch2 |

## ❗ Verifica e Troubleshooting

### Verifica del Push
```bash
# Verifica le immagini caricate
https://hub.docker.com/r/nomeaccount/ctfplatform/tags
```

### Troubleshooting Comune

#### 1. Errore "permission denied"
- ✅ Verifica i permessi di amministratore
- ✅ Su Linux, aggiungi l'utente al gruppo docker

#### 2. Errore "port already in use"
- ✅ Verifica che le porte 80/8080 siano libere
- ✅ Usa porte alternative se necessario

#### 3. Errore durante il build
- ✅ Verifica la connessione internet
- ✅ Controlla lo spazio su disco
- ✅ Pulisci la cache: `docker system prune`

## 💻 Esempio Pratico

### Server Express

#### Struttura del Progetto
```
mia-sfida/
├── src/
│   └── index.js
└── Dockerfile
```

#### File `src/index.js`
```javascript
const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Benvenuto nella sfida CTF!');
});

app.listen(port, () => {
  console.log(`Server in esecuzione sulla porta ${port}`);
});
```

### Dockerfile

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY src/ ./src/
EXPOSE 3000
CMD ["node", "src/index.js"]
```

### Build e Push

```bash
# Build dell'immagine
docker build -t tuousername/ctfplatform:mia-sfida ./mia-sfida

# Push su Docker Hub
docker push tuousername/ctfplatform:mia-sfida
```

## ⚠️ Note di Sicurezza
- Non includere credenziali nei Dockerfile
- Usa .dockerignore per file sensibili
- Minimizza la dimensione delle immagini
- Esegui scan di sicurezza sulle immagini
- Mantieni aggiornate le dipendenze