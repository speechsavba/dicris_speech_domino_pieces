import requests
from domino.base_piece import BasePiece
from .models import InputModel, OutputModel


class SpeechPortalApiPiece(BasePiece):
	"""
	Domino piece that sends a model name + status to a Portal API endpoint.
	POSTs to {portal_url}/models with the JSON body:
		{"name": "<model_name>", "status": "<status>"}
	"""

	def piece_function(self, input_data: InputModel):
	
		status = 'undefined'
		#TEXT STRESS #NORMAL CAUTION ALERT
		if input_data.textstresslevel=='NORMAL' and input_data.voicestresslevel < 0.5 :
			status = 'ok'
		elif input_data.textstresslevel=='NORMAL' and input_data.voicestresslevel < 0.65:
			status = 'moderate'
		elif input_data.textstresslevel=='CAUTION':
			status = 'warning'
		elif input_data.textstresslevel=='ALERT':
			status = 'critical'
		elif input_data.voicestresslevel < 0.8:
			status = 'warning'
		else:
			status = 'critical'

		print(status)
		url = f"{input_data.portal_url.rstrip('/')}/models"

		payload = {
			"name": input_data.name,
			"status": status
		}

		response = requests.post(
			url,
			json=payload,  
			headers={"Content-Type": "application/json"},
			timeout=30
		)
		response.raise_for_status()
		

		returned_status = response.json()
 
		return OutputModel(returned_status=returned_status)