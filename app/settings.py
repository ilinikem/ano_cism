import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../.env")
    )

    def get_db_url(self):
        env = os.getenv("ENVIRONMENT", "dev")
        if env == "prod":
            self.DB_HOST = "db"
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")


settings = Settings()

# import os
#
# from pydantic_settings import BaseSettings, SettingsConfigDict
#
#
# class Settings(BaseSettings):
#     DB_USER: str
#     DB_PASSWORD: str
#     DB_HOST: str
#     DB_PORT: int
#     DB_NAME: str
#
#     model_config = SettingsConfigDict(
#         extra='ignore',
#         env_file_encoding='utf-8'
#     )
#     def get_db_url(self) -> str:
#         return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
#                 f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
#
#
# env = os.getenv("ENVIRONMENT", "dev")
# if env == "prod":
#     settings = Settings(_env_file=".env.prod")
# else:
#     settings = Settings(_env_file=".env")
