from pydantic_settings import BaseSettings  


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str  
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"
        
settings = Settings() 
#instance of the Settings class, which will read the environment variables from the .env file and make them available as attributes of the settings object.

