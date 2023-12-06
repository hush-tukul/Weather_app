import os

from pydantic import BaseModel, Field, field_validator


class UploadedFile(BaseModel):
    link: str = Field(..., alias="src")

    @field_validator("link")
    def link_validator(cls, value: str):
        return os.getenv('BASE_TELEGRAPH_API_LINK').format(endpoint=value)