from domino.testing import piece_dry_run


def test_example_random_num_piece():
    input_data = dict(
        max_num=100
    )
    print(input_data)
    output_data = piece_dry_run(
        "RandomNumPiece",
        input_data,
    )
    print(output_data)
    assert output_data["number"] is not None

#test_example_calc_sum_piece()
