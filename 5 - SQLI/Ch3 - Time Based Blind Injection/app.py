from flask import Flask, render_template, request, redirect, flash, make_response
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Parametri di connessione al DB
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "root")
DB_NAME = os.environ.get("DB_NAME", "ctf")

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            # Query parametrizzata (login sicuro)
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user:
                response = make_response(redirect('/profile'))
                # Imposta il cookie 'uid' con l'ID dell'utente
                response.set_cookie("uid", str(user['id']))
                return response
            else:
                flash("Credenziali errate. Riprova!", "danger")
        except Exception as e:
            flash("Errore nel login.", "danger")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Query vulnerabile (non il focus della challenge, ma volutamente non parametrizzata)
            query = "INSERT INTO users (username, password) VALUES ('%s', '%s')" % (username, password)
            cursor.execute(query)
            conn.commit()
            cursor.close()
            conn.close()
            flash("Registrazione completata!", "success")
            return redirect('/login')
        except Exception as e:
            flash("Errore nella registrazione.", "danger")
    return render_template('register.html')

@app.route('/profile')
def profile():
    uid = request.cookies.get('uid')
    if not uid:
        flash("Effettua il login.", "danger")
        return redirect('/login')
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT username FROM users WHERE id = " + uid
        # stdout
        print(query, file=open('/dev/stdout', 'w'))
        cursor.execute(query)
        user = cursor.fetchone()
        cursor.close()
        conn.close()
    except Exception as e:
        flash("Errore nella query.", "danger")
        return redirect('/login')
    if user:
        return render_template('profile.html', username=user['username'])
    else:
        flash("Utente non trovato.", "danger")
        return redirect('/login')

@app.route('/logout')
def logout():
    response = make_response(redirect('/login'))
    response.set_cookie("uid", "", expires=0)
    flash("Logout effettuato.", "info")
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
