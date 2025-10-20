import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class USLV1BanAction(BaseModel):
    """
    Represents the result of parsing a single line of a user's wiki page into an "action".
    """
    username: str = Field(
        description='The username fetched from the log line, including the prefix.'
    )

    action: Literal["banned", "unbanned"] = Field(
        description='The action taken against this user (banned or unbanned).'
    )

    action_timestamp: datetime.datetime = Field(
        description='The time at which the action was taken.'
    )

    actioning_subreddit: str = Field(
        description='The name of the subreddit which took this action.'
    )

    context: Optional[str] = Field(
        description='Any context that the actioning subreddit provided to explain the action.'
    )

    tags_modification: Literal["Added", "Removed"] = Field(
        description='Whether tags were added or removed as part of this action.'
    )

    tags: list[str] = Field(
        description='The list of tags added/removed as part of this action.'
    )
