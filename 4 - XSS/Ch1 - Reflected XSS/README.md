# Challenge: XSS Exploit - Online Store Search Injection

## Descrizione
In questa challenge, hai accesso a un negozio online che permette di cercare prodotti attraverso un campo di ricerca.  
Tuttavia, il sito non implementa correttamente la **sanitizzazione degli input**, rendendolo vulnerabile a un attacco **XSS (Cross-Site Scripting)**.  
Sfruttando questa vulnerabilità, potresti eseguire codice JavaScript arbitrario all'interno del browser delle vittime.

Sarà possibile iniettare uno script dannoso e rubare informazioni sensibili?

## Obiettivo
- **Sfrutta la vulnerabilità XSS** per eseguire codice JavaScript all'interno del sito.
- **Dimostra l'exploit** eseguendo un alert con `document.cookie` o rubando i cookie della sessione.

## Suggerimenti
- Il valore della ricerca viene inserito direttamente nel DOM senza protezione.
- Prova a iniettare un payload come `<script>alert('XSS!')</script>`.
- Potresti anche provare payload più avanzati per esfiltrare dati sensibili.

Buona fortuna! 🚀🔓
