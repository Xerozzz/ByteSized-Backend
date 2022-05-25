# Library imports
from flask import Flask, request, jsonify,send_file
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import os
import sys
import config
import json
from datetime import datetime
import httpagentparser
from bson.json_util import dumps

# Import from other python files
sys.path.append('./modules')
from qr import qr
from processData import processData

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MongoDB Atlas (need to change if using normal mongodb or other db)
mongodb_atlas = config.MONGODB_ATLAS
client = MongoClient(mongodb_atlas)
db = client.clicks
clicks = db.clicks

# SQLDB init
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB
mysql = MySQL(app)

# Test
@app.route("/")
def index():
    print("Connection success!")
    return "Connection Success!"

# Allowed Files Check
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Register User
@app.route("/register", methods = ['POST'])
def register():
    # Retrieve data
    username = request.form["username"]
    password = generate_password_hash(request.form["password"], "sha256")
    email = request.form["email"]

    # Insert data
    try:
        cur = mysql.connection.cursor()
        res = cur.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
        mysql.connection.commit()
        cur.close()
        return "User added!"
    except Exception as err:
        return("Something went wrong: {}".format(err))
    

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

    # User not found
    if res == None:
        return "User not found."

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
    tag = request.form["tag"]
    if tag == "":
        tag = []

    # Insert data
    try:
        cur = mysql.connection.cursor()
        res = cur.execute("INSERT INTO urls (original, alias, username, tag) VALUES (%s, %s, %s, %s)", (original, alias, username, str(tag)))
        mysql.connection.commit()
        cur.close()
        return f"localhost:5000/{username}/{alias}"
    except Exception as err:
        return("Something went wrong: {}".format(err))

# Bulk Create Link
@app.route("/bulkcreate", methods = ['POST'])
def bulkCreate():
    # Retrieve data
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        # Store file
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Process data
        val = processData(filename)
        
        # Insert data
        try:
            cur = mysql.connection.cursor()
            sql = "INSERT INTO urls (original, alias, username, tag) VALUES (%s, %s, %s, %s)"
            cur.executemany(sql,val)
            mysql.connection.commit()
            rows = cur.rowcount
            cur.close()

            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f"{rows} links added!"
        except Exception as err:
            return("Something went wrong: {}".format(err))

# Delete Link
@app.route("/delete", methods = ['DELETE'])
def deleteLink():
    alias = request.form["alias"]
    username = request.form["username"]

    # Delete data
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM urls WHERE alias = %s and username =  %s", (alias, username))
        mysql.connection.commit()
        cur.close()

        return "Link deleted!"
    except Exception as err:
        return("Something went wrong: {}".format(err))

# Update Link
@app.route("/update", methods = ['PUT'])
def putLink():
    alias = request.form["alias"]
    username = request.form["username"]

    newAlias = request.form["newAlias"]
    newOriginal = request.form["newOriginal"]
    tag = request.form["tag"]

    # Delete data
    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE urls SET alias = %s, original = %s, tag = %s WHERE alias = %s and username = %s", (newAlias, newOriginal, str(tag), alias, username))
        mysql.connection.commit()
        cur.close()

        return "Link updated!"
    except Exception as err:
        return("Something went wrong: {}".format(err))

# Get Link
@app.route("/<username>/<alias>")
def get(username, alias):
    # Create timestamp
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    agent = httpagentparser.detect(request.headers.get('User-Agent'))
    os = agent["platform"]["name"]
    browser = agent["browser"]["name"]

    # Retrieve data
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM urls WHERE alias = %s AND username = %s", (alias, username))
        res = cur.fetchone()
        cur.execute("UPDATE urls SET clicks = clicks + 1 WHERE alias = %s AND username = %s", (alias, username))
        mysql.connection.commit()
        cur.close()

        try:
            # Store Click in MongoDB
            clicks.insert_one({
                "username": username,
                "alias": alias,
                "datetime": time,
                "os": os,
                "browser": browser
            })

            # Redirect to original
            return f"{res[1]}"
        
        except Exception as err:
            return err

    except Exception as err:
        return("Something went wrong: {}".format(err))

# Get all links from a user
@app.route("/<username>")
def userLinks(username):
    try:
        # Query user
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM urls WHERE username = %s", [username])
        row_headers = [x[0] for x in cur.description]
        res = cur.fetchall()
        cur.close()
        
        jsonData = []
        for i in res:
            jsonData.append(dict(zip(row_headers, i)))

        return jsonify(jsonData)

    except Exception as err:
        return("Something went wrong: {}".format(err))

# Get Stats
@app.route("/<username>/<alias>/stats")
def stats(username, alias):
    try:
        # Retrieve data
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM urls WHERE alias = %s AND username = %s", (alias, username))
        res = cur.fetchone()
        cur.close()

        # Redirect to original
        return f"{res[2]}"

    except Exception as err:
        return("Something went wrong: {}".format(err))

# Get All Stats
@app.route("/<username>/stats")
def allStats(username):
    try:
        # Retrieve data
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM urls WHERE username = %s", [username])
        row_headers = [x[0] for x in cur.description]
        res = cur.fetchall()
        cur.close()

        # Format into json
        jsonData = []
        for i in res:
            jsonData.append(dict(zip(row_headers, i)))

        # Redirect to original
        return jsonify(jsonData)

    except Exception as err:
        return("Something went wrong: {}".format(err))
    
# Get Detailed Stats
@app.route("/<username>/<alias>/stats/detailed")
def detailedStats(username, alias):
    try:
        # Retrieve data
        data = clicks.find({"username": username, "alias": alias})
        arr = []
        for i in data:
            arr.append(i)

        return dumps(arr)

    except Exception as err:
        return("Something went wrong: {}".format(err))

# Generate QR Code
@app.route("/<username>/<alias>/qr/<filetype>")
def qrGeneration(username, alias, filetype):
    try:
    # Generate QR Code
        filename= qr("localhost:5000/{}/{}".format(username, alias), filetype)
        
        return send_file(filename, mimetype=f"image/{filetype}")

    except Exception as err:
        return("Something went wrong: {}".format(err))