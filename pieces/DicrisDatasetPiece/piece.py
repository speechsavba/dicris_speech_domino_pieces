from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import random
import base64

class DicrisDatasetPiece(BasePiece):

	def piece_function(self, input_data: InputModel):
		dataset_file = input_data.dataset
		if dataset_file=='random':
			
			wav1 = "http://speech.savba.sk/DiCris/echo_20250716_113400_7B-3.wav"
			wav2 = "http://speech.savba.sk/DiCris/echo_20250715_094400_7B-0.wav"
			wav3 = "http://speech.savba.sk/DiCris/echo_20250716_104301_D5.wav"
			dset=[wav1,wav2,wav3] 
			dataset_file=random.choice(dset)
			self.logger.info(f'Randomly chosed:\n{dataset_file}')

		else:
			self.logger.info(f'Providing:\n{dataset_file}')

		raw_content = f"File:\n{dataset_file}\n"
		base64_content = base64.b64encode(raw_content.encode("utf-8")).decode("utf-8")
		self.display_result = {
			"file_type": "txt",
			"base64_content": base64_content
		}		
		return OutputModel(file_path=dataset_file)
