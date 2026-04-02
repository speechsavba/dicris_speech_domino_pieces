# coding=utf-8
# -*- coding: utf-8 -*-
import random
import string
import subprocess
 
interpunkcia=',;:?!.\"\'\n\r'
zameny_sachia={	':':'A',
								';':'E',
								'/':'U',
								'_':'J',
								'&':'V',
								'#':'0',
								'$':'1',
								'+':'2',
								'%':'w',
								'<':'3',
								'>':'4'
								}

def parse_text(text):
	global interpunkcia
	parts=[]
	part=''
	for c in text:
		if c in interpunkcia:
			parts.append([part.strip(),c])
			part=''
			continue
		else:
			part+=c
	if len(part)!=0:
		parts.append([part.strip(),''])
	return (parts)


def tts_prevod(text,tmp_path='./tmp/'):

	parts=parse_text(text)
	#print(parts)

	p=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
	tmp_file=tmp_path+p+'.cp1250'
	fout=open(tmp_file,'w',encoding='cp1250')
	for part in parts:
		fout.write(part[0]+'\n')
	fout.close()
	tmp_file_prevod=tmp_file+'.prevod'
	
	#print('PREVOD')
	cmd='./prevod/TTS_HMM -vocab '+tmp_file+' '+tmp_file_prevod
	#print (cmd)
	normal = subprocess.run(cmd.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE,check=True)
	#print(normal.stdout)
	
	#os.system(cmd)
	#print(text)
	#print('PO PREVOD')
	fin = open(tmp_file_prevod, "r", encoding='cp1250')
	oe_all=''
	i=-1
	for r in fin:
		i+=1
		r=r.strip()
		if len(r)==0 or not '\t' in r:
			continue				
		og,oe=r.strip().split('\t')
		og=og.strip()
		oe=oe.strip()
		#print(og,' -> ',oe)
		oe2=''
		for c in oe:
			if c in zameny_sachia:
				oe2+=zameny_sachia[c]
			else:
				oe2+=c
		#print(oe2)
		if og==parts[i][0]:
			oe2+=parts[i][1]
		oe_all+=oe2+' '
	#print(oe_all)
	fin.close()

	return(oe_all.strip())
		
		
		

	return(phones)

if __name__ == '__main__':
	tts_prevod(text='Dietky, piatok: paniu; kraj? kov! amfóra "banka" \'pánsky\' vdova. dzyňa džem\nmama bola dnes doma.')