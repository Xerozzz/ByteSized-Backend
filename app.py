# Library imports
from flask import Flask, request, jsonify,send_file
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

# Import from other python files
import config
from qr import qr

app = Flask(__name__)

# DB init
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB
mysql = MySQL(app)

# Test
@app.route("/")
def index():
    return "Connection Success!"

# Register User
@app.route("/register", methods = ['POST'])
def register():
    # Retrieve data
    username = request.form["username"]
    password = generate_password_hash(request.form["password"], "sha256")
    email = request.form["email"]

    # Insert data
    cur = mysql.connection.cursor()
    res = cur.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
    mysql.connection.commit()
    cur.close()
    return "User added!"

# Login User
@app.route("/login", methods = ['POST'])
def login():
    # Retrieve data
    password = request.form["password"]
    email = request.form["email"]

    # Retrieve data from DB
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", [email])
    res = cur.fetchone()
    cur.close()

    # Check Password
    if check_password_hash(res[3], password):
        return f"Welcome back {res[1]}!"
    else:
        return "Wrong password!"

# Create Link
@app.route("/create", methods = ['POST'])
def create():
    # Retrieve data
    original = request.form["original"]
    alias = request.form["alias"]
    username = request.form["username"]

    # Insert data
    cur = mysql.connection.cursor()
    res = cur.execute("INSERT INTO urls (original, alias, username) VALUES (%s, %s, %s)", (original, alias, username))
    mysql.connection.commit()
    cur.close()

    return f"localhost:5000/{username}/{alias}"

# Get Link
@app.route("/<username>/<alias>")
def get(username, alias):
    # Retrieve data
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM urls WHERE alias = %s AND username = %s", (alias, username))
    res = cur.fetchone()
    cur.execute("UPDATE urls SET clicks = clicks + 1 WHERE alias = %s AND username = %s", (alias, username))
    mysql.connection.commit()
    cur.close()

    # Redirect to original
    return f"{res[1]}"

# Get Stats
@app.route("/<username>/<alias>/stats")
def stats(username, alias):
    # Retrieve data
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM urls WHERE alias = %s AND username = %s", (alias, username))
    res = cur.fetchone()
    cur.close()

    # Redirect to original
    return f"{res[2]}"

# Get All Stats
@app.route("/stats")
def all_stats():
    # Retrieve data
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM urls")
    row_headers = [x[0] for x in cur.description]
    res = cur.fetchall()
    cur.close()

    # Format into json
    json_data = []
    for i in res:
        json_data.append(dict(zip(row_headers, i)))

    # Redirect to original
    return jsonify(json_data)

# Generate QR Code
@app.route("/<username>/<alias>/qr")
def qr_generation(username, alias):
    # Generate QR Code
    filename = qr("localhost:5000/{}/{}".format(username, alias))
    
    return send_file(filename, mimetype='image/png')

# Get all links from a user
@app.route("/<username>")
def user_links(username):
    # Query user
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM urls WHERE username = %s", [username])
    row_headers = [x[0] for x in cur.description]
    res = cur.fetchall()
    cur.close()
    
    json_data = []
    for i in res:
        json_data.append(dict(zip(row_headers, i)))

    return jsonify(json_data)

