import mysql.connector
import os

os.system("mysql -u root -e 'ALTER USER \"root\"@\"localhost\" IDENTIFIED VIA mysql_native_password USING PASSWORD(\"root\");'")
os.system("mysql -u root -proot -e 'FLUSH PRIVILEGES;'")

DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "root")
DB_NAME = os.environ.get("DB_NAME", "ctf")

conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
conn.autocommit = True
cursor = conn.cursor(buffered=True)

cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
cursor.execute(f"USE {DB_NAME}")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL
)
""")

cursor.execute("SELECT * FROM users WHERE username='admin'")
if cursor.fetchone() is None:
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', '73812hjkfdsnkfmhdjgsak')")
    print("Utente admin creato con username 'admin' e password '********'")

cursor.execute("""
CREATE TABLE IF NOT EXISTS flagrandomwordss (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mypersonalflag VARCHAR(255) NOT NULL
)
""")
cursor.execute("SELECT * FROM flagrandomwordss")
if cursor.fetchone() is None:
    cursor.execute("INSERT INTO flagrandomwordss (mypersonalflag) VALUES ('flag{Union_Injection_Yeah}')")
    print("Flag inserita nella tabella flag.")

cursor.close()
conn.close()
