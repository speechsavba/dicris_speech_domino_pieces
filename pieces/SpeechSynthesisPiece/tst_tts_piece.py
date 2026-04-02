from domino.testing import piece_dry_run


def test_tts_piece():
    import sys,os
    sys.path.append(os.path.dirname(os.path.realpath(__file__)))
    input_data = dict(
        text='mama bude zajtra doma? Hurá!',
		voice='crisis3b'
    )

    piece_output = piece_dry_run(
        piece_name="TTSPiece",
        input_data=input_data
    )
    print(piece_output)
    assert 'output_audiofile_path' in piece_output
