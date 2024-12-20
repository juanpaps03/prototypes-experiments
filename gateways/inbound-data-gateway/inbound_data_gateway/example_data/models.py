from typing import List, Any

from pydantic import BaseModel, EmailStr, field_validator


# TODO: All this models (except the Response ones) should be in a shared models library.

class ImmutableBaseModel(BaseModel):
    class Config:
        allow_mutation = False
        allow_population_by_field_name = True


class Identifier(ImmutableBaseModel):
    value: str

    @classmethod
    @field_validator("value")
    def check_str_not_empty(cls: Any, v: str) -> Any:
        if v is None or v == "":
            raise ValueError("Please specify a valid value")
        return v


class ExampleDataPayload(ImmutableBaseModel):

    identifiers: List[Identifier]
    email: EmailStr


class ExampleModelResponse(ImmutableBaseModel):
    email: EmailStr