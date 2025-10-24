from pydantic import BaseModel, Field
from enum import Enum

class InputModel(BaseModel):
	y: str = Field(
		default='http://speech.savba.sk/DiCris/echo_20250716_113400_7B-3.wav',
		title="audio to asses",
		description='path to audio or URL to audio or sound read with librosa library and converted to a base64 encoded string.'
	)
	sr: int = Field(
		default=192000,
		title="Sampling frequency of sound",
		description="Sampling frequency of sound (integer)",
		# json_schema_extra={"from_upstream": "always"}
	)

class OutputModel(BaseModel):
	contamination: float = Field(
		default=0.0,
		description="Contamination of insulator from sound (float)"
	)

