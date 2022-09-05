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
import appFunctions as function
from qr import qr
from processData import processData
import DBconnection

mysql, app = DBconnection.connectDB()


# Test
@app.route("/index", methods = ["GET"])
def index():
    res = function.getIndex()
    return res

# Register User
@app.route("/register", methods = ['POST'])
def register():
    try:
        input_json = request.get_json(force=True) 
    except:
        input_json = request.form
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
    try:
        input_json = request.get_json(force=True) 
    except:
        input_json = request.form
    # Retrieve data
    password = request.form["password"]
    email = request.form["email"]

    # Validation of email with regex.py
    res = function.loginUser(email, password)
    return res

# Create Link
@app.route("/create", methods = ['POST'])
def createLink():
    try:
        input_json = request.get_json(force=True) 
    except:
        input_json = request.form
    # Retrieve data
    original = input_json["original"]
    alias = input_json["alias"]
    username = input_json["username"]
    tag = input_json["tag"]
    if tag == "":
        tag = []
    res = function.aliasCreation(original, alias, username, tag)
    return res

# Bulk Create Link
@app.route("/bulkcreate", methods = ['POST'])
def bulkCreate():
    try:
        input_json = request.get_json(force=True) 
    except:
        input_json = request.form
    # Retrieve data
    res = function.bulkCreateLink()
    return res

# Delete Link
@app.route("/delete", methods = ['DELETE'])
def deleteLink():
    try:
        input_json = request.get_json(force=True) 
    except:
        input_json = request.form
    alias = request.form["alias"]
    username = request.form["username"]
    res = function.aliasDeletion(alias, username)
    return res
    
# Update Link
@app.route("/update", methods = ['PUT'])
def putLink():
    try:
        input_json = request.get_json(force=True) 
    except:
        input_json = request.form
    alias = request.form["alias"]
    username = request.form["username"]
    newAlias = request.form["newAlias"]
    newOriginal = request.form["newOriginal"]
    tag = request.form["tag"]
    res = function.aliasUpdate(alias, username, newAlias, newOriginal, tag)
    return res

# Get OriginalLink
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

# All clicks
@app.route("/<username>/all_clicks")
def allClicks(username):
    res = function.getAllClicks(username)
    return res