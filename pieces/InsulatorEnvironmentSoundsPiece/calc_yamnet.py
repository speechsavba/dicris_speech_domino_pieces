import sys
import numpy as np
import librosa    
import os      
import tensorflow as tf
import soundfile as sf
import random

import yamnet.params as yamnet_params
import yamnet.yamnet as yamnet_model

def get_yamnet_model_v2(patch_window_seconds=0.96, patch_hop_seconds=0.48):
	params = yamnet_params.Params(patch_window_seconds=patch_window_seconds, patch_hop_seconds=patch_hop_seconds)
	yamnet = yamnet_model.yamnet_frames_model(params)
	current_dir = os.path.dirname(os.path.abspath(__file__))
	yamnet.load_weights(current_dir+'/yamnet/yamnet.h5')
	yamnet_classes = yamnet_model.class_names(current_dir+'/yamnet/yamnet_class_map.csv')

	return (yamnet,yamnet_classes)

yamnet_model_loaded=None
class_names=None

def identify_with_yamnet_from_wav(wavname):

	wavname_orig = wavname
	wavname = os.path.normpath(wavname)

	# Nacitaj zvuk a resampluj na 16 kHz
	try:
		waveform, sr = librosa.load(wavname)
	except:
		return(None)

	waveform_16k = librosa.resample(waveform, orig_sr=sr, target_sr=16000)
	waveform_np = waveform_16k.astype(np.float32)

	return(identify_with_yamnet(waveform_np))


def identify_with_yamnet(audiodata):
	global yamnet_model_loaded,class_names


	waveform_np = audiodata

	if yamnet_model_loaded==None:
		yamnet_model_loaded, class_names = get_yamnet_model_v2()

	scores, embeddings, spectrogram = yamnet_model_loaded(waveform_np)

	scores_np = scores.numpy()
	mean_scores = np.mean(scores, axis=0)
	class_id=scores_np.mean(axis=0).argmax()
	infered_class = class_names[class_id]
	top_class_indices = np.argsort(mean_scores)[::-1][:10]
	top10=''
	for s in top_class_indices:
		top10+=class_names[s]+' '+str(mean_scores[s])+'\n'

	print(f'The main sound is: {infered_class}')
	return(infered_class,mean_scores[class_id],top10)
	
	

if __name__ == '__main__':
	audio_file='../InsulatorHealthPiece/test_audio/echo_20250716_113400_7B-3.wav'
	infered_class,prob,top10=identify_with_yamnet_from_wav(audio_file)
	print(top10)

