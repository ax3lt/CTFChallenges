from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <!DOCTYPE html>
        <html lang="it">
        <head>
            <meta charset="UTF-8">
            <title>Pannello Admin</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 2em; }
            </style>
        </head>
        <body>
            <h1>Pannello Admin</h1>
            <p>Per ottenere la flag, visita <a href="/flag">/flag</a></p>
        </body>
        </html>
    '''

@app.route('/flag')
def flag():
    return "FLAG{SSRF_VULNERABILITY_SUCCESS}"

if __name__ == '__main__':
    # Il pannello admin è disponibile solo su loopback (localhost) e sulla porta 8001.
    app.run(host='127.0.0.1', port=81, debug=False)
