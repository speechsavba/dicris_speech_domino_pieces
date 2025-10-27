from pydantic import BaseModel, Field

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
	top_class: str = Field(default='unknown',description="Top Sound class"),
	top_prob: float = Field(default=0.0, description="Probability of Top Sound class"),
	top10: str = Field(default='unkown', description="Top 10 of sound classes"
	)

