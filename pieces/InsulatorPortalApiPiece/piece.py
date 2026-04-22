import requests
from domino.base_piece import BasePiece
from .models import InputModel, OutputModel


class InsulatorPortalApiPiece(BasePiece):
	"""
	Domino piece that sends a model name + status to a Portal API endpoint.
	POSTs to {portal_url}/models with the JSON body:
		{"name": "<model_name>", "status": "<status>"}
	"""

	def piece_function(self, input_data: InputModel):
	
		status = 'undefined'
		if input_data.contamination<1:
			status='ok'
		elif input_data.contamination<2:
			status='moderate'
		elif input_data.contamination<3:
			status='warning'
		else:
			status='critical'
			
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