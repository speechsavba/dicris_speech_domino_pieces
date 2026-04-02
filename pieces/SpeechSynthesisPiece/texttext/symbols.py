""" from https://github.com/keithito/tacotron """

'''
Defines the set of symbols used in text input to the model.
'''
_pad        = '_'
_punctuation = ';:,.!?¡¿—…"«»“” '
_letters =     'AÁÄBCČDĎEÉFGHChIÍJKLĹĽMNŇOÓÔPQRŔSŠTŤUÚVWXYÝZŽaáäbcčdďeéfghchiíjklĺľmnňoóôpqrŕsštťuúvwxyýzžä@%řě-'
_letters_216 = 'AÁÄBCČDĎEÉFGHChIÍJKLĹĽMNŇOÓÔPQRŔSŠTŤUÚVWXYÝZŽaáäbcčdďeéfghchiíjklĺľmnňoóôpqrŕsštťuúvwxyýzžä'
_letters_217 = 'AÁÄBCČDĎEÉFGHChIÍJKLĹĽMNŇOÓÔPQRŔSŠTŤUÚVWXYÝZŽaáäbcčdďeéfghchiíjklĺľmnňoóôpqrŕsštťuúvwxyýzžä-'
_letters_221 = 'AÁÄBCČDĎEÉFGHChIÍJKLĹĽMNŇOÓÔPQRŔSŠTŤUÚVWXYÝZŽaáäbcčdďeéfghchiíjklĺľmnňoóôpqrŕsštťuúvwxyýzžä@%řě-'
_letters_117 = 'AÁÄBCČDĎEÉFGHChIÍJKLĹĽMNŇOÓÔPQRŔSŠTŤUÚVWXYÝZŽaáäbcčdďeéfghchiíjklĺľmnňoóôpqrŕsštťuúvwxyýzžä@%řě01234'
_letters_134 = 'AÁÄBCČDĎEÉFGHChIÍJKLĹĽMNŇOÓÔPQRŔSŠTŤUÚVWXYÝZŽaáäbcčdďeéfghchiíjklĺľmnňoóôpqrŕsštťuúvwxyýzžä@%řě0123456789'
_letters_ipa_134 = 'ɑɐɒæɓʙβɔɕçɗɖ'
_letters_178 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
_letters_ipa = "ɑɐɒæɓʙβɔɕçɗɖðʤəɘɚɛɜɝɞɟʄɡɠɢʛɦɧħɥʜɨɪʝɭɬɫɮʟɱɯɰŋɳɲɴøɵɸθœɶʘɹɺɾɻʀʁɽʂʃʈʧʉʊʋⱱʌɣɤʍχʎʏʑʐʒʔʡʕʢǀǁǂǃˈˌːˑʼʴʰʱʲʷˠˤ˞↓↑→↗"


# Export all symbols:
symbols = [_pad] + list(_punctuation) + list(_letters) + list(_letters_ipa)

# Special symbol ids
SPACE_ID = symbols.index(" ")
def set_symbols(version=216):
	global symbols
	if version==216:
		symbols = [_pad] + list(_punctuation) + list(_letters_216) + list(_letters_ipa)
		#print(version,symbols)		
	elif version==217:
		symbols = [_pad] + list(_punctuation) + list(_letters_217) + list(_letters_ipa)
		#print(version,symbols)		
	elif version==221:
		symbols = [_pad] + list(_punctuation) + list(_letters_221) + list(_letters_ipa)
		#print(version,symbols)		
	elif version==117:
		symbols = [_pad] + list(_punctuation) + list(_letters_117)
	elif version==134:
		symbols = [_pad] + list(_punctuation) + list(_letters_134) + list(_letters_ipa_134)
		print('*'*40)
		print(version,symbols)
		print('*'*40)
	elif version==178:
		symbols = [_pad] + list(_punctuation) + list(_letters_178)
		#print(version,symbols)
	else:
		symbols = [_pad] + list(_punctuation) + list(_letters) + list(_letters_ipa)
		#print(version,symbols)
	return(symbols)
	
def get_symbols(version=216):
	global symbols
	if version==216:
		return([_pad] + list(_punctuation) + list(_letters_216) + list(_letters_ipa))
	elif version==217:
		return([_pad] + list(_punctuation) + list(_letters_217) + list(_letters_ipa))
	elif version==221:
		return([_pad] + list(_punctuation) + list(_letters_221) + list(_letters_ipa))
	else:
		return([_pad] + list(_punctuation) + list(_letters) + list(_letters_ipa))
