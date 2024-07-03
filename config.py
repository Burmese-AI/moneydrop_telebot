from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    webhook_url: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()