from praw import Reddit

from usl_config import config

__reddit_client = Reddit(
    client_id=config.reddit.client_id,
    client_secret=config.reddit.client_secret,
    username=config.reddit.username,
    password=config.reddit.password,
    user_agent=config.reddit.user_agent,
    check_for_async=False
)


async def fetch_usl_user_page_markdown(username: str) -> tuple[str, str]:
    """
    Fetch the URL and the raw markdown for a user's ban page from the configured USL subreddit's wiki pages.

    If the specified user's wiki page is not found in the configured subreddit, an exception is thrown.
    :param username: The username to fetch the ban page for, without the u/ prefix.
    :return: The URL and raw markdown for the resolved wiki page, if it exists.
    """
    wiki_page = __reddit_client.subreddit(config.reddit.usl_subreddit).wiki[f'database/{username}']

    wiki_page_url = f'https://reddit.com/r/{config.reddit.usl_subreddit}/wiki/database/{username}'

    return wiki_page_url, wiki_page.content_md
