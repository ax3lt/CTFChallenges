# Challenge: SSRF Exploit - Admin Panel Access

## Descrizione
In questa challenge, hai accesso a un sito che permette di visualizzare file remoti tramite URL.  
Tuttavia, l'amministratore del sito possiede un pannello privato che gira sulla porta **81** e contiene una flag.  
Il sistema non implementa protezioni contro attacchi **SSRF (Server-Side Request Forgery)**, permettendo di forzare il server a effettuare richieste arbitrarie.

Sarà possibile sfruttare questa vulnerabilità per accedere al pannello admin e ottenere la flag?

## Obiettivo
- **Sfrutta la vulnerabilità SSRF** per forzare il server a effettuare una richiesta HTTP a `http://127.0.0.1:81/flag`.
- **Ottieni la FLAG** leggendo il contenuto della risposta.

## Suggerimenti
- Il form accetta URL arbitrari e il server esegue richieste senza restrizioni.
- Se il sistema non blocca richieste interne, dovresti vedere il contenuto della flag nella risposta.

## Avviare il server:
```bash
docker pull ghcr.io/ax3lt/ssrf-ch1
docker run -p 80:80 ghcr.io/ax3lt/ssrf-ch1
```

Buona fortuna! 🚀🔓
