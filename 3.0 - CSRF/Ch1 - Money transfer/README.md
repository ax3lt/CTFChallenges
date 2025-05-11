# Challenge CSRF con HTML Injection

## Descrizione
Questa challenge illustra una vulnerabilità CSRF (Cross-Site Request Forgery) attraverso l'iniezione di codice HTML. 

L'applicazione consente agli utenti di inviare un messaggio HTML che verrà visualizzato dall'amministratore. L'obiettivo è sfruttare questa funzionalità per indurre l'amministratore a eseguire una richiesta di trasferimento fondi involontaria.

## Funzionamento
1. Registrati e accedi all'applicazione
2. Crea un messaggio HTML che contiene un form con autosubmit o una richiesta fetch per eseguire un trasferimento
3. L'admin visiterà automaticamente la pagina con il tuo codice HTML iniettato
4. Se il tuo codice è corretto, l'admin eseguirà inconsapevolmente un trasferimento di denaro verso il tuo account
5. Una volta che il tuo saldo è maggiore di zero, otterrai la flag

## Nota sulla realtà degli attacchi CSRF
In questa challenge, per semplicità, l'HTML dannoso viene inviato e visualizzato sullo stesso server della banca. Tuttavia, come visto a lezione, in un attacco CSRF reale il codice dannoso verrebbe tipicamente ospitato su un sito esterno controllato dall'attaccante. Se l'utente admin fosse già loggato sul sito della banca e visitasse questo sito esterno dannoso, il browser invierebbe automaticamente i cookie di autenticazione nella richiesta al sito della banca, permettendo all'attaccante di eseguire operazioni non autorizzate a nome dell'utente. Questa è l'essenza di un attacco CSRF: sfruttare la fiducia che un sito ha in un browser dell'utente già autenticato.

## Suggerimenti
- L'applicazione utilizza pyppeteer per simulare la navigazione dell'admin
- L'admin accede automaticamente con le credenziali "admin:adminpass"
- Puoi inserire qualsiasi codice HTML, inclusi form e script

**NOTA IMPORTANTE**: Nell'esempio sopra, "localhost:80" si riferisce all'indirizzo interno del container Docker. Il bot admin esegue all'interno del container e visita questa URL. Quando crei il tuo payload, devi sempre usare "localhost:80" e NON la porta esterna sulla quale hai mappato il container.

## Obiettivo
Ottieni la flag eseguendo un trasferimento di denaro verso il tuo account sfruttando la vulnerabilità CSRF.

## Avviare il server:
```bash
docker pull ghcr.io/ax3lt/csrf-ch1
docker run -p 80:80 ghcr.io/ax3lt/csrf-ch1
```