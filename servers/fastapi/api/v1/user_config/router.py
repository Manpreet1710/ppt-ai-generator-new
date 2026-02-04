from fastapi import APIRouter, HTTPException
from models.user_config import UserConfig
from utils.user_config import get_user_config, save_user_config

USER_CONFIG_ROUTER = APIRouter(prefix="/user-config", tags=["User Config"])

@USER_CONFIG_ROUTER.get("", response_model=UserConfig)
def get_config():
    try:
        return get_user_config()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@USER_CONFIG_ROUTER.post("", response_model=UserConfig)
def save_config(user_config: UserConfig):
    try:
        save_user_config(user_config)
        return get_user_config()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
