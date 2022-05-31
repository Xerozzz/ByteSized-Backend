from flask_mysqldb import MySQL
from flask import Flask, request, jsonify,send_file
import config

def connectDB():
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = config.MYSQL_HOST
    app.config['MYSQL_USER'] = config.MYSQL_USER
    app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
    app.config['MYSQL_DB'] = config.MYSQL_DB
    mysql = MySQL(app)
    return mysql, app
