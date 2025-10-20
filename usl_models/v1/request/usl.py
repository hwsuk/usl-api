from typing import Annotated

from pydantic import BaseModel, Field


class USLV1FetchRequest(BaseModel):
    reddit_username: Annotated[
        str,
        Field(
            description='The Reddit username to look up. If the username begins with u/ or /u/, it will be '
                        'automatically reformatted.'
        )
    ]
