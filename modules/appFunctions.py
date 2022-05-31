
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
from modules.regexValidator import validatePassword


# Import from other python files
sys.path.append('./modules')
from qr import qr
from processData import processData
from regexValidator import validateEmail
import DBconnection

mysql, app = DBconnection.connectDB()

# Function to get webpage
def getIndex():
    print("Connection success!")
    return "Connection Success!"


# <--------------------------------------- User Related --------------------------------------->


# Function to register a User after verifying the email is of a proper type
def registerUser(username, password, email):
    if validateEmail(email) == True:
        if validatePassword(password) == False:
            try:
                # Fetch data from SQL database
                cur = mysql.connection.cursor()
                res = cur.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
                mysql.connection.commit()
                cur.close()
                return "User added!"
            except Exception as err:
                return("Something went wrong: {}".format(err))
        else:
            return "Please enter a stronger password"
    else:
        return "Please enter a proper email"
        # Reset the page

# Function to login 
def loginUser(email, password):
    if validateEmail(email) == True:

        # Fetch data from SQL database
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
            return "Password or email does not exist"
    else:
        return "Please enter a valid email address"
        # Reset the page


# <--------------------------------------- Alias Related --------------------------------------->


# Function to create the shortened link and store it into the workbench
def aliasCreation(original, alias, username, tag):
    try:
        cur = mysql.connection.cursor()
        res = cur.execute("INSERT INTO urls (original, alias, username, tag) VALUES (%s, %s, %s, %s)", (original, alias, username, str(tag)))
        mysql.connection.commit()
        cur.close()
        print(res)
        return f"localhost:5000/{username}/{alias}"
    except Exception as err:
        return("Something went wrong: {}".format(err))

# Function to delete the shortened link from the database
def aliasDeletion(alias, username):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM urls WHERE alias = %s and username =  %s", (alias, username))
        mysql.connection.commit()
        cur.close()
        return "Link deleted!"
    except Exception as err:
        return("Something went wrong: {}".format(err))

# Function to update the shortened link in the database
def aliasUpdate(alias, username, newAlias, newOriginal, tag):
    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE urls SET alias = %s, original = %s, tag = %s WHERE alias = %s and username = %s", (newAlias, newOriginal, str(tag), alias, username))
        mysql.connection.commit()
        cur.close()

        return "Link updated!"
    except Exception as err:
        return("Something went wrong: {}".format(err))

# Function to Get original link when the shortened link is used
def retrievingOriginalLink(username, alias):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM urls WHERE alias = %s AND username = %s", (alias, username))
        res = cur.fetchone()
        cur.execute("UPDATE urls SET clicks = clicks + 1 WHERE alias = %s AND username = %s", (alias, username))
        mysql.connection.commit()
        cur.close()

        try:
            # Create timestamp
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            agent = httpagentparser.detect(request.headers.get('User-Agent'))
            os = agent["platform"]["name"]
            browser = agent["browser"]["name"]
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

# Function to Get all links that a user owns
def getAllLinks(username):
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


# <--------------------------------------- Stats Related --------------------------------------->


# Function that retrieve individual user stats from Mongo DB
def getStats(username, alias):
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

# Function that Retrieve all stats from the user
def getAllStats(username):
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

# Function that Retrieve detailed stats from Mongo DB
def getDetailedStats(username, alias):
    try:
       # Retrieve data
       data = clicks.find({"username": username, "alias": alias})
       arr = []
       for i in data:
           arr.append(i)
       return dumps(arr)

    except Exception as err:
        return("Something went wrong: {}".format(err))

# <--------------------------------------- QR Code Related --------------------------------------->

# Generation of the QR Code
def generateQRCode(username, alias, filetype):
    try:
    # Generate QR Code
        filename= qr("localhost:5000/{}/{}".format(username, alias), filetype)
        
        return send_file(filename, mimetype=f"image/{filetype}")

    except Exception as err:
        return("Something went wrong: {}".format(err))