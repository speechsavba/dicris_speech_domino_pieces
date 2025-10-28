from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional

class DatasetFile(str, Enum):
	wav1 = "http://speech.savba.sk/DiCris/echo_20250716_113400_7B-3.wav"
	wav2 = "http://speech.savba.sk/DiCris/echo_20250715_094400_7B-0.wav"
	wav3 = "http://speech.savba.sk/DiCris/echo_20250716_104301_D5.wav"
	wav4 = "random"

class InputModel(BaseModel):
	dataset: DatasetFile = Field(default='', title='Wav name')

class OutputModel(BaseModel):
	file_path: Optional[str] = Field(default=None, title='File path')
