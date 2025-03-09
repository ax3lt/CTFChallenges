from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

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
    if 'username' in session:
        return redirect('/profile')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE username='%s' AND password='%s'" % (username, password)
            cursor.execute(query)
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user:
                session['username'] = user['username']
                flash("Benvenuto, hacker! Hai fatto un bel bypass... o quasi!", "success")
                return redirect('/profile')
            else:
                flash("Credenziali errate. Controlla bene la query ;)", "danger")
        except Exception as e:
            flash(f"Errore nella query: <br><code>{query}</code><br>Dettagli: {str(e)}</code>", "danger")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO users (username, password) VALUES ('%s', '%s')" % (username, password)
            cursor.execute(query)
            conn.commit()
            cursor.close()
            conn.close()
            flash("Registrazione completata!", "success")
            return redirect('/login')
        except Exception as e:
            flash(f"Errore nella query: <br><code>{query}</code><br>Dettagli: {str(e)}</code>", "danger")
    return render_template('register.html')

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect('/login')
    username = session['username']
    if username.lower() == 'admin':
        flag = "flag{SQLi_Master_Hacker}"
        return render_template('profile.html', flag=flag, username=username)
    return render_template('profile.html', username=username)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logout effettuato. Non smettere mai di cercare vulnerabilità!", "info")
    return redirect('/login')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
