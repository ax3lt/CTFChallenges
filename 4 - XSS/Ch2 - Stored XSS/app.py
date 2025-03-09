from flask import Flask, jsonify, request, render_template, redirect, make_response

app = Flask(__name__)

products = [
    {"name": "Laptop", "description": "Laptop potente per il lavoro.", "price": 1200, "image": "static/laptop.bmp"},
    {"name": "Smartphone", "description": "Telefono di ultima generazione.", "price": 800, "image": "static/notverysmartphone.bmp"},
    {"name": "Auricolari", "description": "Auricolari wireless con ottimo suono.", "price": 150, "image": "static/auricolari.bmp"},
    {"name": "Mouse", "description": "Mouse ergonomico per il gaming.", "price": 50, "image": "static/🐀.bmp"},
    {"name": "Tastiera", "description": "Tastiera meccanica RGB.", "price": 100, "image": "static/keyboard.bmp"},
    {"name": "Monitor", "description": "Monitor 4K ultra HD.", "price": 400, "image": "static/screen.bmp"},
    {"name": "Stampante", "description": "Stampante multifunzione.", "price": 250, "image": "static/printer.bmp"},
    {"name": "Hard Disk", "description": "Hard disk esterno 1TB.", "price": 90, "image": "static/dss.bmp"},
    {"name": "Smartwatch", "description": "Orologio intelligente con notifiche.", "price": 200, "image": "static/watch.bmp"},
    {"name": "Router", "description": "Router Wi-Fi ultraveloce.", "price": 130, "image": "static/router.bmp"},
]

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    image = request.form['image']
    products.append({"name": name, "description": description, "price": price, "image": image})
    return redirect('/')

@app.route('/set-admin')
def set_admin():
    resp = make_response(redirect('/'))
    resp.set_cookie('admin', 'flag{you_changed_my_website??}', max_age=3600)  # Valido per 1 ora
    return resp

@app.route('/')
def index():
    print(products)
    query = request.args.get('q', '')
    if query:
        results = [p for p in products if query in p['name'].lower() or query in p['description'].lower()]
    else:
        results = products
    return render_template('index.html', products=results, query=query)

if __name__ == '__main__':
    app.run(debug=False)
