from os import getenv
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class USLAPIRedditSettings(BaseModel):
    """
    Settings used for configuring Reddit API access.
    """
    client_id: str = Field(
        description="The OAuth client ID for the Reddit application."
    )

    client_secret: str = Field(
        description="The OAuth client secret for the Reddit application."
    )

    username: str = Field(
        description="The username of the Reddit account where the application is registered."
    )

    password: str = Field(
        description="The password of the Reddit account where the application is registered."
    )

    user_agent: str = Field(
        description="The user agent sent to Reddit when making API requests.",
        default='UniversalScammerList REST API by u/HWSUKMods'
    )

    usl_subreddit: str = Field(
        description='The subreddit from which USL wiki pages should be read.',
        default='UniversalScammerList'
    )


class USLAPISecuritySettings(BaseModel):
    """
    Settings used for securing access to the API endpoints.
    """
    api_key: str = Field(
        description="The API key used for securing access to the API endpoints."
    )


class USLAPISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="USL_API_", env_file=".env", env_file_encoding="utf-8"
    )

    reddit: USLAPIRedditSettings
    security: USLAPISecuritySettings

    local_dev: bool = Field(
        description='If true, then debug logging and documentation endpoints will be enabled.',
        default=False
    )


__config_location = getenv('USL_API_CONFIG_FILE_LOCATION', './config.json')

if Path(__config_location).exists():
    print(f'Loading configuration from {__config_location}')

    with open(__config_location, 'r') as f:
        config = USLAPISettings.model_validate_json(f.read())
else:
    print(f'Loading configuration from environment variables.')

    config = USLAPISettings()
