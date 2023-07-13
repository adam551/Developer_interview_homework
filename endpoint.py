from flask import Flask, request
from datetime import date
import json

def process_json(input_dict):
	json_list = []
	for i in range(len(input_dict['entry'])):
		code_list = []
		measurement_value_list = []
		measurement_unit_list = []
		data = {}
		try:
			data['observationId'] = input_dict['entry'][i]['resource']['id']
		except:
			data['observationId'] = "ObservationIdNotFound"
		try:
			patientId = str(input_dict['entry'][i]['resource']['subject']['reference']).split('/')[1]
		except:
			patientId = "PatientIdNotFound"
		data['patientId'] = patientId
		try:
			performerId = str(input_dict['entry'][i]['resource']['performer'][0]['reference']).split('/')[1]
		except:
			performerId = "PerformerNotFound"
		data['performerId'] = performerId

		try:
			for j in range(len(input_dict['entry'][i]['resource']['code']['coding'])):
				if input_dict['entry'][i]['resource']['code']['coding'][j]['system'].find("http://loinc.org") >= 0:
					code_list.append(input_dict['entry'][i]['resource']['code']['coding'][j])
			data['measuerementCoding'] = code_list
		except:
			data['measuerementCoding'] = "MeasurementCodingNotFound"

		try:
			for j in range(len(input_dict['entry'][i]['resource']['component'])):
				for k in range(len(input_dict['entry'][i]['resource']['component'][j]['code']['coding'])):
					if input_dict['entry'][i]['resource']['component'][j]['code']['coding'][0]['system'].find("http://loinc.org") >= 0:
						for l in range(len(input_dict['entry'][i]['resource']['component'])):
							measurement_value_list.append(input_dict['entry'][i]['resource']['component'][l]['valueQuantity']['value'])
							measurement_unit_list.append(input_dict['entry'][i]['resource']['component'][l]['valueQuantity']['unit'])
			data['measurementValue'] = measurement_value_list
			data['measurementUnit'] = measurement_unit_list
		except:
			data['measurementValue'] = "ValueNotFound"
			data['measurementUnit'] = "UnitNotFound"

		try:
			data['measurementDate'] = str(input_dict['entry'][i]['resource']['effectiveDateTime']).split('T')[0]
		except:
			data['measurementDate'] = "DateNotFound"
		data['dataFetched'] = str(date.today())
		json_list.append(data)

	output_dict = json.dumps(json_list)
	return output_dict


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def upload_json():
    return process_json(request.get_json())
     

if __name__ == '__main__':
    app.run()
    