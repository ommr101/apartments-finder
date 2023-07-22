from datetime import datetime, timedelta
from typing import List

from entities import ApartmentFilter, PostFilter, ApartmentPost
from apartments_finder.logger import logger


class ApartmentPostFilterer:
    async def is_match(self, apartment_post: ApartmentPost, apartment_filters: List[ApartmentFilter]):
        for apartment_filter in apartment_filters:
            if (
                    apartment_filter.min_rooms <= apartment_post.rooms <= apartment_filter.max_rooms and
                    apartment_filter.min_rent <= apartment_post.rent <= apartment_filter.max_rent
            ):
                return True

        return False

    async def should_ignore_post(self, apartment_post: ApartmentPost, post_filters: List[PostFilter]):
        for post_filter in post_filters:
            if not apartment_post.post_original_text:
                logger.info("No text was found in post")
                return True

            text_length = len(apartment_post.post_original_text)
            if text_length > post_filter.max_post_text_len:
                logger.info(f"Text length in post is {text_length} and is too long")
                return True

            now = datetime.now()
            time_diff = now - apartment_post.post_date
            if time_diff >= timedelta(minutes=post_filter.max_post_minutes_difference):
                logger.info(f"The post is from {apartment_post.post_date} and is too old")
                return True

            for w in post_filter.words_to_ignore_post_on:
                if w in apartment_post.post_original_text:
                    logger.info(f"Found the ignore post on word '{w}'")
                    return True

        return False
