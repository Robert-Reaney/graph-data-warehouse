from pydantic import BaseModel


class HealthResponse(BaseModel):
    """
    HealthResponse is a string telling the consumer the API is healthy.
    """
    message: str

class DacisId(BaseModel):
    id: str
