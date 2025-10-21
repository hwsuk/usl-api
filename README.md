# Universal Scammer List API

This application provides programmatic access to the [Universal Scammer List](https://reddit.com/r/UniversalScammerList) database via a REST API.

> Note: This application is not officially sanctioned by the r/UniversalScammerList moderation team, and the authors have no affiliation with them.

## Background

The Universal Scammer List is a widely-used database of known trade scammers on Reddit. Participating trading subreddits can add users to the list if that user has carried out a scam or engaged in suspicious behaviour, allowing other subreddits to take proactive action to safeguard their communities against known scammers.

The USL is backed by a series of Reddit wiki pages, containing Markdown that would need to be parsed manually to use the USL as part of an automation workflow. There is no API exposed by the USL mod team that enables a developer to read from the USL - this unofficial application parses the aforementioned Markdown pages into a JSON object which represents a user's ban history on the USL.

### How it works

- The wiki page for the queried Reddit user is looked up (`/r/UniversalScammerList/wiki/database/$username`).
  - If no wiki page for the searched user exists, then the user is assumed not to be banned on the USL.
- Each entry in the wiki page is parsed into the following fields, known collectively as an "action":
  - The Reddit username against whom the action was taken.
  - The action that was taken (banned/unbanned).
  - The time at which the action was taken.
  - The subreddit that carried out the action.
  - Any context provided for the action.
  - Whether tags were added or removed.
  - The tags added or removed as part of this action.
- The parsed actions are sorted by their timestamps, earliest to latest.
- The actions are replayed in chronological order. For each parsed action:
  - If the action is "banned", the parsed ban is added to a tally.
  - If the action is "unbanned", any bans in the tally thus far are removed if the tags on the unban action match _all_ of the tags in a previous ban action.
- After all of the actions are replayed, if there are any bans remaining in the tally, the user is considered banned from the USL.

## Setup

See [config.example.json](./config.example.json) for a skeleton configuration - the application will read its configuration from a file named `config.json` in its working directory.

> If running in Docker, you will need to bind-mount your configuration to `/app/config.json`.

## Usage

> All requests must contain an `x-usl-api-key` header with the value set to that configured in `config.json / security.api_key`.

> If `config.json / local_dev` is set to `true`, an OpenAPI spec will be visible at `openapi.json`. You can view this spec in your browser using the `/docs` or `/redoc` endpoints.


### V1 - Fetch Bans from USL

Look for a user's USL page and parse it to see if they have an active ban.

#### Request Body

```json
{
  "reddit_username": "u/ExampleRedditUser"
}
```

#### Response Body

````json
{
  "searched_username": "ExampleRedditUser",
  "is_banned": true,
  "active_bans": [
    {
      "ban_timestamp": "2022-11-03T00:00:00",
      "actioning_subreddit": "r/UniversalScammerList",
      "context": "Example context",
      "tags": ["#scammer"]
    }
  ],
  "search_result": "User was found in the USL database with active bans.",
  "wiki_page_link": "https://reddit.com/r/UniversalScammerList/wiki/database/ExampleRedditUser"}
````
