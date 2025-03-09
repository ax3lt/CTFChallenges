from flask import Flask, render_template, request, redirect, session, url_for, flash
from threading import Thread
import time
import requests
import os
from flask.sessions import SecureCookieSessionInterface

app = Flask(__name__)
app.secret_key = "SOME_SECRET_KEY"

users = {
    "admin": {"password": "adminpass", "balance": 999999999999999999999},
}

global admin_link
admin_link = None

#############################################
def generate_admin_session_cookie(app):
    """
    Genera e restituisce un cookie di sessione firmato per l'utente admin.
    """
    session_data = {"username": "admin"}
    serializer = SecureCookieSessionInterface().get_signing_serializer(app)
    return serializer.dumps(session_data)

ADMIN_SESSION_COOKIE = generate_admin_session_cookie(app)
#############################################

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
            if username == "admin":
                return redirect(url_for('admin_dashboard'))
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
    if username is not None:
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

    global admin_link
    admin_link = None
    return "Transfer effettuato!"

@app.route('/contact', methods=['POST'])
def contact():
    message = request.form.get("message")
    global admin_link
    admin_link = message
    print(f"Link inviato: {message}")
    print(f"Admin virtuale visiterà il link: {admin_link}")
    return "Messaggio inviato! L'admin virtuale visiterà il link ogni 10 secondi."

def admin_auto_visit():
    s = requests.Session()
    s.cookies.set("session", ADMIN_SESSION_COOKIE, domain="localhost")
    print("Cookie di sessione admin hard-coded impostato.")

    global admin_link
    while True:
        if admin_link:
            try:
                url = 'http://localhost:80' + admin_link
                resp = s.get(url)
                print(f"Admin virtuale ha visitato: {url} (Status: {resp.status_code})")
            except Exception as e:
                print(f"Errore visitando il link admin: {e}")
        time.sleep(2)

if __name__ == '__main__':
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        thread = Thread(target=admin_auto_visit, daemon=True)
        thread.start()
    app.run(debug=False, port=80, host='0.0.0.0')
