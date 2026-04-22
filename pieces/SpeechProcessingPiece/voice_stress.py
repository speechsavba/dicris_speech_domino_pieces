# -*- coding: utf-8 -*-
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
import traceback

class VoiceStress():
	def __init__(self, trill_model_path, stress_regression_model_path,logger=None):
		
		self.current_dir = os.path.dirname(os.path.abspath(__file__))
		sys.path.append(self.current_dir)
		from trill import init_trill_model, get_TRILLv3_audiofile, get_TRILLv3_signal,get_TRILLv3_signal_ok
		self.init_trill_model = init_trill_model
		self.get_TRILLv3_signal = get_TRILLv3_signal_ok
		self.trill_model_path=trill_model_path
		self.stress_regression_model_path=stress_regression_model_path
		self.logger = logger
		try:
			self.trill_model_ready=self.init_trill_model(pp=self.trill_model_path)
			if False:
				self.nnmodel = tf.keras.Sequential([
				    tf.keras.layers.InputLayer(batch_input_shape=(None, 512), dtype='float32'),
					layers.Dense(128, activation='relu'),
					layers.Dropout(0.4),
					layers.Dense(64, activation='relu'),
					layers.Dense(1) # regresia
					])
				self.nnmodel.compile(optimizer='adam', loss=Huber(delta=1.0), metrics=['mae'])
				self.nnmodel.load_weights(self.stress_regression_model_path)
			else:
				self.nnmodel = tf.keras.models.load_model(self.stress_regression_model_path,custom_objects={"Huber": Huber})
		except Exception:
			self.nnmodel=None
			self.trill_model_ready=False
			print('Exception loading model: ',self.stress_regression_model_path)
			traceback.print_exc()
			if self.logger:
				self.logger.info('Error: VoiceStress class not initialised')
			return
		if self.logger:
			self.logger.info('VoiceStress class initialised')
		return
		
	#   y - signal 16kHz
	#  sr - sampling frequency
	def get_voice_stress_level(self,y,sr=16000):
		if not self.trill_model_ready:
			if self.logger:
				self.logger.info('Trill model missing in path: '+self.trill_model_path)
			return(-1.0,-1.0)
		if self.nnmodel is None:
			if self.logger:
				self.logger.info('Voice Stress model missing in path: '+self.stress_regression_model_path)
			return (-1.0, -1.0)
		feats=self.get_features_trill(y,sr)
		speechstress_score,speechstress_prob = self.do_prediction(feats)
		if speechstress_prob<0.0:
			speechstress_prob=0.0
		if speechstress_prob>1.0:
			speechstress_prob=1.0
		if self.logger:
			self.logger.info('Stress probability value {}'.format(speechstress_prob))
		# Return output
		return (float(speechstress_score),speechstress_prob)

	def get_features_trill(self, y, sr):
		#print(type(y))
		if self.logger:
			self.logger.info('VoiceStress.get_features_trill START')

		if not self.trill_model_ready:
			self.init_trill_model(pp=self.trill_model_path)
		trillv3_emb_avg=self.get_TRILLv3_signal(y,sr)
		if self.logger:
			self.logger.info('VoiceStress.get_features_trill FINISH')
		return (np.array(trillv3_emb_avg))
		
	def sigmoid_transformation(self,x):
	    stred = 18
	    strmost = 0.2#0.35 
	    
	    y = 1 / (1 + math.exp(-strmost * (x - stred)))
	    return y			
	
	def transformacia_rozsahu(self,x):
	    # O�etrenie hodn�t mimo z�kladn� rozsah 0-100 (volite�n�)
	    x = max(0, min(100, x))

	    if x <= 13:
	        # Segment 0-13 -> 0-0.13
	        # Pomer je 1:1, ale vzorec pre linearitu: y = y0 + (x - x0) * (y1 - y0) / (x1 - x0)
	        return x * (0.13 / 13)
	    
	    elif x <= 23:
	        # Segment 13-23 -> 0.13-0.75
	        return 0.13 + (x - 13) * (0.75 - 0.13) / (23 - 13)
	    
	    else:
	        # Segment 23-100 -> 0.75-1.0
	        return 0.75 + (x - 23) * (1.0 - 0.75) / (100 - 23)

	def do_prediction(self,feats):
		if self.nnmodel is None:
			if self.logger:
				self.logger.info('Voice Stress model missing in path: '+self.stress_regression_model_path)
			return(-1.0,-1.0)
		if self.logger:
			self.logger.info('VoiceStress.do_prediction START')
		print('do_prediction: '+str(type(feats)) +' '+ str(feats.shape))
		
		y_pred = self.nnmodel.predict(np.array([feats]))[0][0]
		if self.logger:
			self.logger.info('VoiceStress.do_prediction FINISH')
		print(y_pred)
		stress_prob=self.sigmoid_transformation(y_pred)
		print(y_pred,stress_prob)
		return (y_pred,stress_prob)
		
if __name__ == "__main__":
	wav_file='e:/Python/TRILL/mama.wav'
	import soundfile as sf
	signal, samplerate = sf.read(wav_file)
	vs=VoiceStress(trill_model_path=r"e:/Python/DiCris/DOMINO/dicris_speech_domino_pieces/home_shared_storage/speech_data/stress/trill/", stress_regression_model_path='e:/Python/DiCris/DOMINO/dicris_speech_domino_pieces/home_shared_storage/speech_data/stress/model/nn_stress_regressor_mmvl+stressdat_huber.keras')
	print(vs.get_voice_stress_level(signal))


