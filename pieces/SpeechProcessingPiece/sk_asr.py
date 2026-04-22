import argparse
import librosa
import os,re
import sys
import torch
#from huggingface_hub import login
#from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
#import torch
#import torchaudio
#from speechbrain.inference.classifiers import EncoderClassifier
import soundfile as sf
import time
import sherpa_onnx
import random
#pip3 install praat-textgrids
#from textgrids import TextGrid
import traceback

class SK_ASR():
	def __init__(self, asr_model_path,logger=None):
		self.logger=logger
		self.asr_model_path=asr_model_path
		self.model=None
		self.stream=None
		try:
			self.init_model()
		except Exception:
			traceback.print_exc()
			if self.logger:
				self.logger.info('ERROR: SK_ASR class not initialised')
			return

		self.stevo={"[uh]":"uh","[um]":"um","mm-hmm":"mhm",'[spk]':'mhm','[fil]':'mhm','[@]':'uh','[@:]':'uh','[int]':''}
		if self.logger:
			self.logger.info('SK_ASR class initialised')
		return

	def get_audio(self,file_path, start, end,channel=0,mono=False):
		audio, sr = librosa.load(file_path, sr=None, offset=start, duration=end - start,mono=mono)

		if mono==False and audio.ndim != 1:
			return(audio[channel], sr)
		else:
			return(audio, sr)
			
	def init_model(self):
		self.device = "cuda" if torch.cuda.is_available() else "cpu"
		print(self.device)
		torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

		self.model = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=self.asr_model_path+'encoder.onnx',decoder=self.asr_model_path+'decoder.onnx',joiner=self.asr_model_path+'joiner.onnx',tokens=self.asr_model_path+'tokens.txt',provider=self.device)
		#k2_model.to(device)
		return

	
	def clean_ASR_result(self,text):
		text=text.lower()
		text = re.sub(r'[.,!;]', ' ', text)
		text2=''
		for w in text.strip().split(' '):
			if w in self.stevo:
				text2+=self.stevo[w]+' '
			else:
				text2 += w + ' '

		text = re.sub(r' +', ' ', text2).strip()
		return(text)

		
	def transcribe_audio(self,audio,sr=16000):
		if self.model is None:
			return("Missing model in path: "+self.asr_model_path)
		self.stream = self.model.create_stream()
		self.stream.accept_waveform(16000, audio)
		self.model.decode_stream(self.stream)
		text=self.clean_ASR_result(self.stream.result.text)
		return(text)


def main(audiofile):

	if not os.path.isfile(audiofile):
		print('ERROR: Missing audiofile '+audiofile)
		sys.exit(1)
	sk_asr=SK_ASR(asr_model_path='e:/Python/DiCris/DOMINO/dicris_speech_domino_pieces/home_shared_storage/speech_data/asr/model/')
	audio, sr = librosa.load(audiofile, sr=16000)
	res=sk_asr.transcribe_audio(audio,sr)
	print(res)
			



if __name__ == "__main__":
	wav_file='e:/Python/TRILL/mama.wav'
	main(wav_file)
