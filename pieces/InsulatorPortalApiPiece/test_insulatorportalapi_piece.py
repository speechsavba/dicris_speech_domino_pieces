from domino.testing import piece_dry_run


def test_insulatorportalapi_piece():
	input_data = dict(
		contamination=2.8,
	)

	piece_output = piece_dry_run(
		piece_name="InsulatorPortalApiPiece",
		input_data=input_data
	)
	assert 'returned_status' in piece_output
