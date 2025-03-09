# Challenge: CSRF Exploit - Admin Session Hijack

## Descrizione
In questa challenge, sei entrato in un sito web con un sistema di trasferimento di denaro molto insicuro.  
L'amministratore del sito ha una quantità illimitata di denaro e visita periodicamente i link inviati dagli utenti attraverso un form di contatto.  
Purtroppo, il sito non implementa protezioni contro attacchi **CSRF (Cross-Site Request Forgery)**.  
Sarà possibile sfruttare questa vulnerabilità per far sì che l'admin trasferisca del denaro nel tuo account?

## Obiettivo
- **Sfrutta una vulnerabilità CSRF** per far sì che l'admin trasferisca denaro sul tuo account.
- **Ottieni almeno 1$ di saldo** nel tuo profilo per ricevere la **FLAG**.

## Suggerimenti
- Il sito non usa un token CSRF per proteggere il form di trasferimento.
- L'admin visita automaticamente i link che gli invii attraverso il form "contact".
- Ispeziona il form di trasferimento e scopri come inviare una richiesta di trasferimento di denaro.