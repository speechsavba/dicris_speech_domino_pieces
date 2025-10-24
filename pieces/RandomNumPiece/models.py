from pydantic import BaseModel, Field


class InputModel(BaseModel):
    max_num: float = Field(
        default=100.0,
        title="Maximum",
        description="Maximum for random generator (float)",
        # json_schema_extra={"from_upstream": "always"}
    )
    min_num: float = Field(
        default=0.0,
        title="Minimum",
        description="Minimum for random generator (float)",
        # json_schema_extra={"from_upstream": "always"}
    )


class OutputModel(BaseModel):
    """
    IsDay Piece Output Model
    """
    number: float = Field(
        default=0.0,
        description="Random number (float)"
    )
