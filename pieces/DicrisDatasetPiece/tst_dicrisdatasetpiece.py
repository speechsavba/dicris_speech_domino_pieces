from domino.testing import piece_dry_run


def test_dicrisdatasetpiece():
    dataset = 'random'
    input_data = dict(
        dataset=dataset
    )

    piece_output = piece_dry_run(
        piece_name="DicrisDatasetPiece",
        input_data=input_data
    )
    assert 'file_path' in piece_output
