# -*- coding: utf-8 -*-
from domino.base_piece import BasePiece
#from pyroomacoustics.datasets.cmu_arctic import speaker_dir

from .models import InputModel, OutputModel
from io import BytesIO
import numpy as np
import base64
import os,sys
from pathlib import Path
import librosa
import numpy as np
import requests
import tensorflow as tf
import numpy as np
import math
from tensorflow.keras import layers, models
from tensorflow.keras.losses import Huber
from .voice_stress import VoiceStress
from .sk_asr import SK_ASR
from .llm_stress import TextStress
from .speaker_verification import SPEAKER_ID

class SpeechProcessingPiece(BasePiece):
	def piece_function(self, input_data: InputModel):

		print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
		if not hasattr(self, 'workflow_shared_storage_path'):
			self.workflow_shared_storage_path='./home_shared_storage'
		if not hasattr(self, 'current_dir'):
			print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
			print("A new SpeechProcessingPiece object has been created!")
			self.current_dir = os.path.dirname(os.path.abspath(__file__))
			# Add it to sys.path if needed
			sys.path.append(self.current_dir)
		print('self.results_path:',self.results_path)
		print('self.workflow_shared_storage_path:',self.workflow_shared_storage_path)
		self.voicestress = VoiceStress(trill_model_path=self.workflow_shared_storage_path+'/speech_data/stress/trill/',stress_regression_model_path=self.workflow_shared_storage_path+'/speech_data/stress/model/nn_stress_regressor_mmvl+stressdat_huber.keras',logger=self.logger)
		self.sk_asr = SK_ASR(asr_model_path=self.workflow_shared_storage_path+'/speech_data/asr/model/',logger=self.logger)
		self.textstress = TextStress(llm_model_path=self.workflow_shared_storage_path+"/speech_data/stress/llm/msievers/gemma-3-1b-it-qat-q4_0-gguf/gemma-3-1b-it-qat-q4_0.gguf",logger=self.logger)
		self.SpeakerID=SPEAKER_ID(score_th=0.6, home_shared_storage=self.workflow_shared_storage_path,logger=self.logger)



		self.logger.info(self.workflow_shared_storage_path)
		self.logger.info(f"SpeechProcessingPiece START")
		sr = input_data.sr
		# Try to open image from file path or base64 encoded string
		y = input_data.y
		print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
		max_path_size = 4096#int(os.pathconf('/', 'PC_PATH_MAX'))
		if len(y) < max_path_size:
			if y.startswith('http'):
				self.logger.info("Y seems to be URL, loading with requests and librosa")
				y,sr=self.get_url_data(y)
			elif  Path(y).exists() and Path(y).is_file():
				self.logger.info("Y is a file path, loading with librosa")
				if sr<=0:
					sr=None
				y, sr = librosa.load(y, sr=16000, mono=True)

		else:
			self.logger.info("Y is not a file path, trying to decode as base64 string")
			try:
				decoded_bytes = base64.b64decode(y)
				y = np.frombuffer(decoded_bytes, dtype=np.float32)
			except Exception:
				raise ValueError("Y is not a file path or a base64 encoded string")

		text              = self.sk_asr.transcribe_audio(y,sr)
		voicestress_score, voicestress_prob = self.voicestress.get_voice_stress_level(y,sr)
		textstress_pred   = self.textstress.get_text_stress_level(text)
		spk_id=self.SpeakerID.find_id(y)
		print(text,voicestress_prob,textstress_pred,spk_id[0],spk_id[1])


		self.logger.info('Prediction value {}'.format(voicestress_prob))
		raw_content = f"Prediction value of stress level in speech on scale 0-1 (0-no stress 1-high stress) is: {voicestress_prob}\n"
		base64_content = base64.b64encode(raw_content.encode("utf-8")).decode("utf-8")
		self.display_result = {
			"file_type": "txt",
			"base64_content": base64_content
		}

		status = 'undefined'
		#TEXT STRESS #NORMAL CAUTION ALERT
		if textstress_pred=='NORMAL' and voicestress_prob < 0.5 :
			status = 'ok'
		elif textstress_pred=='NORMAL' and voicestress_prob < 0.65:
			status = 'moderate'
		elif textstress_pred=='CAUTION':
			status = 'warning'
		elif textstress_pred=='ALERT':
			status = 'critical'
		elif voicestress_prob < 0.8:
			status = 'warning'
		else:
			status = 'critical'
		self.set_dashboard_status(status=status)


		# Return output
		return OutputModel(
			text             = text,
			voicestresslevel = voicestress_prob,
			textstresslevel  = textstress_pred,
			speaker_id       = spk_id[1]
		)

	def set_dashboard_status(self,status,model_name='Voiceprocessing'):
		DASHBOARD_URL = "https://dicris.sk:8000"
		if not status in ['ok','moderate','warning','critical','undefined']:
			status='undefined'

		response = requests.post(
			f"{DASHBOARD_URL}/models",
			json={"name": model_name, "status": status}
		)

		if response.status_code == 201:
			print(f"OK: {response.json()}")
		else:
			print(f"Chyba {response.status_code}: {response.text}")

		return response

	def get_url_data(self,url):
		try:
			headers = {}
			body_data = None
			response = requests.get(url, headers=headers)
			response.raise_for_status()

		except requests.RequestException as e:
			raise Exception(f"HTTP request error: {e}")

		audio_bytes = BytesIO(response.content)

		y, sr = librosa.load(audio_bytes, sr=16000, mono=True)

		return(y,sr)


