from textwrap import dedent

from fastapi import APIRouter, status, HTTPException, Security
from loguru import logger

import usl_services.usl as usl_service
from usl_models.v1.request import USLV1FetchRequest
from usl_models.v1.response import USLV1FetchResponse
from usl_util.reddit import trim_and_validate_reddit_username
from usl_util.security import validate_api_key

router = APIRouter(prefix='/v1/usl', tags=['usl'])


@router.get(
    '',
    response_model=USLV1FetchResponse,
    status_code=status.HTTP_200_OK,
    summary='Fetch User Bans from USL Database',
    description=dedent("""
    Fetch user info from the Universal Scammer List wiki pages, parse the markdown and return a model that represents the 
    searched user's active bans, as well as the result of searching the database.
    
    A user is considered to have an active ban if they meet the following criteria:
    
    * They have a wiki page in the database. If no page exists they are not considered banned.
    * They have a ban from any subreddit with a tag (e.g. #scammer) that has not been subsequently rescinded by an unban.
    """)
)
async def usl_v1_fetch_user_bans(
        request: USLV1FetchRequest,
        _: str = Security(validate_api_key)
) -> USLV1FetchResponse:
    try:
        trimmed_username = trim_and_validate_reddit_username(request.reddit_username)
    except RuntimeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid Reddit username provided.'
        )

    logger.debug(f'Fetching USL user bans for Reddit username {trimmed_username}.')

    return await usl_service.fetch_usl_bans_for_user(trimmed_username)