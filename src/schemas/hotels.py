from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str
    #name: str
    location: str

class HotelPATCH(BaseModel):
    title: str | None = Field(None)
    #name: str | None = Field(None)
    location: str | None = Field(None)
