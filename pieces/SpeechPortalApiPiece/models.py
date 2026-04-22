from pydantic import BaseModel, Field


class InputModel(BaseModel):
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
	name: str = Field(
		default="Voiceprocessing",
		title="Model Name",
		description="Name of the model whose status will be sent."
	)
	portal_url: str = Field(
		default="https://dicris.sk:8000",
		title="Portal URL",
		description="URL of the Portal API endpoint (defaults to localhost)."
	)


class OutputModel(BaseModel):
	returned_status: dict = Field(
		description="JSON response returned by the Portal API."
	)