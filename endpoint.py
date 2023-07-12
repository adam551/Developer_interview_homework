from flask import Flask, request
from flask_restful import Resource, Api
import json
import os

def process_json(input_string):
	print("-----------------------------" + str(type(input_string)))
	print("________________" + input_string["resourceType"])
    

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def upload_json():
    data = process_json(request.get_json())
    return "data"
     

if __name__ == '__main__':
    app.run()
    