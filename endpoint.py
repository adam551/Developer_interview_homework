from flask import Flask, request
from flask_restful import Resource, Api
import json

def process_json(input_dict):
	print("-----------------------------" + str(type(input_dict)))
	print("________________" + input_dict["resourceType"])
	for entry in input_dict["entry"]:
		print(str(type(entry)))
		for detail in entry["resource"]:
			print(str(type(detail)) + "\n")
			#print(detail["id"])
			#for subdetail in detail["id"]:
			#	print(subdetail)
		input()
    


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def upload_json():
    data = process_json(request.get_json())
    return "data"
     

if __name__ == '__main__':
    app.run()
    