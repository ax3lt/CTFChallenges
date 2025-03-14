from flask import Flask, render_template, request, redirect, session, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "SOME_SECRET_KEY"

users = {
    "admin": {"password": "adminpass", "balance": 999999999999999999999},
}

global admin_html
admin_html = None

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users:
            flash("Username già esistente!")
            return redirect(url_for('register'))
        users[username] = {"password": password, "balance": 0}
        flash("Registrazione avvenuta con successo. Ora effettua il login!")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username]["password"] == password:
            session['username'] = username
            flash("Login effettuato!")
            return redirect(url_for('profile'))
        else:
            flash("Credenziali errate.")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logout effettuato.")
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    balance = users[username]['balance']
    flag = ''

    if balance > 0:
        flag = "Woah! Ma come hai fatto? Vabbè, ecco la flag: FLAG{CSRF_VULNERABILITY_SUCCESS}"

    return render_template('profile.html', username=username, balance=balance, flag=flag)

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    username = session.get('username')
    if username is not None and username != 'admin':
        return "Solo l'admin può effettuare trasferimenti!", 403

    target_account = request.values.get("accountName")
    try:
        amount = int(request.values.get("amount", "0"))
    except ValueError:
        return "Importo non valido", 400

    if target_account in users:
        users[target_account]['balance'] += amount
    else:
        users[target_account] = {"password": "", "balance": amount}

    global admin_html
    admin_html = None
    return "Transfer effettuato!"

@app.route('/contact', methods=['POST'])
def contact():
    html_content = request.form.get("message")
    global admin_html
    admin_html = html_content
    print(f"HTML inviato: {html_content}")
    print(f"Admin virtuale visiterà la pagina con questo HTML: {admin_html}")
    return "Messaggio inviato! L'admin virtuale visiterà la pagina ogni 10 secondi."

@app.route('/admin-view')
def admin_view():
    global admin_html
    if admin_html:
        return admin_html
    return "Nessun messaggio da visualizzare"

if __name__ == '__main__':
    app.run(debug=False, port=80, host='0.0.0.0')
