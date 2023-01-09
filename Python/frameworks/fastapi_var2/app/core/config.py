from starlette.config import Config

config = Config(".env")

DATABASE_URL = config("DATABASE_URL", cast=str, default='postgresql://fastapi_user:fastapi_user@localhost:5432/fastapi_docker_db')
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=15)
SECRET_KEY = config("SECRET_KEY", cast=str, default='4b141a430b39cf4b7cc77436ab15a00f58215bd7f47fcc0e91ce98dffdef9380')
ALGORITHM = config("ALGORITHM", cast=str, default='HS256')  # openssl rand -hex 32
