from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import random
import base64

DatasetFiles=["http://speech.savba.sk/DiCris/Speech/DiCris_MR_0080.wav",
				"http://speech.savba.sk/DiCris/Speech/DiCris_MR_0102.wav",
				"http://speech.savba.sk/DiCris/Speech/DiCris_MR_0281.wav",
				"http://speech.savba.sk/DiCris/Speech/DiCris_MT_0175.wav",
				"http://speech.savba.sk/DiCris/Speech/DiCris_MT_0309.wav",
				"http://speech.savba.sk/DiCris/Speech/DiCris_MT_0340.wav",
				"http://speech.savba.sk/DiCris/Speech/DiCris_RS_0114.wav",
				"http://speech.savba.sk/DiCris/Speech/DiCris_RS_0276.wav",
				"http://speech.savba.sk/DiCris/Speech/DiCris_RS_0358.wav",
				"http://speech.savba.sk/DiCris/Speech/DiCris_VK_0266.wav",
				"http://speech.savba.sk/DiCris/Speech/DiCris_VK_0342.wav",
				"http://speech.savba.sk/DiCris/Speech/DiCris_VK_0369.wav"
			]


class SpeechDatasetPiece(BasePiece):

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
