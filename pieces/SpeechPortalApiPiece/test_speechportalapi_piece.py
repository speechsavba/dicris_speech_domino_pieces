from domino.testing import piece_dry_run


def test_speechportalapi_piece():
	input_data = dict(
		voicestresslevel=0.8,
		textstresslevel='NORMAL',
		text='Toto je ukážka ASR textu',
		speaker_id='VR'
	)

	piece_output = piece_dry_run(
		piece_name="SpeechPortalApiPiece",
		input_data=input_data
	)
	assert 'returned_status' in piece_output
