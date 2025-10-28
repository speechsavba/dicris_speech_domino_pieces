from domino.testing import piece_dry_run

def test_insulatorcontamination_piece():
	input_data = dict(
		y='http://speech.savba.sk/DiCris/echo_20250715_094400_7B-0.wav',
		sr=192000,
	)

	piece_output = piece_dry_run(
		piece_name="InsulatorHealthPiece",
		input_data=input_data
	)
	assert piece_output is not None
	assert piece_output["contamination"] is not None
