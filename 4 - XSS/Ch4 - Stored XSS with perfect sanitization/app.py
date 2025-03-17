from flask import Flask, render_template, request, redirect, session, url_for, flash
from threading import Thread
import time
import requests
import os
import sys
from flask.sessions import SecureCookieSessionInterface

app = Flask(__name__)
app.secret_key = "SUPER_SECRET_KEY_CH4"

# Flag per la challenge
FLAG = "CTF{client_side_bypass}"

# In-memory "database" per gli utenti:
users = {
    "admin": {"password": "adminpass"},
}

comments = []

#############################################
# Generazione anticipata del cookie di sessione per admin
def generate_admin_session_cookie(app):
    """
    Genera e restituisce un cookie di sessione firmato per l'utente admin.
    """
    session_data = {"username": "admin"}
    serializer = SecureCookieSessionInterface().get_signing_serializer(app)
    return serializer.dumps(session_data)

# Il cookie di sessione per l'admin viene generato una sola volta e salvato in una variabile globale.
ADMIN_SESSION_COOKIE = generate_admin_session_cookie(app)
#############################################

@app.route('/')
def index():
    return render_template('index.html')

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

    return render_template('profile.html', username=username, comments=comments)

@app.route('/addcomment', methods=['POST'])
def addcomment():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    # Nessuna sanitizzazione lato server! Prende direttamente i valori inviati
    comment = request.form['content']
    color = request.form['color']
    image = request.form['image']

    print(comment, color, image, file=sys.stdout, flush=True)
    
    # Aggiunge il commento così com'è, senza controlli
    comments.append((username, comment, color, image))
    return redirect(url_for('profile'))

@app.route('/flag', methods=['GET'])
def flag():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    if username == "admin":
        return FLAG
    return "Non sei autorizzato a visualizzare questa pagina."

@app.route('/set-admin', methods=['GET'])
def set_admin():
    session['username'] = "admin"
    return "admin cookie set"

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0') 