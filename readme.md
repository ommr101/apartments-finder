# Facebook Apartments to Rent Scraper

This project aims to scrape data from various Facebook apartments to rent groups, extract relevant information such as rent, location, and number of rooms using OpenAI Function Calling API, filter it based on user requirements, and send the relevant apartments to a predefined Telegram group.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [License](#license)

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/ommr101/apartments-finder.git
   ```

2. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

## Configuration


The `apartments_finder_config.json` configuration file is used to define the settings and filters for the Apartments Finder program. It allows you to customize the parameters for apartment and post filtering.

```json
{
  "apartment_filters": [
    {
      "min_rooms": 2,
      "max_rooms": 3,
      "min_rent": 4000,
      "max_rent": 6000
    }
  ],
  "post_filters": [
    {
      "words_to_ignore_post_on": [
        "מחפש",
        "מחפשת"
      ],
      "max_post_minutes_difference": 150,
      "max_post_text_len": 800
    }
  ],
  "max_posts_to_enrich_in_run": 20,
  "posts_per_group_limit": 30,
  "total_posts_limit": 300
}
```

## Configuration Parameters

The configuration file consists of the following parameters:

### `apartment_filters`

- `min_rooms`: The minimum number of rooms an apartment must have.
- `max_rooms`: The maximum number of rooms an apartment must have.
- `min_rent`: The minimum rent amount for an apartment.
- `max_rent`: The maximum rent amount for an apartment.

These parameters define the filters for selecting apartments based on the number of rooms and rent range.

### `post_filters`

- `words_to_ignore_post_on`: A list of words to ignore when processing apartment posts. These words are typically irrelevant and can be used to exclude certain posts.
- `max_post_minutes_difference`: The maximum allowed time difference in minutes between the current time and the timestamp of an apartment post. Posts older than this time limit will be ignored.
- `max_post_text_len`: The maximum allowed length of the text content in an apartment post. Posts exceeding this limit will be ignored.

These parameters define the filters for selecting and processing apartment posts.

### `max_posts_to_enrich_in_run`

The maximum number of apartment posts to enrich in a single run of the program. Enriching refers to using OpenAI API to enrich a post with rent, location and rooms extracted from the post text.

### `posts_per_group_limit`

A limit on the number of apartment posts to process in a single Facebook group.

### `total_posts_limit`

The overall limit on the number of apartment posts to process. Once this limit is reached, the program will stop processing further posts.

### Environment Variables Configuration

Set up the following environment variables using a .env file (should be located in root directory)  or any other way according to the following table -

| Variable                             | Description                                                                                                            |
| ------------------------------------ |------------------------------------------------------------------------------------------------------------------------|
| `OPENAI_API_KEY`                     | The API key for the OpenAI service.                                                                                    |
| `TELEGRAM_BOT_API_KEY`               | The API key for the Telegram Bot service.                                                                              |
| `TELEGRAM_BOT_APARTMENTS_GROUP_CHAT_ID`         | The ID of the Telegram group to send the filtered apartments to.                                                       |
| `TELEGRAM_BOT_APARTMENTS_LOGS_GROUP_CHAT_ID`    | The ID of the Telegram group for logging purposes (Optional).                                                          |
| `FACEBOOK_USERNAME`                  | Your Facebook username.                                                                                                |
| `FACEBOOK_PASSWORD`                  | Your Facebook password.                                                                                                |
| `FACEBOOK_GROUPS`                    | A list of Facebook group ids to scrape apartment posts from, divided by comma. <br> E.g. - `132132,978213987,12358123` |


## Usage
Once all the configuration is set, run the main script:

   ```shell
   python main.py
   ```

## License

This project is licensed under the [MIT License](LICENSE). Feel free to modify and distribute this code as per the terms of the license.
