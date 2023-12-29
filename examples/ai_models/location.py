from marvin import ai_fn, ai_model
from pydantic import BaseModel, Field


@ai_model(client=client)
class Location(BaseModel):
    city: str
    state_abbreviation: str = Field(
        ..., description="The two-letter state abbreviation"
    )


st.write(Location("The Big Apple"))
