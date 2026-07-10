from pydantic import BaseModel, ConfigDict, Field


class Location(BaseModel):
    """Represents a geographic location mentioned in a news article."""

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    country: str = Field(
        ...,
        min_length=1,
        description="Country name",
    )

    state: str | None = Field(
        default=None,
        description="State or province",
    )

    city: str | None = Field(
        default=None,
        description="City or locality",
    )