import datetime
import re
from typing import Optional

import prawcore.exceptions
from fastapi import HTTPException, status
from loguru import logger

import usl_services.reddit as reddit_service
from usl_models.v1.parser import USLV1BanAction
from usl_models.v1.response import USLV1FetchResponse, USLV1FetchResponseSearchResult, USLV1FetchResponseBanInfo

__dt_format = '%Y-%m-%d %H:%M %Z'
__action_line_regex = r'^\*\s(u\/[A-Za-z0-9-_]{3,20}) was (banned|unbanned) on (\d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC) from (r\/[A-Za-z0-9-_]*) with context - (.* -)?\s?Tags (Added|Removed): (.*)$'

async def fetch_usl_bans_for_user(username: str) -> USLV1FetchResponse:
    """
    Fetch the USL bans for the specified user.
    :param username: The username, without the u/ prefix, to fetch bans for.
    :return: A model representing the user's ban status.
    """
    logger.debug(f'Fetching wiki page for user {username}.')

    try:
        wiki_page_link, wiki_md = await reddit_service.fetch_usl_user_page_markdown(username)
    except prawcore.exceptions.NotFound:
        logger.debug(f'No wiki page found for user {username} - assuming not banned.')

        return USLV1FetchResponse(
            searched_username=username,
            is_banned=False,
            search_result=USLV1FetchResponseSearchResult.NOT_FOUND
        )

    logger.debug(f'Parsing and replaying ban actions for user {username}.')

    parsed_actions = [
        parse_markdown_line_to_action(line)
        for line in wiki_md.splitlines()
        if re.match(__action_line_regex, line)
    ]

    if len(parsed_actions) == 0:
        logger.error(f'Markdown page found for user {username}, but no lines could be parsed into actions.')

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='An error occurred when parsing the specified user\'s bans.'
        )

    active_bans = replay_parsed_actions(parsed_actions)

    if len(active_bans) == 0:
        return USLV1FetchResponse(
            searched_username=username,
            is_banned=False,
            search_result=USLV1FetchResponseSearchResult.FOUND_WITH_NO_ACTIVE_BANS,
            wiki_page_link=wiki_page_link
        )
    else:
        ban_info = [
            USLV1FetchResponseBanInfo(
                ban_timestamp=active_ban.action_timestamp,
                actioning_subreddit=active_ban.actioning_subreddit,
                context=active_ban.context,
                tags=active_ban.tags
            )
            for active_ban in active_bans
        ]

        return USLV1FetchResponse(
            searched_username=username,
            is_banned=True,
            search_result=USLV1FetchResponseSearchResult.FOUND_WITH_ACTIVE_BANS,
            active_bans=ban_info,
            wiki_page_link=wiki_page_link
        )

def replay_parsed_actions(actions: list[USLV1BanAction]) -> list[USLV1BanAction]:
    """
    Replay the parsed actions in chronological order to create a final list of active bans for a given user.
    :param actions: The parsed actions to replay.
    :return: A list of ban information representing any active bans for a given user.
             If the user has no active bans, the list will be empty.
    """
    chronological_actions = sorted(actions, key=lambda action: action.action_timestamp)

    active_bans: list[USLV1BanAction] = []

    for action in chronological_actions:
        # If this action is a ban, add them to the active bans list
        if action.action == "banned":
            active_bans.append(action)

        # If this action is an unban, remove any bans that exactly the tags of this unban action
        if action.action == "unbanned":
            active_bans = [
                active_ban for active_ban in active_bans if active_ban.tags != action.tags
            ]

    return active_bans

def parse_markdown_line_to_action(line: str) -> Optional[USLV1BanAction]:
    """
    Parse a single line of Markdown into a representation of the action taken against the user.
    :param line: The line to parse.
    :return: A representation of the action taken against the user, if the line can be parsed, otherwise None.
    """
    matches = re.search(__action_line_regex, line)

    if not matches:
        return None

    return USLV1BanAction(
        username=matches.group(1),
        action=matches.group(2),
        action_timestamp=datetime.datetime.strptime(matches.group(3), __dt_format),
        actioning_subreddit=matches.group(4),
        context=matches.group(5),
        tags_modification=matches.group(6),
        tags=matches.group(7).split(', ')
    )
