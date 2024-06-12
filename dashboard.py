'''
By: George Moraites
Date: 06/11/2024
Description: This project was made as a personal
project to consolidate stock information into a
personal dashboard.
'''

from flask import Flask, jsonify, request
import os
import requests

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'