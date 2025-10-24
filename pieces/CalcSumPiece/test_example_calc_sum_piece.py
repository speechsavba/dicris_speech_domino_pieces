from domino.testing import piece_dry_run

def test_example_calc_sum_piece():
    input_data = dict(
        a_num=5,
        b_num=2
    )
    output_data = piece_dry_run(
        "CalcSumPiece",
        input_data,
    )

    assert output_data["message"] is not None
