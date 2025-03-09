# 📘 Manuale Utente - CTF Platform

## 📋 Indice
- [Requisiti di Sistema](#requisiti-di-sistema)
- [Guida Rapida](#guida-rapida)
  - [Avvio di Docker](#avvio-di-docker)
  - [Download delle Immagini](#download-delle-immagini)
  - [Avvio delle Sfide](#avvio-delle-sfide)
- [Catalogo Sfide](#catalogo-sfide)
  - [Introduzione](#introduzione)
  - [Cookies](#cookies)
  - [CSRF](#csrf)
  - [SSRF](#ssrf)
  - [XSS](#xss)
  - [SQLI](#sqli)
- [Comandi Utili](#comandi-utili)
- [Risoluzione Problemi](#risoluzione-problemi)
- [Note Tecniche](#note-tecniche)
  - [Dettagli delle Sfide](#dettagli-delle-sfide)
  - [Gestione delle Risorse](#gestione-delle-risorse)
  - [Sicurezza](#sicurezza)

## 🔧 Requisiti di Sistema
Prima di iniziare, assicurati di avere:
- Docker installato sul tuo sistema operativo
- Una connessione internet stabile per scaricare le immagini
- Almeno 2GB di spazio libero su disco
- 4GB di RAM consigliati

## 🚀 Guida Rapida

### Avvio di Docker
1. Avvia Docker Desktop
2. Attendi che l'icona nella barra delle applicazioni smetta di animarsi
3. Verifica che lo stato sia "Docker Desktop is running"

### Download delle Immagini
```bash
# Sintassi generale
docker pull ax3lt/ctfplatform:nome-sfida

# Esempio
docker pull ax3lt/ctfplatform:intro-ch1
```

### Avvio delle Sfide
```bash
# Sintassi generale
docker run -p 8000:80 ax3lt/ctfplatform:nome-sfida

# La sfida sarà accessibile su
http://localhost:8000
```

## 📚 Catalogo Sfide

### Introduzione
| Sfida | Descrizione |
|-------|-------------|
| intro-ch1 | Prima sfida introduttiva |
| intro-ch2 | Seconda sfida introduttiva |

### Cookies
| Sfida | Descrizione |
|-------|-------------|
| cookies-ch1 | Cookie login |
| cookies-ch2 | Session bruteforce |
| cookies-ch3 | Cookie shop |
| cookies-ch4 | HMAC Cookie |

### CSRF
| Sfida | Descrizione |
|-------|-------------|
| csrf-ch1 | Money transfer |

### SSRF
| Sfida | Descrizione |
|-------|-------------|
| ssrf-ch1 | Private Webserver |

### XSS
| Sfida | Descrizione |
|-------|-------------|
| xss-ch1 | Reflected XSS |
| xss-ch2 | Stored XSS |
| xss-ch3 | Stored XSS Forum Wrong Sanitization |

### SQLI
| Sfida | Descrizione |
|-------|-------------|
| sqli-ch1 | WhiteBox Injection |
| sqli-ch2 | Union Injection Filtered |
| sqli-ch3 | Time Based Blind Injection |

## 🛠️ Comandi Utili

### Gestione Container
```bash
# Fermare una sfida in esecuzione
CTRL+C nel terminale
# oppure
docker ps    # per vedere l'ID del container
docker stop ID_CONTAINER

# Vedere sfide in esecuzione
docker ps

# Rimuovere container fermato
docker rm ID_CONTAINER

# Vedere immagini scaricate
docker images
```

## ❗ Risoluzione Problemi

### Porta in Uso
Se la porta 80 è già occupata:
```bash
# Usa una porta alternativa
docker run -p 8080:80 ax3lt/ctfplatform:nome-sfida
# La sfida sarà su http://localhost:8080
```

### Problemi di Avvio
Se l'immagine non si avvia:
1. Ferma tutti i container in esecuzione
2. Riavvia Docker Desktop
3. Riprova il comando run

### Aggiornamento Immagini
```bash
# Forza il riscariamento di un'immagine
docker pull ax3lt/ctfplatform:nome-sfida
```

## 📋 Note Tecniche

### Dettagli delle Sfide

#### Introduzione
- intro-ch1: Porta 80, no database
- intro-ch2: Porta 80, no database

#### Cookies
- cookies-ch1: Porta 80, database SQLite
- cookies-ch2: Porta 80, database SQLite
- cookies-ch3: Porta 80, database MySQL
- cookies-ch4: Porta 80, database SQLite

#### CSRF
- csrf-ch1: Porta 80, database MySQL

#### SSRF
- ssrf-ch1: Porte 80 e servizio interno sulla 8080

#### XSS
- xss-ch1: Porta 80, no database
- xss-ch2: Porta 80, database MySQL + bot Chrome
- xss-ch3: Porta 80, database MySQL + bot Chrome

#### SQLI
- sqli-ch1: Porta 80, database MySQL
- sqli-ch2: Porta 80, database MySQL
- sqli-ch3: Porta 80, database MySQL

### Gestione delle Risorse
- ✅ Ogni container è isolato e ha le proprie risorse
- ✅ Il database viene reinizializzato ad ogni riavvio
- ✅ I file caricati vengono eliminati alla chiusura del container

### Sicurezza
- ⚠️ Le sfide sono progettate per essere eseguite localmente
- ⚠️ Non esporre le porte dei container su internet
- ⚠️ Utilizzare password diverse da quelle di produzione
- ⚠️ Non utilizzare dati sensibili nelle sfide