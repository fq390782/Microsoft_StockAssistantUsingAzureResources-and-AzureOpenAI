from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from enum import Enum
from os import getenv
from dotenv import load_dotenv
load_dotenv()   # For another libraries having more security conditions...


class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',  # extra=forbid (default)
        frozen=True  
    )

    # Sql Settings
    SQL_HOST: str               = getenv('SQL_HOST', 'localhost')
    SQL_USER: str               = getenv('SQL_USER', 'postgres')
    SQL_PORT: int               = 5432
    SQL_PASSWORD: Optional[str] = getenv('SQL_PASSWORD')
    SQL_DATABASE: str           = getenv('SQL_DATABASE', 'postgres')
    
    # Redis Settings
    REDIS_HOST: str             = getenv('REDIS_HOST', 'localhost')
    REDIS_PORT: int             = int(getenv('REDIS_PORT', 6379))
    REDIS_PASSWORD: Optional[str] = getenv('REDIS_PASSWORD')
    REDIS_DATABASE: int         = 0

    # Naver API
    NAVER_API_CLIENT_ID: Optional[str]    = getenv('NAVER_API_CLIENT_ID')
    NAVER_API_SECRET_KEY: Optional[str]   = getenv('NAVER_API_SECRET_KEY')

    # Azure OpenAI
    AZURE_OPENAI_KEY: Optional[str]         = getenv('AZURE_OPENAI_KEY')
    AZURE_OPENAI_API_VERSION: Optional[str] = getenv('AZURE_OPENAI_API_VERSION')
    AZURE_OPENAI_ENDPOINT: Optional[str]    = getenv('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_MODEL: Optional[str]       = getenv('AZURE_OPENAI_MODEL')
    AZURE_OPENAI_DEPLOYMENT: Optional[str]  = getenv('AZURE_OPENAI_DEPLOYMENT')


api_settings = ApiSettings()

