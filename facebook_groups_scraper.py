import asyncio
import random
from datetime import datetime, timedelta
from typing import List, AsyncIterator

from facebook_scraper import get_posts, Post

from logger import logger


class FacebookGroupsScraper:
    def __init__(self, username, password):
        self._default_config = {
            'credentials': (username, password),
            'extra_info': False,
            'page_limit': 10,
            'options': {
                'comments': False,
                'reactors': False,
                "allow_extra_requests": False,
                "posts_per_page": 10
            }
        }

    async def get_posts(self, group_ids: List[str]) -> AsyncIterator[Post]:
        for group_id in group_ids:
            logger.info(f"Getting posts from group id - {group_id}")

            posts = get_posts(group=group_id, **self._default_config)
            for post in posts:
                logger.info(f"Found post id - {post['post_id']}")

                if await self._should_ignore_post(post):
                    continue

                yield post

            sleep_duration = random.randint(1, 5)
            logger.info(f"Sleeping for {sleep_duration} seconds so the bot won't be detected")
            await asyncio.sleep(sleep_duration)

    async def _should_ignore_post(self, post):
        if not post['original_text']:
            logger.info("No text was found in post. Skipping it...")
            return True

        text_length = len(post['original_text'])
        if text_length > 600:
            logger.info(f"Text length in post is {text_length} and is too long. Skipping it...")
            return True

        now = datetime.now()
        time_diff = now - post['time']
        if time_diff <= timedelta(hours=4):
            logger.info(f"The post is from {post['time']} and is too old. Skipping it...")
            return True

        return False
