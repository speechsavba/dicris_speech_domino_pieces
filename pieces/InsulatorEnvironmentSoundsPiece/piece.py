# -*- coding: utf-8 -*-
from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
from io import BytesIO
import numpy as np
import base64
import os,sys
from pathlib import Path
import librosa
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
import requests
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add it to sys.path if needed
sys.path.append(current_dir)

from calc_yamnet import identify_with_yamnet

class InsulatorEnvironmentSoundsPiece(BasePiece):

	def piece_function(self, input_data: InputModel):
		self.logger.info(f"InsulatorEnvironmentSoundsPiece START")
		sr = input_data.sr
		# Try to open image from file path or base64 encoded string
		y = input_data.y

		max_path_size = 4096#int(os.pathconf('/', 'PC_PATH_MAX'))
		if len(y) < max_path_size:
			if y.startswith('http'):
				self.logger.info("Y seems to be URL, loading with requests and librosa")
				y,sr=self.get_url_data(y)
			elif  Path(y).exists() and Path(y).is_file():
				self.logger.info("Y is a file path, loading with librosa")
				if sr<=0:
					sr=None
				y, sr = librosa.load(y, sr=sr)

		else:
			self.logger.info("Y is not a file path, trying to decode as base64 string")
			try:
				decoded_bytes = base64.b64decode(y)
				y = np.frombuffer(decoded_bytes, dtype=np.float32)
			except Exception:
				raise ValueError("Y is not a file path or a base64 encoded string")

		y_16k = librosa.resample(y, orig_sr=sr, target_sr=16000)
		y_np = y_16k.astype(np.float32)
		self.logger.info(f"InsulatorEnvironmentSoundsPiece IDENTIFICATION START")

		infered_class,infered_prob,top10=identify_with_yamnet(y_np)

		self.logger.info(f"InsulatorEnvironmentSoundsPiece IDENTIFICATION END")

		self.logger.info(f'Prediction TOP {infered_class} with prob: {infered_prob}')
		self.logger.info(f'Prediction TOP10 {top10}')

		raw_content = f"Prediction TOP10 is: {top10}\n"
		base64_content = base64.b64encode(raw_content.encode("utf-8")).decode("utf-8")
		self.display_result = {
			"file_type": "txt",
			"base64_content": base64_content
		}

		# Return output
		return OutputModel(
			top_class=infered_class,
			top_prob=infered_prob,
			top10=top10
		)



	def get_url_data(self,url):
		try:
			headers = {}
			body_data = None
			response = requests.get(url, headers=headers)
			response.raise_for_status()

		except requests.RequestException as e:
			raise Exception(f"HTTP request error: {e}")

		audio_bytes = BytesIO(response.content)

		y, sr = librosa.load(audio_bytes, sr=None)

		return(y,sr)


