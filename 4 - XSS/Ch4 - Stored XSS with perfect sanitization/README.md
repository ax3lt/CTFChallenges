# Challenge 4 - Stored XSS con Sanitizzazione Lato Client

Questa challenge si concentra sul pericolo di implementare controlli di sicurezza **solo lato client**, dimostrando come questi possano essere facilmente bypassati.

## Descrizione
L'applicazione è un forum che permette agli utenti di postare commenti con stile personalizzato (colore del testo) e immagini.

A differenza di challenge precedenti, questa applicazione implementa una protezione **avanzata** lato client utilizzando **DOMPurify**, una libreria molto efficace per la sanitizzazione dell'input. Tuttavia, non c'è alcuna sanitizzazione lato server.

## Obiettivo
- Sfruttare la vulnerabilità causata dall'assenza di controlli lato server
- Bypassare la protezione client tramite strumenti di intercettazione come Burp Suite
- Eseguire un attacco XSS Stored per ottenere la flag dall'admin

## Il Problema

Il forum implementa una perfetta sanitizzazione lato client usando DOMPurify, una delle librerie più efficaci per prevenire XSS. Tuttavia, l'applicazione commette un errore critico:

**Non implementa alcuna protezione lato server.**

Questo significa che, sebbene il form sul browser sanitizzi perfettamente l'input prima dell'invio, un attaccante può intercettare e modificare la richiesta HTTP dopo la sanitizzazione, inserendo codice JavaScript dannoso che verrà eseguito quando visualizzato da altri utenti.

## Come Bypassare la Protezione

1. Utilizza uno strumento come Burp Suite per intercettare la richiesta HTTP
2. Modifica i parametri della richiesta POST dopo che sono stati sanitizzati dal client
3. Inserisci il payload XSS direttamente nella richiesta modificata
4. Il server accetterà il payload senza alcuna sanitizzazione

## Esempio di Attacco

1. Registra un account sul forum
2. Configura Burp Suite (o un altro proxy) per intercettare le richieste
3. Scrivi un commento e invialo mentre intercetti la richiesta

## Cosa Imparare
Questa challenge dimostra:
- L'importanza della "difesa in profondità" - non affidare mai la sicurezza solo alle protezioni client
- Come gli attaccanti possono bypassare facilmente i controlli client
- Perché è fondamentale implementare controlli di sicurezza lato server

## Avvio del Server
```bash
docker build -t xss-ch4 .
docker run -p 5000:5555 xss-ch4
```

Buona fortuna! 