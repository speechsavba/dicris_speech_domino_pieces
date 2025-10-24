from pydantic import BaseModel, Field


class InputModel(BaseModel):
	"""
	Sum Piece Input Model
	"""

	a_num: float = Field(
		default=1.0,
		description="float",
	),
	b_num: float = Field(
		default=1.0,
		description="float",
	)


class OutputModel(BaseModel):
	"""
	Sleep Piece Output Model
	"""
	message: str = Field(
		description="Sum of a and b"
	)
