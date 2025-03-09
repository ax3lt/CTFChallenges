# Challenge: Wrong Sanitization - Bypass XSS Filtering

## Descrizione
Questo sito web è un piccolo forum in cui gli utenti possono lasciare commenti e personalizzarli con un colore e un'immagine.  
Il problema? Il codice tenta di prevenire gli attacchi **XSS (Cross-Site Scripting)**, ma lo fa in modo errato! 😈

L'admin visita periodicamente la pagina `/profile`, dove sono visibili tutti i commenti.  
Se riuscissi a **bypassare la sanitizzazione e iniettare uno script malevolo**, potresti ottenere la sua sessione e accedere alla flag segreta su `/flag`.

## Obiettivo
- **Trova un modo per iniettare codice malevolo** nonostante i tentativi di sanitizzazione.
- **Fai eseguire il tuo script quando l'admin visita la pagina** `/profile`.
- **Recupera la flag** che si trova su `/flag`.

## Suggerimenti
- Il codice sostituisce `<script>` con una versione "sanitizzata", ma ci sono altri modi per eseguire JavaScript.
- Prova a sfruttare gli **attributi HTML degli elementi img o div** (`onerror`, `onmouseover`, ecc.).
- Se riesci a eseguire JavaScript, usa `fetch('/flag')` per ottenere il contenuto della flag.

## Avviare il server:
```bash
docker pull ghcr.io/ax3lt/xss-ch3
docker run -p 80:80 ghcr.io/ax3lt/xss-ch3
```

[//]: # (- Esempio di payload: `1" onerror="fetch&#40;'/flag'&#41;.then&#40;response => response.text&#40;&#41;&#41;.then&#40;flag => { fetch&#40;'/' + encodeURIComponent&#40;flag&#41;&#41;; }&#41;;"`)

Buona fortuna! 🚀🔓
