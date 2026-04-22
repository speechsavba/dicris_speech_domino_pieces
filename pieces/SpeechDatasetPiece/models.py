from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional

class InputModel(BaseModel):
	#dataset: DatasetFile = Field(default='', title='Wav name')
	pass

class OutputModel(BaseModel):
	file_path: Optional[str] = Field(default=None, title='File path')
