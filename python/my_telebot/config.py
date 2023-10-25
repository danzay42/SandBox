from dynaconf import Dynaconf
from pydantic import BaseModel


class Settings(BaseModel):
    NAME: str
    API_ID: int
    API_HASH: str
    TOKEN: str


settings = Dynaconf(
    envvar_prefix="TELEBOT",
    settings_files=['settings.yaml', '.secrets.yaml'],
)
settings = Settings(**settings.as_dict())
