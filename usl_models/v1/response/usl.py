import datetime
from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class USLV1FetchResponseSearchResult(Enum):
    NOT_FOUND = "User was not found in the USL database."
    FOUND_WITH_NO_ACTIVE_BANS = "User was found in the USL database, but has no active bans."
    FOUND_WITH_ACTIVE_BANS = "User was found in the USL database with active bans."


class USLV1FetchResponseBanInfo(BaseModel):
    """
    Contains information about an active USL ban.
    """
    ban_timestamp: Annotated[
        datetime.datetime,
        Field(
            description='The timestamp at which this ban was enacted.'
        )
    ]

    actioning_subreddit: Annotated[
        str,
        Field(
            description='The subreddit that registered this ban.'
        )
    ]

    context: Annotated[
        Optional[str],
        Field(
            description='Any context provided by the banning subreddit to explain the ban.'
        )
    ] = None,

    tags: Annotated[
        list[str],
        Field(
            description='The list of tags assigned to this ban.'
        )
    ]

class USLV1FetchResponse(BaseModel):
    searched_username: Annotated[
        str,
        Field(
            description='The Reddit username which was looked up.'
        )
    ]

    is_banned: Annotated[
        bool,
        Field(
            description='True if, after tallying up bans and unbans from the USL database, the searched user is banned.'
        )
    ]

    active_bans: Annotated[
        list[USLV1FetchResponseBanInfo],
        Field(
            description='Information about active USL bans. A ban is considered active if it has not been overturned '
                        'by a subsequent unban.'
        )
    ] = []

    search_result: Annotated[
        USLV1FetchResponseSearchResult,
        Field(
            description='Describes the result of searching the USL database.'
        )
    ]

    wiki_page_link: Annotated[
        Optional[str],
        Field(
            description='If the searched user is found in the database, this field links to the underlying wiki page.'
        )
    ] = None