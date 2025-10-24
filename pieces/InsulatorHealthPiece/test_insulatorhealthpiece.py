from domino.testing import piece_dry_run
from pathlib import Path
#from pieces.InsulatorHealthPiece.piece import NormalizedPipeline

# Open test image and convert to base64 string using Pillow
audio_path = str(Path(__file__).parent / "test_audio/echo_20250716_113400_7B-3.wav")
audio_url = 'http://speech.savba.sk/DiCris/echo_20250716_113400_7B-3.wav'
audio_url = 'http://speech.savba.sk/DiCris/echo_20250715_094400_7B-0.wav'


def test_insulatorcontaminationpiece():
    input_data = dict(
        #y=audio_path,
		y=audio_url,
        sr=-1,
    )
    piece_output = piece_dry_run(
        piece_name="InsulatorHealthPiece",
        input_data=input_data
    )
    assert piece_output is not None
    assert piece_output["contamination"] is not None
    assert piece_output["contamination"]!=-1

#if __name__ == "__main__":
#	test_insulatorcontaminationpiece()