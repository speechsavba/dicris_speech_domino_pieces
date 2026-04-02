from num2words import num2words
import regex as re

skratky={'žel. st.':'železničná stanica', 'AS':'autobusová stanica'}

def time_replace(match):
	match1 = match.group(1)
	match2 = match.group(2)
	match3 = match.group(3)
	tmp=str.split(':')
	
	#aj sekundy
	if match3!='':
		hodiny=num2words(int(match1),lang='sk')
		minuty=num2words(int(match2),lang='sk')
		sekundy=minuty=num2words(int(match3),lang='sk')
		cas=hodiny + ' ' + minuty + ' ' +sekundy
	elif match2!='':
		hodiny=num2words(int(match1),lang='sk')
		minuty=num2words(int(match2),lang='sk')
		cas=hodiny + ' ' + minuty
	else:
		hodiny=num2words(int(match1),lang='sk')
		cas=hodiny
	return(' '+cas+' ')

def number_replace(match):
	match0 = match.group(0)
	number=num2words(int(match0),lang='sk')
	return(' '+number+' ')

def do_skratky(sentence):
	global skratky
	for skratka in skratky:
		sentence = sentence.replace ( skratka,skratky[skratka] )
	return(sentence)


def tts_pps(text):
	text=' '+text+' '

	text = text.replace('alzhei','alzhaj')
	text=do_skratky(text)
	for char in '.,;!?':
		text=text.replace(char,' '+char+' ')
	text=re.sub(r' (\d{1,2}):(\d\d):{0,1}(\d{0,2}) ', time_replace, text)
	text=re.sub(r' \d+ ', number_replace, text)
	text=re.sub(r' +',' ',text)
	text=re.sub(r' ([,;\!\?\.])',r'\1',text)
	
	#pre hlas milan zatial
	text=text.replace('ä','e')

	return(text)


def main():		
	print('START')
	test=['dnes je 12.3.2025.','kupil som 3 jablka']
	for r in test:
		print(r)
		r=tts_pps(r)
		print(r)

if __name__ == "__main__":
    main()		