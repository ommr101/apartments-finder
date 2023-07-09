import asyncio
import random
from typing import AsyncIterator, List

from facebook_scraper import Post, get_posts

from apartments_finder.logger import logger


class FacebookGroupsScraper:
    def __init__(self, username, password):
        self._default_config = {
            "credentials": (username, password),
            "extra_info": False,
            "page_limit": 10,
            "options": {
                "comments": False,
                "reactors": False,
                "allow_extra_requests": False,
                "posts_per_page": 10
            },
            "group_sort_setting": 'CHRONOLOGICAL'
        }

    async def get_posts(
        self,
        group_ids: List[str],
        posts_per_group_limit: int = 3,
        total_posts_limit: int = 30,
    ) -> AsyncIterator[Post]:
        total_posts_counter = 0
        for group_id in group_ids:
            posts_per_group_counter = 0
            logger.info(f"Getting posts from group id - {group_id}")

            posts = get_posts(group=group_id, **self._default_config)
            for post in posts:
                logger.info(f"Found post id - {post['post_id']}")

                yield post

                total_posts_counter += 1
                if total_posts_counter >= total_posts_limit:
                    logger.info(
                        "Total posts limit reached. Stop returning more posts..."
                    )
                    return

                posts_per_group_counter += 1
                if posts_per_group_counter >= posts_per_group_limit:
                    logger.info(
                        "Total posts per group limit reached. Moving to next group id..."
                    )
                    continue

            sleep_duration = random.randint(1, 5)
            logger.info(
                f"Sleeping for {sleep_duration} seconds so the bot won't be detected"
            )
            await asyncio.sleep(sleep_duration)
