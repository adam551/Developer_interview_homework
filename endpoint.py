from flask import Flask, request
from datetime import date
import json

#TODO
def convert_unit(value, unit):
	new_value = value
	new_unit = unit
	return [value, unit]


def process_json(input_dict):
	json_list = []
	for i in range(len(input_dict['entry'])):
		code_list = []
		measurement_value_list = []
		measurement_unit_list = []
		data = {}
		try:
			data['observationId'] = input_dict['entry'][i]['resource']['id']
            data['patientId'] = str(input_dict['entry'][i]['resource']['subject']['reference']).split('/')[1]
            data['performerId'] = str(input_dict['entry'][i]['resource']['performer'][0]['reference']).split('/')[1]
            
			for j in range(len(input_dict['entry'][i]['resource']['code']['coding'])):
				if input_dict['entry'][i]['resource']['code']['coding'][j]['system'].find("http://loinc.org") >= 0:
					code_list.append(input_dict['entry'][i]['resource']['code']['coding'][j])
			data['measuerementCoding'] = code_list
            
			for j in range(len(input_dict['entry'][i]['resource']['component'])):
				for k in range(len(input_dict['entry'][i]['resource']['component'][j]['code']['coding'])):
					if input_dict['entry'][i]['resource']['component'][j]['code']['coding'][0]['system'].find("http://loinc.org") >= 0:
						for l in range(len(input_dict['entry'][i]['resource']['component'])):
							measurement_value_list.append(input_dict['entry'][i]['resource']['component'][l]['valueQuantity']['value'])
							measurement_unit_list.append(input_dict['entry'][i]['resource']['component'][l]['valueQuantity']['unit'])
			data['measurementValue'] = measurement_value_list
			data['measurementUnit'] = measurement_unit_list

			data['measurementDate'] = str(input_dict['entry'][i]['resource']['effectiveDateTime']).split('T')[0]

            data['dataFetched'] = str(date.today())
        except:
            data = "Data " + str(i) + " Missing"
		json_list.append(data)

	output_dict = json.dumps(json_list)
	return output_dict


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def upload_json():
    return process_json(request.get_json())
     

if __name__ == '__main__':
    app.run()
    