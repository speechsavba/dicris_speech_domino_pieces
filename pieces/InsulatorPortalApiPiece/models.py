from pydantic import BaseModel, Field


class InputModel(BaseModel):
	contamination: float = Field(
		default=0.0,
		description="Contamination of insulator from sound (float)"
	)
		
	name: str = Field(
		default="Insulator",
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