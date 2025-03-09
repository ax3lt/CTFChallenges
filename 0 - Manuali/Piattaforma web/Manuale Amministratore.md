# 👨‍💼 Manuale Amministratore - Piattaforma CTF

## 📋 Indice
- [Dashboard Amministrativa](#dashboard-amministrativa)
  - [Statistiche Generali](#statistiche-generali)
  - [Grafici di Analisi](#grafici-di-analisi)
  - [Monitor Challenge](#monitor-challenge)
  - [Ultime Attività](#ultime-attività)
- [Gestione Immagini Docker](#gestione-immagini-docker)
  - [Visualizzazione](#visualizzazione)
  - [Operazioni CRUD](#operazioni-crud)
  - [Troubleshooting Docker](#troubleshooting-docker)
- [Gestione Utenti](#gestione-utenti)
  - [Visualizzazione Utenti](#visualizzazione-utenti)
  - [Operazioni Utente](#operazioni-utente)
  - [Sicurezza Account](#sicurezza-account)
- [Gestione Challenge](#gestione-challenge)
  - [Visualizzazione Challenge](#visualizzazione-challenge)
  - [Operazioni Challenge](#operazioni-challenge)
  - [Gestione Stato](#gestione-stato)
  - [Soluzioni e Monitoraggio](#soluzioni-e-monitoraggio)
- [Sicurezza Piattaforma](#sicurezza-piattaforma)
  - [Protezioni Implementate](#protezioni-implementate)
  - [Best Practices](#best-practices)
  - [Monitoraggio](#monitoraggio)

## 📊 Dashboard Amministrativa

### 📈 Statistiche Generali

#### 🎯 Card Challenges
| Metrica | Descrizione |
|---------|-------------|
| Totale Challenge | Numero totale disponibili |
| Challenge Online | Numero attualmente attive |
| Tasso Attività | % challenge online |

#### 👥 Card Utenti
| Metrica | Descrizione |
|---------|-------------|
| Utenti Totali | Numero registrati |
| Nuovi Oggi | Registrazioni giornaliere |
| Crescita | % crescita giornaliera |

#### 🎌 Card Flag
| Metrica | Descrizione |
|---------|-------------|
| Flag Inviate | Tentativi totali oggi |
| Flag Corrette | Successi oggi |
| Tasso Successo | % successo giornaliero |

#### ⭐ Card Soluzioni
| Metrica | Descrizione |
|---------|-------------|
| Soluzioni Corrette | Totale completamenti |
| Tentativi Totali | Tutti i tentativi |
| Tasso Globale | % successo globale |

### 📊 Grafici di Analisi

#### 📈 Attività Settimanale
- Grafico andamento 7 giorni
- Flag totali vs corrette
- Area con gradiente
- No zoom per pulizia

#### 🏆 Top 5 Challenge
- Grafico a ciambella
- % completamento per challenge
- Legenda interattiva

### 📋 Monitor Challenge
| Colonna | Descrizione |
|---------|-------------|
| Nome | Identificativo challenge |
| Stato | Online/Offline |
| Porta | Porta esposta |
| Soluzioni | Numero completamenti |
| Ultimo Check | Timestamp controllo |
| Azioni | Link modifica rapida |

### 📝 Ultime Attività
| Colonna | Descrizione |
|---------|-------------|
| Email | Identificativo utente |
| Azione | Flag Corretta/Errata |
| Challenge | Nome challenge |
| Timestamp | Data e ora |

## 🐳 Gestione Immagini Docker

### 👁️ Visualizzazione
- Tabella immagini registrate
- Ordinamento colonne
- Ricerca testuale
- Paginazione automatica

### ⚙️ Operazioni CRUD

#### ➕ Aggiunta Immagine
1. Click "Aggiungi nuova immagine"
2. Compila modal:
   - 📝 Nome descrittivo
   - 🔗 Docker Image URL
3. Click "Aggiungi"

⚠️ Note:
- URL pubblicamente accessibile
- No duplicati
- Validazione automatica

#### ❌ Eliminazione
1. Click icona cestino
2. Conferma eliminazione

⚠️ Limitazioni:
- No eliminazione se in uso
- Rimozione DB + Docker locale

### 🔧 Troubleshooting Docker

#### 🚫 Errore "Immagine Esistente"
- ✅ Verifica duplicati
- ✅ Elimina se necessario

#### 🔄 Errore Pull
- ✅ Verifica URL
- ✅ Controlla accesso pubblico
- ✅ Verifica Docker Desktop
- ✅ Controlla connessione

## 👥 Gestione Utenti

### 📋 Visualizzazione Utenti
| Colonna | Descrizione |
|---------|-------------|
| Username | Nome utente |
| Email | Contatto |
| Anno | Corso frequentato |
| Ruolo | Admin/Utente |
| Punti | Score totale |
| Visibilità | Stato profilo |
| Ultimo Accesso | Timestamp |
| IP | Ultimo IP |
| Tema | UI preference |
| Creazione | Data registrazione |

### ⚙️ Operazioni Utente

#### ➕ Nuovo Utente
1. Click "Aggiungi Utente"
2. Compila form:
   - 👤 Username univoco
   - 📧 Email univoca
   - 📚 Anno (1-5)
   - 🔑 Password iniziale
   - 👑 Ruolo
   - 🎨 Tema UI

#### ✏️ Modifica
- Username/Email
- Anno/Password
- Ruolo/Punti
- Visibilità/Tema

#### ❌ Eliminazione
- Anonimizzazione dati
- Preservazione statistiche
- Protezione admin

### 🔒 Sicurezza Account
- 🔑 Hash password (SHA-256)
- 📝 Log IP
- 🛡️ Token CSRF
- 👮 Accesso limitato

## 🎮 Gestione Challenge

### 📋 Visualizzazione Challenge
- Griglia di card
- Ricerca globale
- Filtri stato/categoria
- Card espandibili

### ⚙️ Operazioni Challenge

#### ➕ Nuova Challenge
1. Click "Crea challenge"
2. Configura:
   - 📝 Nome univoco
   - 📄 Descrizione markdown
   - 👁️ Visibilità
   - 🔌 Porte
   - ⭐ Punti
   - 🎌 Flag
   - 🏷️ Categorie
   - 💡 Suggerimenti
   - 🐳 Immagine Docker

#### 🎮 Gestione Stato
| Azione | Effetto |
|--------|---------|
| ▶️ Start | Avvio container |
| ⏹️ Stop | Stop container |
| 🔄 Restart | Reset stato |

### 📊 Soluzioni e Monitoraggio
- 📈 Statistiche realtime
- 📝 Log tentativi
- 🔍 Analisi performance
- 📊 Export dati

## 🔒 Sicurezza Piattaforma

### 🛡️ Protezioni Implementate

#### 🔑 Gestione Sessioni
```javascript
// Configurazione sessioni sicure
{
  secret: process.env.SESSION_SECRET,
  name: 'sessionId',
  cookie: {
    httpOnly: true,
    sameSite: 'strict',
    maxAge: 24 * 60 * 60 * 1000 // 24 ore
  }
}
```

#### 🚫 Rate Limiting
| Tipo | Limite | Finestra |
|------|---------|----------|
| Generale | 100 richieste | 15 minuti |
| Auth | 15 tentativi | 15 minuti |

#### 🛡️ Security Headers
| Header | Valore | Scopo |
|--------|---------|--------|
| X-Content-Type-Options | nosniff | Previene MIME-sniffing |
| X-Frame-Options | DENY | Previene clickjacking |
| X-XSS-Protection | 1; mode=block | Protezione XSS browser |
| Referrer-Policy | strict-origin-when-cross-origin | Controllo referrer |

#### 🔐 CSRF Protection
```html
<!-- Token CSRF in ogni form -->
<input type="hidden" name="_csrf" value="{{ csrfToken }}">
```

#### 🧹 Sanitizzazione Input
| Protezione | Implementazione | Scopo |
|------------|----------------|--------|
| XSS | express-xss-sanitizer | Sanitizza input |
| MongoDB | express-mongo-sanitize | Previene NoSQL injection |
| JSON | limit: '10kb' | Previene DOS |

### 🔧 Configurazioni di Sicurezza

#### 🌐 CORS
```javascript
cors({
  origin: process.env.CORS_ORIGIN,
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
})
```

#### 💾 Database
| Configurazione | Valore | Scopo |
|----------------|--------|--------|
| Connection Timeout | 5000ms | Previene hanging |
| Socket Timeout | 45000ms | Gestione timeout |
| Auto Remove | native | Pulizia sessioni |

#### 🔒 Helmet
- Configurazione automatica headers sicurezza
- Disabilitazione x-powered-by
- Protezione contro attacchi comuni

### 📝 Logging e Monitoraggio

#### 🔍 Log di Sistema
| Evento | Dati Registrati |
|--------|----------------|
| Errori | Timestamp, URL, Method, Stack |
| Auth | Tentativi, IP, Timestamp |
| CSRF | URL, Method, Headers |
| Server | Error Details, Request Data |

#### ⚠️ Sistema di Alert
| Trigger | Azione |
|---------|---------|
| Auth Falliti | Log + Rate Limit |
| CSRF Invalid | Redirect + Session Reset |
| Error 500 | Log Dettagliato + Alert |
| Rate Limit | Blocco Temporaneo |

#### 📊 Monitoraggio Real-time
- 📈 Performance metriche
- 🔍 Pattern sospetti
- 🚫 Tentativi bloccati
- ⚡ Latenza sistema

### 🏗️ Best Practices Implementate

#### 🔐 Gestione Errori
```javascript
// Gestione errori sicura
{
  title: `Errore ${statusCode}`,
  message: errorMessage,
  // No stack traces in produzione
  stack: process.env.NODE_ENV === 'development' ? err.stack : null
}
```

#### 🛡️ Sicurezza Applicativa
- ✅ Validazione input server-side
- ✅ Sanitizzazione output
- ✅ Gestione sessioni sicura
- ✅ Rate limiting configurabile
- ✅ CORS restrittivo
- ✅ CSP implementato

#### 🔒 Protezione Dati
- ✅ Encryption in transit
- ✅ Sanitizzazione MongoDB
- ✅ Validazione parametri
- ✅ Protezione sessioni
- ✅ Cookie sicuri

### 🔄 Procedure di Manutenzione

#### 📋 Checklist Giornaliera
- [ ] Verifica log errori
- [ ] Controllo rate limiting
- [ ] Monitoraggio accessi
- [ ] Check performance

#### 🔍 Review Settimanale
- [ ] Analisi pattern attacco
- [ ] Verifica configurazioni
- [ ] Update dipendenze
- [ ] Backup database

#### 📊 Report Mensile
- [ ] Statistiche sicurezza
- [ ] Trend attacchi
- [ ] Performance review
- [ ] Update policy 