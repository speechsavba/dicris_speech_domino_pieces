from nemo.collections.asr.models import EncDecSpeakerLabelModel
from sklearn.metrics.pairwise import cosine_similarity
import torch
import numpy as np
import librosa,glob,os,json
import traceback

default_home_shared_storage='e:/Python/DiCris/DOMINO/dicris_speech_domino_pieces/home_shared_storage/'
class SPEAKER_ID():
	def __init__(self, score_th=0.7,home_shared_storage=default_home_shared_storage,logger=None):
		self.home_shared_storage=home_shared_storage
		self.enrolments_file=self.home_shared_storage+'/speech_data/speaker/enrollments/enrollments.json'
		self.score_th=score_th
		self.model=None
		self.logger=logger
		try:
			self.init_model()
			self.init_enrollments()
		except Exception:
			traceback.print_exc()
			if self.logger:
				self.logger.info('ERROR: SPEAKER_ID class not initialised')
			return
		return


	def init_model(self):
		self.model = EncDecSpeakerLabelModel.from_pretrained("titanet_large")
		self.model.eval()

	def init_enrollments(self):

		if os.path.isfile(self.enrolments_file):
			fin=open(self.enrolments_file,'r',encoding='utf8')
			self.enrollments=json.load(fin)
			fin.close()
		else:
			self.enrollments={}


	def get_audio(self,file_path):
		audio, sr = librosa.load(file_path, sr=16000, mono=True)
		return(audio, sr)

	def get_embedding_signal(self,audio):
		signal = torch.tensor(audio).unsqueeze(0)  # [1, T]
		length = torch.tensor([signal.shape[1]])
		logits, emb = self.model.forward(input_signal=signal, input_signal_length=length)
		#emb1 = emb.detach().squeeze().cpu().numpy()
		if True:
			emb = emb.detach().squeeze()
			emb = emb / torch.linalg.norm(emb)
		emb = emb.cpu().numpy()
		return(emb)

	def get_embedding_file(self, filename):
		emb = self.model.get_embedding(filename).squeeze()
		if True:
			emb = emb / torch.linalg.norm(emb)
		emb = emb.cpu().numpy()
		return(emb)

	def create_enrollment(self, audio_files):
		embs = []
		for f in audio_files:
			e = self.get_embedding_file(f)
			embs.append(e)

		embs = np.vstack(embs)  # tvar (N, 192)
		embs = embs / np.linalg.norm(embs, axis=1, keepdims=True)
		speaker_emb = np.mean(embs, axis=0, keepdims=True)
		speaker_emb = speaker_emb.reshape(-1).tolist()
		return(speaker_emb)

	def create_enrollments(self,inenrpath):
		speaker_dirs = glob.glob(os.path.join(inenrpath, '**/'), recursive=True)
		enrollments={}
		for speaker_dir in speaker_dirs:
			speaker=os.path.basename(os.path.normpath(speaker_dir))
			wav_v_adresary = glob.glob(speaker_dir+'/*.wav')
			if len(wav_v_adresary)==0:
				continue
			enrl=self.create_enrollment(wav_v_adresary)
			enrollments[speaker]=enrl
		outjson=inenrpath+'enrollments.json'
		fout=open(outjson,'w',encoding='utf8')
		json.dump(enrollments,fout)
		fout.close()
		return

	def find_id_file(self,filepath):
		unk_emb=self.get_embedding_file(filepath)
		max_score=[0,'unknown']
		for speaker in self.enrollments:
			score= cosine_similarity([unk_emb], [self.enrollments[speaker]])[0][0]
			if score>max_score[0]:
				max_score=[score,speaker]
		print('Nearest: ' ,max_score)
		if max_score[0]>self.score_th:
			print('It is: ', max_score)
		else:
			max_score[1] = 'Unknown'
		return(max_score)

	def find_id(self, signal):
			unk_emb = self.get_embedding_signal(signal)
			max_score = [0, 'unknown']
			for speaker in self.enrollments:
				score = cosine_similarity([unk_emb], [self.enrollments[speaker]])[0][0]
				if score > max_score[0]:
					max_score = [score, speaker]
			print('Nearest: ', max_score)
			if max_score[0] > self.score_th:
				print('It is: ', max_score)
			else:
				max_score[1] = 'Unknown'
			return (max_score)

	def test(self):
		emb1 = self.model.get_embedding("i:/SPEECH_DB-WORK/StressDat/release-29speaker/s04h/1/s04h_2a_crisis_1_0043.wav")
		emb1 = emb1.detach().cpu().numpy()
		emb2 = self.model.get_embedding("i:/SPEECH_DB-WORK/StressDat/release-29speaker/s01a/1/s01a_11a_crisis_1_0303.wav")
		emb2 = emb2.detach().cpu().numpy()

		np.save("speaker_emb1.npy", emb1)
		np.save("speaker_emb2.npy", emb2)


		emb1 = np.load("speaker_emb1.npy")
		emb2 = np.load("speaker_emb2.npy")

		score = cosine_similarity(emb1, emb2)[0][0]
		print("Similarity:", score)

		files = ["rec1.wav", "rec2.wav", "rec3.wav"]
		embs = []
		for f in files:
			e = self.model.get_embedding(f).detach().cpu().numpy()
			embs.append(e)

		embs = np.vstack(embs)   # tvar (N, 192)
		embs = embs / np.linalg.norm(embs, axis=1, keepdims=True)
		template_emb = np.mean(embs, axis=0, keepdims=True)
		np.save("speaker_template.npy", template_emb)

if __name__ == "__main__":
	sv=SPEAKER_ID()
	if True:
		sv.create_enrollments(default_home_shared_storage+'/speech_data/speaker/enrollments/')
	sv.find_id_file('i:/SPEECH_DB-WORK/DiCris/crisis-vyber-dicris-elek-plyn/aj_crisis_1_0001.wav')
	sv.find_id_file('i:/SPEECH_DB-WORK/DiCris/crisis-vyber-dicris-elek-plyn/akal92f_crisis_1_0103.wav')
	file_path='i:/SPEECH_DB-WORK/DiCris/crisis-vyber-dicris-elek-plyn/aj_crisis_1_0001.wav'
	audio, sr = librosa.load(file_path, sr=16000, mono=True)
	sv.find_id(audio)
	file_path='i:/SPEECH_DB-WORK/DiCris/crisis-vyber-dicris-elek-plyn/akal92f_crisis_1_0103.wav'
	audio, sr = librosa.load(file_path, sr=16000, mono=True)
	sv.find_id(audio)

	#sv.create_enrollment('aaa',["i:/SPEECH_DB-WORK/StressDat/release-29speaker/s04h/1/s04h_2a_crisis_1_0043.wav","i:/SPEECH_DB-WORK/StressDat/release-29speaker/s04h/1/s04h_2a_crisis_1_0046.wav"])
	#emb=sv.get_embedding_file("i:/SPEECH_DB-WORK/StressDat/release-29speaker/s04h/1/s04h_2a_crisis_1_0043.wav")

