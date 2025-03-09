# Challenge: Whitebox SQL Injection

## Descrizione
Hai accesso al codice sorgente di questa applicazione web e hai trovato qualcosa di interessante:  
le query SQL sono costruite **concatenando direttamente i dati dell'utente**, il che le rende vulnerabili a **SQL Injection**! 😈

L'obiettivo? Ottenere l'accesso come **admin** per visualizzare la flag nascosta nella pagina `/profile`.

## Obiettivo
- **Trova un modo per bypassare il login senza conoscere la password dell'admin.**
- **Ottieni accesso alla pagina del profilo come admin.**
- **Recupera la flag segreta.**

## Suggerimenti
- Il codice di login utilizza la query SQL:
```sql
  SELECT * FROM users WHERE username='%s' AND password='%s'
```
Puoi modificarla sfruttando una SQL Injection?
- Prova ad inserire caratteri speciali nel campo username o password.
- Ricorda che in alcuni database o configurazioni ' OR '1'='1 può sempre restituire un utente valido.

Buona fortuna! 🕵️‍♂️🔥