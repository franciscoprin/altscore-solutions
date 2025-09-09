import os
import requests
from pydantic import BaseModel, HttpUrl, field_validator
from typing import Literal
from dotenv import load_dotenv


class RegisterRequest(BaseModel):
    alias: str
    country: str
    email: str
    apply_role: Literal["engineering", "data", "integrations"]

    @field_validator("country")
    @classmethod
    def validate_country_iso3(cls, v: str) -> str:
        # Normalize to uppercase and validate format: exactly 3 alphabetic characters
        v_norm = v.strip().upper()
        if not (len(v_norm) == 3 and v_norm.isalpha()):
            raise ValueError("Country must be an ISO 3166-1 alpha-3 code (3 letters, e.g., 'MEX', 'ESP', 'VEN', etc)")
        return v_norm


def register(url: HttpUrl, data: RegisterRequest):
    r = requests.post(url, json=data.dict())
    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        # Surface server-provided details to understand 4xx/5xx causes
        try:
            detail = r.json()
        except Exception:
            detail = r.text
        raise requests.HTTPError(f"{e} | Response body: {detail}") from e
    return r.json()

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
    BASE_URL = os.getenv('ALTSCORE_BASE_URL')
    REGISTER_PATH = "v1/register"
    url = f"{BASE_URL}/{REGISTER_PATH}"
    
    # Get registration details from environment variables with defaults
    data = RegisterRequest(
        alias=os.getenv('ALTSCORE_ALIAS'),
        country=os.getenv('ALTSCORE_COUNTRY'),
        email=os.getenv('ALTSCORE_EMAIL'),
        apply_role=os.getenv('ALTSCORE_APPLY_ROLE'),
    )

    response = register(
        url=url,
        data=data,
    )

    print(response)
