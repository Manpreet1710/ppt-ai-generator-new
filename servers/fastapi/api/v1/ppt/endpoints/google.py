from typing import Annotated, List, Dict
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel

from utils.available_models import list_available_google_models

class GoogleAPIKey(BaseModel):
    api_key: str

GOOGLE_ROUTER = APIRouter(prefix="/google", tags=["Google"])


@GOOGLE_ROUTER.post("/models/available", response_model=List[Dict])
async def get_available_models(body: GoogleAPIKey):
    try:
        return await list_available_google_models(body.api_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
