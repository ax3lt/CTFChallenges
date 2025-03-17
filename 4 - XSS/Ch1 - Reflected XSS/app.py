from flask import Flask, jsonify, request, render_template, make_response

app = Flask(__name__)

FLAG = "CTF{XSS_Reflected}"

products = [
    {"name": "Laptop", "description": "Laptop potente per il lavoro.", "price": 1200},
    {"name": "Smartphone", "description": "Telefono di ultima generazione.", "price": 800},
    {"name": "Auricolari", "description": "Auricolari wireless con ottimo suono.", "price": 150},
    {"name": "Mouse", "description": "Mouse ergonomico per il gaming.", "price": 50},
    {"name": "Tastiera", "description": "Tastiera meccanica RGB.", "price": 100},
    {"name": "Monitor", "description": "Monitor 4K ultra HD.", "price": 400},
    {"name": "Stampante", "description": "Stampante multifunzione.", "price": 250},
    {"name": "Hard Disk", "description": "Hard disk esterno 1TB.", "price": 90},
    {"name": "Smartwatch", "description": "Orologio intelligente con notifiche.", "price": 200},
    {"name": "Router", "description": "Router Wi-Fi ultraveloce.", "price": 130}
]

@app.route('/')
def index():
    query = request.args.get('q', '')
    if query:
        results = [p for p in products if query in p['name'].lower() or query in p['description'].lower()]
    else:
        results = products
    
    response = make_response(render_template('index.html', products=results, query=query))
    response.set_cookie('flag', FLAG, httponly=False, secure=False, samesite='Lax')
    return response

if __name__ == '__main__':
    app.run(debug=False)
