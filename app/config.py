from os import access
from pydantic import BaseSettings



class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    #pull env variables from env file but we will not do something like this in prod

    class Config:
        env_file = ".env"

settings = Settings()