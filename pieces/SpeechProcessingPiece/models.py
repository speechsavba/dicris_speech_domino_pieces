from pydantic import BaseModel, Field

class InputModel(BaseModel):
	y: str = Field(
		default='http://speech.savba.sk/DiCris/stress/zrab_crisis_3_0003.wav',
		title="audio to asses",
		description='path to audio or URL to audio or sound read with librosa library and converted to a base64 encoded string.'
	)
	sr: int = Field(
		default=16000,
		title="Sampling frequency of sound",
		description="Sampling frequency of sound (integer)",
		# json_schema_extra={"from_upstream": "always"}
	)

class OutputModel(BaseModel):
	voicestresslevel: float = Field(
		default=0.0,
		description="Stress level in range: min 0.0 - 1.0 max  (float)"
	)
	textstresslevel: str = Field(
		default='NORMAL',
		description="Stress level from text - NORMAL, CAUTION or ALERT. I case of error: UNKNOWN"
	)
	text: str = Field(
		default='',
		description="ASR text from audio"
	)
	speaker_id: str = Field(
		default='',
		description="Speaker ID from voice"
	)

