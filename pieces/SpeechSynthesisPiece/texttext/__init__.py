""" from https://github.com/keithito/tacotron """
from texttext import cleaners
from texttext.symbols import symbols, set_symbols, get_symbols


# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}

def text_to_sequence(text, cleaner_names,version=221):
  '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
    Args:
      text: string to convert to a sequence
      cleaner_names: names of the cleaner functions to run the text through
    Returns:
      List of integers corresponding to the symbols in the text
  '''
  print('setting symbols:',version)
  symbols=set_symbols(version=version)
  _symbol_to_id = {s: i for i, s in enumerate(symbols)}
  _id_to_symbol = {i: s for i, s in enumerate(symbols)}
  #print(symbols)
  		
  sequence = []
  wrong_symbols=set()
  #print('-------------------+++++++++++++++++++')
  #print(text)
  clean_text = _clean_text(text, cleaner_names)
  #print(clean_text)	
  #print('-------------------+++++++++++++++++++')
  for symbol in clean_text:
    try:	
        symbol_id = _symbol_to_id[symbol]
        sequence += [symbol_id]
    except:
        print('wrong character')
        wrong_symbols.add(symbol)				
  #print(sequence)
  return sequence,wrong_symbols

def text_to_sequence_orig(text, cleaner_names):
  '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
    Args:
      text: string to convert to a sequence
      cleaner_names: names of the cleaner functions to run the text through
    Returns:
      List of integers corresponding to the symbols in the text
  '''
  sequence = []

  clean_text = _clean_text(text, cleaner_names)
  for symbol in clean_text:
    try:	
        symbol_id = _symbol_to_id[symbol]
        sequence += [symbol_id]
    except:
        print('wrong character')
  return sequence


def cleaned_text_to_sequence(cleaned_text):
  '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
    Args:
      text: string to convert to a sequence
    Returns:
      List of integers corresponding to the symbols in the text
  '''
  sequence = [_symbol_to_id[symbol] for symbol in cleaned_text]
  return sequence


def sequence_to_text(sequence):
  '''Converts a sequence of IDs back to a string'''
  result = ''
  for symbol_id in sequence:
    s = _id_to_symbol[symbol_id]
    result += s
  return result


def _clean_text(text, cleaner_names):
  for name in cleaner_names:
    cleaner = getattr(cleaners, name)
    if not cleaner:
      raise Exception('Unknown cleaner: %s' % name)
    #print('cleaner',text)
    text = cleaner(text)
    #print(text)		
  return text
