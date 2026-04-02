from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import base64
import hashlib
import os,sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
from tts_vits import load_model, do_tts

class TTSPiece(BasePiece):

	def generate_hash(self, text):
	    # Encode the text to bytes
	    encoded_text = text.encode('utf-8')
	    # Create a SHA-256 hash object
	    hash_object = hashlib.sha256(encoded_text)
	    # Get the hexadecimal representation of the hash
	    hash_hex = hash_object.hexdigest()
	    return hash_hex

	def piece_function(self, input_data: InputModel):
		if not hasattr(self, 'workflow_shared_storage_path'):
			self.workflow_shared_storage_path='./home_shared_storage'
			self.workflow_shared_storage_path=os.path.abspath(self.workflow_shared_storage_path)
		current_dir = os.path.dirname(os.path.abspath(__file__))
		os.chdir(current_dir)
		text = input_data.text
		voice = input_data.voice
		out_file = self.workflow_shared_storage_path+'/speech_data/tts/tmp/'+self.generate_hash(text)+'_'+voice+'.wav'
		self.logger.info(f'Starting tts for:\n{voice}')
		load_model(voice,self.workflow_shared_storage_path+'/speech_data/tts/models/'+voice)
		times=do_tts(voice,text,out_file)
		out_file=os.path.abspath(out_file)

		raw_content = f"File:\n{out_file}\n"
		base64_content = base64.b64encode(raw_content.encode("utf-8")).decode("utf-8")
		self.display_result = {
			"file_type": "txt",
			"base64_content": base64_content
		}		
		return OutputModel(output_audiofile_path=out_file)
