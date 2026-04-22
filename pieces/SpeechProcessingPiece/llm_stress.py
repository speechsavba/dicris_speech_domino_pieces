from llama_cpp import Llama
import os,sys
import traceback

default_prompt = "Si klasifikacný modul. Tvojou jedinou úlohou je zaradit vstupný text do jedného z nasledujúcich troch tagov (ALERT,CAUTION,NORMAL):\
			- ALERT - ak text obsahuje varovanie, hrozbu, nebezpecenstvo, núdzový stav\
			- CAUTION - potenciálne riziko, varovanie bez naliehavosti\
			- NORMAL  - ak ide o bežný oznam, pozdrav alebo neutrálnu vetu\
			PRAVIDLÁ: - Odpovedaj VÝHRADNE jedným tagom - NIKDY nepridávaj žiadne iné slová - NIKDY nevysvetluj odpoved\
			Príklady:\
			User: klasifikuj: pozor hrozí nebezpecenstvo\
			assistant: ALERT\
			User: klasifikuj: klzká podlaha\
			assistant: CAUTION\
			User: klasifikuj: nameral som hodnotu 220 voltov\
			assistant: NORMAL\
			User: klasifikuj: Fáza L1 – porucha.\
			assistant: ALERT\
			User: klasifikuj: Prosíme o zvýšenú opatrnost.\
			assistant: CAUTION\
			User: klasifikuj: Prebieha servis.\
			assistant: NORMAL\
			"
default_prompt2 = "Si klasifikacný modul. Tvojou jedinou úlohou je zaradit vstupný text do jedného z nasledujúcich troch tagov (ALERT,CAUTION,NORMAL):\
			- ALERT - ak text obsahuje varovanie, hrozbu, nebezpecenstvo, núdzový stav\
			- CAUTION - potenciálne riziko, varovanie bez naliehavosti\
			- NORMAL  - ak ide o bežný oznam, pozdrav alebo neutrálnu vetu\
			PRAVIDLÁ: - Odpovedaj VÝHRADNE jedným tagom - NIKDY nepridávaj žiadne iné slová - NIKDY nevysvetluj odpoveď"
priklady=[['klasifikuj: pozor hrozí nebezpecenstvo','assistant: ALERT'],\
			['klasifikuj: klzká podlaha','CAUTION'],\
			['klasifikuj: nameral som hodnotu 220 voltov','NORMAL'],\
			['klasifikuj: Fáza L1 – porucha.','ALERT'],\
			['klasifikuj: Prosíme o zvýšenú opatrnosť.','CAUTION'],\
			['klasifikuj: Prebieha servis.','NORMAL']]




class TextStress():
	def __init__(self, llm_model_path, prompt=None,logger=None):
		global default_prompt
		self.current_dir = os.path.dirname(os.path.abspath(__file__))
		sys.path.append(self.current_dir)
		self.llm_model_path =llm_model_path
		self.logger = logger

		if not os.path.isfile(self.llm_model_path):
			if self.logger:
				self.logger.info('Error: VoiceStress class not initialised - llm_model_path not file')
			self.llm_model = None
			return

		#self.llm_model = self.init_llm(chat_format="gemma")

		try:
			self.llm_model = self.init_llm()
		except Exception:
			self.llm_model=None
			traceback.print_exc()
			if self.logger:
				self.logger.info('Error: VoiceStress class not initialised - Llama did not load model')
			return
		if prompt == None:
			self.prompt=default_prompt
		else:
			self.prompt=prompt
		if self.logger:
			self.logger.info('VoiceStress class initialised')
		return

	def init_llm(self, n_ctx=4096, n_threads=1, n_gpu_layers=0, chat_format=None):
		print(self.llm_model_path)
		llm_model = Llama(model_path=self.llm_model_path,
						  n_ctx=n_ctx,  # kontext
						  n_threads=n_threads,  # podľa CPU
						  n_gpu_layers=n_gpu_layers,  # ak chceš GPU, nastav >0
						  chat_format=chat_format,
						  verbose=False
						  )
		return(llm_model)

	def get_text_stress_level(self,text,debug=False):
		#pred=self.get_text_stress_level_v1(text)
		pred = self.get_text_stress_level_v2(text)
		if debug==False:
			if 'NORMAL' in pred:
				return('NORMAL')
			elif 'CAUTION' in pred:
				return ('CAUTION')
			elif 'ALERT' in pred:
				return ('ALERT')
			else:
				return ('UNKNOWN')
		else:
			pred=pred.replace('\n',' ')
			if 'NORMAL' in pred:
				return('NORMAL'+' - '+pred)
			elif 'CAUTION' in pred:
				return ('CAUTION'+' - '+pred)
			elif 'ALERT' in pred:
				return ('ALERT'+' - '+pred)
			else:
				return ('UNKNOWN'+' - '+pred)


	
	def get_text_stress_level_v1(self,text):
		if self.llm_model==None:
			self.llm_model=init_llm()

		for max_tokens in [10,20,30,40]:
			response = self.llm_model(
				self.prompt+' User: '+text,
				max_tokens=max_tokens,
				temperature=0.0,
				top_p=1.0,
				min_p=0.0,
				top_k=1.0,
				stop=["</s>"]
			)
			for res in ['NORMAL','CAUTION','ALERT']:
				if res in response["choices"][0]["text"]:
					return (response["choices"][0]["text"])

		#print(text,'V1->',response["choices"][0]["text"])
		#nput('>')
		return(response["choices"][0]["text"])

	def get_text_stress_level_v2(self,text):

		if self.llm_model==None:
			return('UNKNOWN')
		messages = [{"role": "system", "content": default_prompt2}]
		for user,assistant in priklady:
			messages.append({"role": "user", "content": user})
			messages.append({"role": "assistant", "content": assistant})
		messages.append({"role": "user", "content": 'klasifikuj: '+text})
		for max_tokens in [10, 20, 30, 40]:
			response = self.llm_model.create_chat_completion(
				messages=messages,
				max_tokens=10,
				temperature=0.0,
				top_p=1.0,
				min_p=0.0,
				top_k=1.0,
				stop=["</s>"]
			)
			for res in ['NORMAL','CAUTION','ALERT']:
				if res in response["choices"][0]["message"]["content"]:
					return (response["choices"][0]["message"]["content"])

		#print(text,'V2->',response["choices"][0]["message"]["content"])
		return(response["choices"][0]["message"]["content"])



if __name__ == "__main__":

	ts = TextStress(llm_model_path=r"e:/Python/DiCris/DOMINO/dicris_speech_domino_pieces/home_shared_storage/speech_data/stress/llm/msievers/gemma-3-1b-it-qat-q4_0-gguf/gemma-3-1b-it-qat-q4_0.gguf")
	texty = ['na stanici prebieha rekonštrukcia, zvýšte opatrnosť pri pohybe',
			 'dnes som unavený idem sa už radšej najesť', 'táto hodnota sa mi nepáči','utekajte']

	for t in texty:
		print(t,ts.get_text_stress_level_v2(t))
		#print(t,ts.get_text_stress_level(t))

