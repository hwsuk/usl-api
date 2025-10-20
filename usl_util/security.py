from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from usl_config import config

api_key_header = APIKeyHeader(name='x-usl-api-key')


def validate_api_key(api_key_header_value: str = Security(api_key_header)) -> str:
    """
    Validate that the API key provided in the request matches the configured key.

    If the provided API key does not match, a 401 error is returned to the client.
    :param api_key_header_value: The value of the configured API key header.
    :return: The contents of the API key header, if the provided API key matches the configured key.
    """
    if api_key_header_value == config.security.api_key:
        return api_key_header_value

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
