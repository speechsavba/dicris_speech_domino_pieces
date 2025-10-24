# -*- coding: utf-8 -*-
from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
from io import BytesIO
import numpy as np
import base64
import os
from pathlib import Path
import librosa
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
import joblib
import requests


norm_pipeline=None
old_min=0
old_max=0
new_min=0
new_max=0
pipeline=None

class NormalizedPipeline:
	def __init__(self, pipeline,old_min,old_max,new_min,new_max):
		self.pipeline = pipeline
		self.old_min = old_min
		self.old_max = old_max
		self.new_min = new_min
		self.new_max = new_max

	def normalize(self, y_pred):
		y_pred = (y_pred - self.old_min) / (self.old_max - self.old_min) * (self.new_max - self.new_min) + self.new_min
		return(y_pred)

	def predict(self, X):
		y_pred = self.pipeline.predict(X)
		return (self.normalize(y_pred))

class InsulatorHealthPiece(BasePiece):

	def piece_function(self, input_data: InputModel):

				
		self.logger.info(f"InsulatorHealthPiece START")
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

		print(type(y))
		self.logger.info(f"InsulatorHealthPiece GET FEATURES")
		feats=self.get_features_50Hz_Marian_2D(y,sr)
		self.logger.info(f"InsulatorHealthPiece FEATURES SHAPE: "+ str(feats.shape))
		contamination_pred = self.do_prediction(feats)
		self.logger.info('Prediction value {}'.format(contamination_pred))

		# Return output
		return OutputModel(
			contamination=contamination_pred,
		)

	def get_features_50Hz_Marian_2D(self, y, sr, makedb=True, matrix_size=64):
		n_fft = 192000
		print(type(y))
		dur = librosa.get_duration(y=y, sr=sr)
		hop_length = int(sr * dur / matrix_size)
		S = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
		if makedb:
			D = librosa.amplitude_to_db(np.abs(S), ref=-1.0)

		spec_2D_7 = []
		for i in range(D.shape[1]):
			column_vector = D[:, i]
			column_50Hz = []
			for freq in range(50, 20000, 50):
				amp = column_vector[freq]
				column_50Hz.append(amp)
			spec_2D_7.append(column_50Hz)
		return (np.array(spec_2D_7))

	def do_prediction(self,feats):
		global norm_pipeline
		global old_min, old_max, new_min, new_max,pipeline
		if pipeline is None:
			model_path = str(Path(__file__).parent / 'svr_pipeline.joblib')
			limits_path = str(Path(__file__).parent / 'svr_pipeline.limits')
			self.logger.info('Trying to load model from {}'.format(model_path))
			if Path(model_path).exists() and Path(model_path).is_file() and Path(limits_path).exists() and Path(limits_path).is_file():
				try:
					pipeline = joblib.load(model_path)
					old_min, old_max, new_min, new_max = map(float,open(limits_path).read().strip().split())
					self.logger.info('Model loaded')
				except:
					self.logger.info('Loading model failed')
					return (-1.0)
			else:
				self.logger.info('Error: Model file missing')
				return (-1.0)

		feats = np.array([feats])
		feats_flat = feats.reshape((feats.shape[0], -1))
		y_pred = pipeline.predict(feats_flat)[0]
		print(y_pred)
		y_pred = (y_pred - old_min) / (old_max - old_min) * (new_max - new_min) + new_min
		if y_pred<0.0:
			y_pred=0.0
		self.logger.info('Prediction done')
		print(y_pred)
		return (y_pred)
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


