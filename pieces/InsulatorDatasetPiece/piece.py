from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import random
import base64

DatasetFiles=["http://speech.savba.sk/DiCris/Insulator/echo_20250716_113400_7B-3.wav",
			"http://speech.savba.sk/DiCris/Insulator/echo_20250715_094400_7B-0.wav",
			"http://speech.savba.sk/DiCris/Insulator/echo_20250716_104301_D5.wav",
			"http://speech.savba.sk/DiCris/Insulator/echo_20250715_103400_7B.wav"
			]


class InsulatorDatasetPiece(BasePiece):

	def piece_function(self, input_data: InputModel):
		global DatasetFiles
		#dataset_file = input_data.dataset
		#if dataset_file=='random':
		dataset_file=random.choice(DatasetFiles)
		self.logger.info(f'Randomly chosed:\n{dataset_file}')

		raw_content = f"File:\n{dataset_file}\n"
		base64_content = base64.b64encode(raw_content.encode("utf-8")).decode("utf-8")
		self.display_result = {
			"file_type": "txt",
			"base64_content": base64_content
		}		
		return OutputModel(file_path=dataset_file)
