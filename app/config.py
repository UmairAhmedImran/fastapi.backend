from pydantic import BaseSettings

class Settings(BaseSettings):
    database_username: str
    database_port: str
    database_hostname: str
    database_password:str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minute: str

    class Config:
        env_file = '.env'

Settings = Settings()
