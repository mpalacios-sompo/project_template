from typing import Optional, List
from pydantic import BaseModel, Field

# Sample Classes
class Capital(BaseModel):
    city: str = Field(description="The city")
    country: str = Field(description="The country to which the city belongs")

class Response(BaseModel):
    response: List[Capital]
