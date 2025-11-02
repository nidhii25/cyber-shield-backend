from pydantic import BaseModel, HttpUrl

class PhishingDetectionRequest(BaseModel):
    url:HttpUrl

