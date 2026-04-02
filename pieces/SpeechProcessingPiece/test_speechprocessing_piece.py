from domino.testing import piece_dry_run
import sys

def test_speechprocessing_piece():
	input_data = dict(
		#y='http://speech.savba.sk/DiCris/stress/zrab_crisis_1_0016.wav',
		y='http://speech.savba.sk/DiCris/stress/vr_crisis_1_0001.wav',
		#y='http://speech.savba.sk/DiCris/stress/mrst_crisis_1_0109.wav',
		#y='http://speech.savba.sk/DiCris/stress/zrab_crisis_3_0018.wav',
		#y='http://speech.savba.sk/DiCris/echo_20250715_094400_7B-0.wav',


		sr=16000,
	)

	piece_output = piece_dry_run(
		piece_name="SpeechProcessingPiece",
		input_data=input_data
	)
	print(piece_output)
	assert piece_output is not None
	assert piece_output["voicestresslevel"] is not None
	assert piece_output["textstresslevel"] is not None
	assert piece_output["text"] is not None
	assert piece_output["speaker_id"] is not None
