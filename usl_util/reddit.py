import re

__valid_username_regex = r'^[A-Za-z0-9-_]{3,20}$'

def trim_and_validate_reddit_username(reddit_username: str) -> str:
    """
    Validate a Reddit username by removing its prefix, and verifying it matches Reddit's username requirements.

    A valid Reddit username is 3-20 characters long, and contains only alphanumeric characters, as well as - and _.

    If the username provided to this function is invalid, an exception is thrown.
    :return: The username, with its prefix removed, if the username is valid.
    """
    # Trim the /u/ or u/ prefix from the username, if present.
    trimmed_username = reddit_username.replace("/u/", "u/").replace("u/", "")

    if not re.match(__valid_username_regex, trimmed_username):
        raise RuntimeError('Invalid Reddit username provided.')

    return trimmed_username
