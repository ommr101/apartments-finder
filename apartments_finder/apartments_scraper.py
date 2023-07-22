import asyncio
import random
from abc import ABC, abstractmethod
from typing import AsyncIterator

from entities import ApartmentPost
from facebook_scraper import get_posts
from apartments_finder.logger import logger


class ApartmentsScraper(ABC):
    @abstractmethod
    def get_apartments(self) -> AsyncIterator[ApartmentPost]:
        pass


class FacebookGroupsScraper(ApartmentsScraper):
    def __init__(self, username, password, group_ids, posts_per_group_limit, total_posts_limit):
        self._default_config = {
            "credentials": (username, password),
            "extra_info": False,
            "page_limit": 10,
            "options": {
                "comments": False,
                "reactors": False,
                "allow_extra_requests": False,
                "posts_per_page": 10
            }
        }

        self._group_ids = group_ids
        self._total_posts_limit = total_posts_limit
        self._posts_per_group_limit = posts_per_group_limit

    async def get_apartments(self) -> AsyncIterator[ApartmentPost]:
        total_posts_counter = 0
        get_posts_config = dict(self._default_config)

        for group_id in self._group_ids:
            posts_per_group_counter = 0
            logger.info(f"Getting posts from group id - {group_id}")

            posts = get_posts(group=group_id, **get_posts_config)
            for post in posts:
                logger.info(f"Found post id - {post['post_id']}")

                post_original_text = post["original_text"]
                post_url = post["post_url"]
                post_date = post["time"]

                apartment_post = ApartmentPost(
                    post_original_text=post_original_text,
                    post_url=post_url,
                    post_date=post_date
                )

                yield apartment_post

                total_posts_counter += 1
                if total_posts_counter >= self._total_posts_limit:
                    logger.info(
                        "Total posts limit reached. Stop returning more posts..."
                    )
                    return

                posts_per_group_counter += 1
                if posts_per_group_counter >= self._posts_per_group_limit:
                    logger.info(
                        "Total posts per group limit reached. Moving to next group id..."
                    )
                    break

            # Remove credentials from config in order to avoid re-authentication
            get_posts_config.pop('credentials', None)

            sleep_duration = random.randint(1, 5)
            logger.info(
                f"Sleeping for {sleep_duration} seconds so the bot won't be detected"
            )
            await asyncio.sleep(sleep_duration)
