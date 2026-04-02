import glob
import os,sys
import numpy as np
import soundfile as sf
import json
import tensorflow_hub as hub
import tensorflow as tf
modulev3=None


'''
wav_file='mama.wav'
signal, samplerate = sf.read(wav_file)

modulev3 = hub.load('./v3')
trillv3 = modulev3(samples=signal, sample_rate=samplerate)
trillv3_emb = trillv3['embedding']
'''
# Import TF 2.X and make sure we're running eager.
#import tensorflow.compat.v2 as tf
#tf.enable_v2_behavior()
#assert tf.executing_eagerly()


def init_trill_model(pp=None):
	global modulev3, modulev3_graph
	if pp is None:
		pp=os.path.dirname(__file__)
	print('Init TRILL model 1')
	try:
		modulev3 = hub.load(pp+'/v3')
	except Exception as e:
		print(f"Failed to load model: {e}")
		return(False)

	print('TRILL model loaded')
	print(modulev3)

	#modulev3 = hub.load('https://tfhub.dev/google/nonsemantic-speech-benchmark/trill/3')
	return (True)

def get_TRILLv3_signal(signal,samplerate):
	pp=os.path.dirname(__file__)
	#print(pp)
	#print(pp+'/v3')

	#modulev3 = hub.load(pp+'/v3')
	#modulev3 = hub.load('/home/EWA/flask_server/ASR_RQ/trill/v3')
	#print(' get_TRILLv3_signal Init TRILL model 2')
	modulev3a = hub.load(pp+'/v3')


	#print('TRILL 4aXXXXXX')
	#print('TRILL 4c')
	#print(signal.shape)
	max_int16 = 2**15
	#print('TRILL 4d')
	chunks_cnt=int(signal.shape[0]/(samplerate*10.0))#10 seconds max in chunk
	if chunks_cnt==0:
		chunks=[signal]
	else:
		chunks=np.array_split(signal, chunks_cnt)
	#print('TRILL 4e')
	trillv3_emb_all=np.empty(shape=(0,512))
	#print('TRILL 4f')

	for chunk in chunks:
		#print('TRILL 4f1')
		#print('SR',samplerate)
		#print('CHUNK',chunk.shape)
		#with modulev3_graph.as_default():
		trillv3 = modulev3a(samples=chunk, sample_rate=samplerate)
		#print('TRILL 4f2')
		trillv3_emb = trillv3['embedding']
		#print('TRILL 4f3')
		#print(trillv3_emb.shape)
		#print(trillv3_emb)
		trillv3_emb_all=np.concatenate((trillv3_emb_all, trillv3_emb))
		#print('TRILL 4f4')
	#print('TRILL 4g')
	trillv3_emb_avg = np.mean(trillv3_emb_all, axis=0, keepdims=False)
	#print('TRILL 4h')
	return (trillv3_emb_avg.tolist())

def get_TRILLv3_signal_ok(signal,samplerate):
	global modulev3, modulev3_graph
	#print('TRILL 4aZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ')
	if modulev3==None:
		print('TRILL 4b')
		init_trill_model()
		if modulev3==None:
			print('Error loading model')
			return()
		else:
			print('TRILL Model loaded')
	#print('TRILL 4c')
	#print(signal.shape)
	max_int16 = 2**15
	#print('TRILL 4d')
	chunks_cnt=int(signal.shape[0]/(samplerate*10.0))#10 seconds max in chunk
	if chunks_cnt==0:
		chunks=[signal]
	else:
		chunks=np.array_split(signal, chunks_cnt)
	#print('TRILL 4e')
	trillv3_emb_all=None
	#print('TRILL 4f')

	for chunk in chunks:
		#print('TRILL 4f1')
		print('SR',samplerate)
		#print('CHUNK',chunk.shape)
		trillv3 = modulev3(samples=chunk, sample_rate=samplerate)
		#print('TRILL 4f2')
		trillv3_emb = trillv3['embedding']
		#print('TRILL 4f3')
		if trillv3_emb_all==None:
			trillv3_emb_all=trillv3_emb
		else:
			trillv3_emb_all=tf.concat([trillv3_emb_all, trillv3_emb], axis=0)
		#trillv3_emb_all=np.concatenate((trillv3_emb_all, trillv3_emb))
		#print('TRILL 4f4')
	#print('TRILL 4g')
	trillv3_emb_avg = tf.reduce_mean(trillv3_emb_all,axis=0, keepdims=False)
	#trillv3_emb_avg = np.mean(trillv3_emb_all, axis=0, keepdims=False)
	#print('TRILL 4h')
	return (trillv3_emb_avg.numpy().tolist())

def get_TRILLv3_audiofile_ok(audio='mama.wav'):
	global modulev3, modulev3_graph
	#print('TRILL 1')
	if modulev3==None:
		#print('TRILL 2')
		init_trill_model()

	#print('TRILL 3')
	signal, samplerate = sf.read(audio)
	#print('TRILL 4')
	trill2=get_TRILLv3_signal(signal,samplerate)
	#trill2=get_TRILLv3_signal_ok(signal,samplerate)
	#print('TRILL 5')
	return(trill2)

def get_TRILLv3_audiofile(audio='mama.wav'):
	#print('TRILL 3')
	signal, samplerate = sf.read(audio)
	#print('TRILL 4 before get_TRILLv3_signal')
	trill2=get_TRILLv3_signal(signal,samplerate)
	#trill2=get_TRILLv3_signal_ok(signal,samplerate)
	#print('TRILL 5')
	return(trill2)


def get_TRILLv3_signal_v1(signal,samplerate):
	global modulev3
	if modulev3==None:
		init_trill_model()

	#print(signal.shape)
	max_int16 = 2**15


	trillv3 = modulev3(samples=signal, sample_rate=samplerate)
	trillv3_emb = trillv3['embedding']
	trillv3_emb_avg = np.mean(trillv3_emb, axis=0, keepdims=False)

	return (trillv3_emb_avg.tolist())



#calc_TRILL(dbpath+'wav.scp',dbpath+'trill.ark')
if __name__ == "__main__":
	init_trill_model()
	wav_file='mama.wav'
	signal, samplerate = sf.read(wav_file)
	
	trill1 = get_TRILLv3_signal_ok(signal, samplerate)
	print(trill1[:10])
	trill2 = get_TRILLv3_signal(signal, samplerate)
	print(trill2[:10])
	input('>')
	#signal, samplerate = sf.read('../../ASR_align/trs/665u9v5i01.wav')
	for i in range(1):
		print(i)
		print('get_TRILLv3_signal_v1')
		trill1=get_TRILLv3_signal_v1(signal,samplerate)
		print('get_TRILLv3_signal')
		trill2=get_TRILLv3_signal(signal,samplerate)
		print('get_TRILLv3_audiofile')
		trill3=get_TRILLv3_audiofile(wav_file)

		with open('test1.json', "w",encoding='utf-8') as write_file:
			json.dump(trill1, write_file, indent=4,ensure_ascii=False,sort_keys=True)
		with open('test2.json', "w",encoding='utf-8') as write_file:
			json.dump(trill2, write_file, indent=4,ensure_ascii=False,sort_keys=True)

	print('FINISH')

