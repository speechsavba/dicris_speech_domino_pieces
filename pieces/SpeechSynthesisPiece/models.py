from pydantic import BaseModel, Field


class InputModel(BaseModel):
	text: str = Field(
		default='Dnes je piatok a idem domov.',
		title="Text to synthesize",
		description='Text to synthesize in utf-8 encoding'
	)
	voice: str = Field(
		default='bajn',
		title="Voice to use for synthesis. Available: bajn, hamar3_ore",
		description="Sampling frequency of sound (integer)",
	)

class OutputModel(BaseModel):
	 output_audiofile_path: str = Field(description='Output audiofile path of the synthesized speech.')

