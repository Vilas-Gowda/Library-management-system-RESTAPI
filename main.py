from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
import sqlite3

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()