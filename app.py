# Library imports
from distutils.log import error
from tracemalloc import stop
from urllib import response
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
import appFunctions
from qr import qr
from processData import processData

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# SQLDB init
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB
mysql = MySQL(app)




# Test
@app.route("/", methods = ["GET"])
def index():
    res = function.getIndex()
    return res

# Allowed Files Check
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Not sure if needed, will not turn it into a module.


# Register User
@app.route("/register", methods = ['POST'])
def register():
    # Retrieve data
    username = request.form["username"]
    password = generate_password_hash(request.form["password"], "sha256")
    email = request.form["email"]
    # Validation of email with regex.py
    res = function.registerUser(username, password, email)
    return res
    
# Login User
@app.route("/login", methods = ['POST'])
def login():
    # Retrieve data
    password = request.form["password"]
    email = request.form["email"]

    # Validation of email with regex.py
    res = function.loginUser(email, password)
    return res

# Create Link
@app.route("/create", methods = ['POST'])
def createLink():
    # Retrieve data
    original = request.form["original"]
    alias = request.form["alias"]
    username = request.form["username"]
    tag = request.form["tag"]
    if tag == "":
        tag = []
    res = function.aliasCreation(original, alias, username, tag)
    return res

# Bulk Create Link

# Dont know what this means, will migrate once i understand

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
    res = function.aliasDeletion(alias, username)
    return res
    
# Update Link
@app.route("/update", methods = ['PUT'])
def putLink():
    alias = request.form["alias"]
    username = request.form["username"]
    newAlias = request.form["newAlias"]
    newOriginal = request.form["newOriginal"]
    tag = request.form["tag"]
    res = function.aliasUpdate(alias, username, newAlias, newOriginal, tag)
    return res

# Get Link
@app.route("/<username>/<alias>")
def get(username, alias):
    res = function.retrievingOriginalLink(username,alias)
    return res
    # Retrieve data

# Get all links from a user
@app.route("/<username>")
def userLinks(username):
    res = function.getAllLinks(username)
    return res

# Get Stats
@app.route("/<username>/<alias>/stats")
def stats(username, alias):
    res = function.getStats(username, alias)
    return res

# Get All Stats
@app.route("/<username>/stats")
def allStats(username):
    res = function.getAllStats(username)
    return res
    
# Get Detailed Stats
@app.route("/<username>/<alias>/stats/detailed")
def detailedStats(username, alias):
    res = function.getDetailedStats(username, alias)
    return res

# Generate QR Code
@app.route("/<username>/<alias>/qr/<filetype>")
def qrGeneration(username, alias, filetype):
    res = function.generateQRCode(username, alias, filetype)
    return res