from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <!DOCTYPE html>
        <html lang="it">
        <head>
            <meta charset="UTF-8">
            <title>File Previewer</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 2em; }
                pre { background: #f4f4f4; padding: 1em; }
            </style>
        </head>
        <body>
            <h1>Anteprima dei File</h1>
            <p>Inserisci l'URL del file di cui vuoi vedere l'anteprima:</p>
            <p>Il nostro admin con un potentissimo pannello privato sulla porta 81 monitora tutto!</p>
            <form action="/preview" method="GET">
                <input type="text" name="url" placeholder="http://esempio.com/file.txt" size="50" required>
                <button type="submit">Visualizza Anteprima</button>
            </form>
        </body>
        </html>
    '''

@app.route('/preview')
def preview():
    url = request.args.get('url')
    if not url:
        return "Nessun URL fornito.", 400
    try:
        r = requests.get(url, timeout=5)
        content = r.text[:10000]
        return render_template_string('''
            <!DOCTYPE html>
            <html lang="it">
            <head>
                <meta charset="UTF-8">
                <title>Anteprima File</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 2em; }
                    pre { background: #f4f4f4; padding: 1em; }
                </style>
            </head>
            <body>
                <h1>Anteprima File</h1>
                <pre>{{ content }}</pre>
                <p><a href="/">Torna alla home</a></p>
            </body>
            </html>
        ''', content=content)
    except Exception as e:
        return "Errore durante il recupero del file: " + str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
