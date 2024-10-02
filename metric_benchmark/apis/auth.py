import os

from dotenv import load_dotenv
from fastapi import Header, HTTPException, status

load_dotenv()

API_KEY = os.getenv("API_KEY", "")


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key"
        )
