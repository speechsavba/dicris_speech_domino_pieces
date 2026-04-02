# coding=utf-8
# -*- coding: utf-8 -*-
print('TTS START')
import subprocess
import logging
logging.basicConfig(level=logging.ERROR, filename="tts.log", filemode='w')
import scipy.io.wavfile as wav

import os,sys
import string
import json
import math
import time

import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader

import commons

import utils
import numpy as np
import sys,os
print('*'*40)
print(sys.path)
print('*'*40)
print(os.getcwd())
print('*'*40)

emotions={'<nadšenie>':5,'<povzbudenie>':6,'<chlacholenie>':7,'<radosť>':8,'<hnev>':9 }

#from data_utils import TextAudioLoader, TextAudioCollate, TextAudioSpeakerLoader, TextAudioSpeakerCollate

from models_vits import SynthesizerTrn
from texttext.symbols import symbols
from texttext import text_to_sequence

from scipy.io.wavfile import write
import random

from tts_preproces import tts_pps 
from tts_prevod import tts_prevod
from clean_temp import clean_temp_dir 

import glob
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
clean_temp_dir(current_dir+'/tmp/')

voices={}
print(torch.are_deterministic_algorithms_enabled())
#torch.use_deterministic_algorithms(warn=True)
#print(torch.are_deterministic_algorithms_enabled())
#sys.exit()

device = torch.device("cpu")
#device = torch.device("cuda")

def latest_checkpoint_path(dir_path, regex="G_*.pth"):
	f_list = glob.glob(os.path.join(dir_path, regex))
	f_list.sort(key=lambda f: int("".join(filter(str.isdigit, f))))
	x = f_list[-1]
	print(x)
	return x


def load_model(name,path):
		global voices
		global device
		
		print(name,path)
		voices[name]=path
		latest_cp=latest_checkpoint_path(path)
		config = path+'/config.json'
		print(config)
		hps = utils.get_hparams_from_file(config)
		#print(hps)
		#sys.exit(0)

		if 'symbols' in hps and 'symbols_len' in hps['symbols']:    
			symbols_len= hps['symbols']['symbols_len']
		else:
			symbols_len=len(symbols)
		#if name=='milan' or name=='bajn' or name=='mato':
		#		symbols_len=216			
		net_g = SynthesizerTrn(
				symbols_len,
				hps.data.filter_length // 2 + 1,
				hps.train.segment_size // hps.data.hop_length,
				**hps.model)
		net_g.to(device) 
		_ = net_g.eval()
		print(_)
		_ = utils.load_checkpoint(latest_cp, net_g, None)
		print(_)
		voices[name]=[hps,net_g]
		return

def load_models(modelsdir,onlymodel=None):
	global voices
	toload=[]
	for path in glob.glob(f'{modelsdir}/*/'):
		print(path)
		if '_skip' in path:
			print('skipping: ',path)
		elif onlymodel!=None and not onlymodel in path:
			print('skipping: ', path)
		else:
			name=os.path.basename(os.path.normpath(path))
			toload.append([name,path])

	for name,path in toload:
		load_model(name,path)
	voice_list=[]
	for voice in voices:
		print(voice,type(voices[voice][0]),type(voices[voice][1]))
		voice_list.append(voice)
	return(voice_list)

def get_text(text, hps):
	print('-'*40)
	print(text)
	print('-'*40)
	if 'symbols' in hps and 'symbols_len' in hps['symbols']:
	  symbols_len= hps['symbols']['symbols_len']
	  version=symbols_len
	print('+'*40)
	print(text)
	print('+'*40)
	text_norm,wrong_symbols = text_to_sequence(text, hps.data.text_cleaners,version=version)
	if hps.data.add_blank:
		text_norm = commons.intersperse(text_norm, 0)
	text_norm = torch.LongTensor(text_norm)
	#print('@'*40)
	#print(text_norm)
	#print('@'*40)
	return text_norm,wrong_symbols

def do_tts(voice,text,audio_file,length_scale=1.0):
	global voices
	global device
	global emotions
	print('Cleaning text !!!')
	text = text.lower()
	text = text.replace('co2','cé ó dva')
	text= tts_pps(text)
	
	print(text)
	if '_ore' in voice:
		#print('Prevod text !!!')
		add_emotion=-1
		for emo in emotions:
			if emo in text:
				add_emotion=emotions[emo]
				text=text.replace(emo,'')
		text=tts_prevod(text)
		if 'hamar3' in voice:
				text=' '+text+' '
				text=text.replace(' hes ',' 8 ')
				text=text.replace(' hez ',' 8 ')
				text=text.replace(' spk ',' 9 ')
				text=text.replace(' zbg ',' 9 ')
				print(text)
		if add_emotion>0:
			text+=str(add_emotion)
		print(text)
		print('Po Prevod text !!!')

	hps,net_g=voices[voice]
	stn_tst,wrong_symbols = get_text(text, hps)
	print(stn_tst,wrong_symbols)
	time_1=time.time()	
	print('Running TTS')
	with torch.no_grad():
		x_tst = stn_tst.unsqueeze(0).to(device)
		x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).to(device)
		#print('*'*40)
		#print('*'*40)
		#print(type(x_tst_lengths))
		#print(x_tst_lengths.size())
		#print(x_tst.size())
		#print('*'*40)
		#print('*'*40)
		audio = net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=length_scale)[0][0,0].data.cpu().float().numpy()


		#audio_file=args[1]
	time_2=time.time()	
	print('Writing temporary wav file')
	#print('Sampling rate:',hps.data.sampling_rate)
	#print('data:',type(audio))
	#print('data:',type(audio.size))
	#print('data:',audio[0:10])
	#audio_int16 = audio.astype(np.int16, casting='safe')
	audio_int32 = (audio*1024000000).astype(np.int32)
	#print('data:',audio_int32[0:10])
	#audio_int16 =(audio_int32>>16).astype(np.int16)   

	#wav.write(audio_file, hps.data.sampling_rate, audio_int32)
	audio_int16 =(audio*32000).astype(np.int16)
	#wav.write(audio_file, hps.data.sampling_rate, audio_int16)
	time_3=time.time()	
	wav.write(audio_file, hps['data']['sampling_rate'], audio_int16)#16000
	time_4=time.time()	

	if not os.path.exists(audio_file):
		print('Error writing wav file ', audio_file)
		return(-1)
	text_file=audio_file+'.txt'
	fout=open(text_file,'w',encoding='utf-8')
	fout.write(text)
	fout.close()
	time_5=time.time()	
	return(wrong_symbols,time_5-time_1,time_2-time_1,time_3-time_2,time_4-time_3,time_5-time_4)


def test():        
	modelsdir = './model/'
	load_models(modelsdir)
	i=0
	for text in ['mama bola doma.','otec nebol doma!','Dedo tam bol alebo nie?']:
		i+=1
		for voice in voices:
			i+=1
			do_tts(voice,text,'./tmp/'+voice+'_'+str(i)+'.wav')
			#sys.exit(0)
			
	sys.exit(0)

def main2(args):
	audio_file=args[1]
	text_file=args[0]
	if len(args)>=3:
		modelname=args[2]
	else:
		modelname = 'bajn'
	load_models('./model/', onlymodel=modelname)
	print('Reading text file: ',text_file)
	file = open(args[0], "r", encoding='cp1250')
	text=file.read()
	times=do_tts(modelname,text,audio_file,align_type='simple')
	print(times)

def main(args):

	print('Reading text file: ',args[0])
	file = open(args[0], "r", encoding='cp1250')
	text=file.read()
	if len(args)==2:
		voice='milan'
		path='./model/milan'
	elif args[2] in ['milan','bajn','mato']:
		voice=args[2]
		path='./model/'+voice
	else:
		voice='milan'
		path='./model/milan'
	print('*'*20)
	print('VOICE: ',voice)
	print('*'*20)
	print('Preprocessing text')
	text= tts_pps(text)

	if True:
		print('Loading models')
		latest_cp=latest_checkpoint_path(path)
		config = path+'/config.json'
		print(config)
		hps = utils.get_hparams_from_file(config)
		#print(hps)
		#sys.exit(0)

		device = torch.device("cpu")
		if 'symbols' in hps and 'symbols_len' in hps['symbols']:
			symbols_len= hps['symbols']['symbols_len']
		else:
			symbols_len=len(symbols)
		print('symbols_len:',symbols_len)

		device = torch.device("cpu")

		net_g = SynthesizerTrn(
			symbols_len,
			hps.data.filter_length // 2 + 1,
			hps.train.segment_size // hps.data.hop_length,
			**hps.model)
		net_g.to(device)
		_ = net_g.eval()

		if voice=='milan':
			_ = utils.load_checkpoint("./model/milan/G_384000.pth", net_g, None)
		elif voice=='mato':
			_ = utils.load_checkpoint("./model/mato/G_630000.pth", net_g, None)
		elif voice=='bajn':
			_ = utils.load_checkpoint("./model/bajn/G_464000.pth", net_g, None)

		print('Cleaning text')
		stn_tst = get_text(text, hps)

		print('Running TTS')
		with torch.no_grad():
			x_tst = stn_tst.unsqueeze(0).to(device)
			x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).to(device)
			audio = net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
		#ipd.display(ipd.Audio(audio, rate=hps.data.sampling_rate, normalize=False))

	audio_file=args[1]
	if audio_file.endswith('.wav'):
		print('Writing temporary wav file')
		temp_audio_file='./tmp/'+''.join(random.choices(string.ascii_letters, k=8))+'.wav'
		wav.write(temp_audio_file, hps.data.sampling_rate, audio)
		if not os.path.exists(temp_audio_file):
			print('Error writing wav file ', temp_audio_file)
			return(-1)
						
		print('Converting wav: ',audio_file)
		cmd='ffmpeg -y -i '+temp_audio_file+' -ar 16000 -ac 1 -sample_fmt s16 '+audio_file
		print(cmd)
		os.system(cmd)
		if not os.path.exists(audio_file):
			print('Error - coversion to audio file not succesfull: ',  audio_file)
			os.remove(temp_audio_file)
			return(-1)
		os.remove(temp_audio_file)
						
						
		cmd='python3 mono_align/tts_align.py '+os.path.abspath(audio_file)+' '+os.path.abspath(args[0])
		print (cmd)
		#normal = subprocess.run(cmd.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE,check=True)
		#print(normal.stdout)
		os.system(cmd)
		return(0)
	else:
		print('Writing temporary wav file')
		temp_audio_file='./tmp/'+''.join(random.choices(string.ascii_letters, k=8))+'.wav'
		wav.write(temp_audio_file, hps.data.sampling_rate, audio)
		if not os.path.exists(temp_audio_file):
			print('Error writing temporary wav file')
			return(-1)
		print('Compressing wav to: ',audio_file)
		cmd='ffmpeg -i '+temp_audio_file+' '+audio_file
		print(cmd)
		os.system(cmd)
		if not os.path.exists(temp_audio_file):
			print('Error - coversion to audio file not succesfull: ',  audio_file)
			os.remove(temp_audio_file)
			return(-1)
		os.remove(temp_audio_file)
		return(0)


if __name__ == "__main__":
	#load_model('hamar3_ore','./model/hamar3_ore')
	#times=do_tts('hamar3_ore','mama bola dnes doma','./tmp/mama_bola_doma2.wav')
	load_model('crisis1','../../home_shared_storage/speech_data/tts/models/crisis1/')
	times = do_tts('crisis1', 'deti boli doma', './tmp/deti_boli_doma1a.wav')
	load_model('crisis2', '../../home_shared_storage/speech_data/tts/models/crisis2/')
	times = do_tts('crisis2', 'deti boli doma', './tmp/deti_boli_doma2a.wav')
	load_model('crisis3', '../../home_shared_storage/speech_data/tts/models/crisis3/')
	times = do_tts('crisis3', 'deti boli doma', './tmp/deti_boli_doma3a.wav')
	print(times)
	sys.exit()
	args = sys.argv[1:]
	args=['emo_hnev.txt','emo_hnev.wav','viki_exp_ore2']
	args = ['emo_chlacholenie.txt', 'emo_chlacholenie.wav', 'viki_exp_ore2']
	if len(args)<2:
		print('Nespravny pocet parametrov.\nPriklad pouzitia:\n python synt_svk_file_cpu.py in_file.txt out_file.ogg\n\n')
		print('in_file.txt - obsahuje vstupny subor s textom pre syntezu v kodovani cp1250\n')
		print('out_file.ogg - vystupny zvukovy subor, do ktoreho bude zapisana synteticka rec\n')
		sys.exit(0)
	else:
		cur_path= os.path.dirname(os.path.abspath(__file__))
		os.chdir(cur_path)
		#sys.exit(main(args))
		sys.exit(main2(args))
