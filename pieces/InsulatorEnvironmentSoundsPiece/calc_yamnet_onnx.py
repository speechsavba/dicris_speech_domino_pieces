import onnxruntime as ort
import numpy as np
import librosa
import csv,os

model=None
class_names=None
input_name=None

def load_class_map(path="yamnet/yamnet_class_map.csv"):
    with open(path, newline='') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        return [row[2] for row in reader]

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
	
def identify_with_yamnet(audiodata,modelpath):
	global model, class_names, input_name
	print(model)
	print(model==None)
	
	if model==None:
		print('Loading model')
		#current_dir = os.path.dirname(os.path.abspath(__file__))
		model = ort.InferenceSession(modelpath+"/yamnet.onnx", providers=["CPUExecutionProvider"])
		class_names = load_class_map(modelpath+"/yamnet_class_map.csv")
		input_name = model.get_inputs()[0].name
	
	waveform_np = audiodata

	outputs = model.run(None, {input_name: waveform_np})
	scores, embeddings, spectrogram = outputs

	mean_scores = np.mean(scores, axis=0)
	
	class_id=scores.mean(axis=0).argmax()
	infered_class = class_names[class_id]
	top_class_indices = np.argsort(mean_scores)[::-1][:10]
	top10=''
	for s in top_class_indices:
		top10+=class_names[s]+' '+str(mean_scores[s])+'\n'

	print(f'The main sound is: {infered_class}')
	return(infered_class,mean_scores[class_id],top10)



identify_with_yamnet_from_wav('../InsulatorHealthPiece/test_audio/echo_20250716_113400_7B-3.wav')
identify_with_yamnet_from_wav('../InsulatorHealthPiece/test_audio/echo_20250715_094400_7B-0.wav')