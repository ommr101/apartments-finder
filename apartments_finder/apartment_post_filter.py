import dataclasses
from datetime import datetime, timedelta
from typing import List

from config import config

from apartments_finder.apartment_post_enricher import ApartmentPost
from apartments_finder.logger import logger


@dataclasses.dataclass
class ApartmentFilter:
    min_rooms: float
    max_rooms: float
    min_rent: int
    max_rent: int

    def __str__(self):
        return (
            f"{self.min_rooms=}, {self.max_rooms=}, {self.min_rent=}, {self.max_rent=}"
        )


class ApartmentPostFilter:
    async def is_match(self, apartment_post: ApartmentPost, apartment_filters: List[ApartmentFilter]):
        for apartment_filter in apartment_filters:
            if (
                    apartment_filter.min_rooms <= apartment_post.rooms <= apartment_filter.max_rooms and
                    apartment_filter.min_rent <= apartment_post.rent <= apartment_filter.max_rent
            ):
                return True

        return False

    async def should_ignore_post(self, apartment_post: ApartmentPost):
        if not apartment_post.post_original_text:
            logger.info("No text was found in post")
            return True

        text_length = len(apartment_post.post_original_text)
        if text_length > config.MAX_TEXT_LEN:
            logger.info(f"Text length in post is {text_length} and is too long")
            return True

        now = datetime.now()
        time_diff = now - apartment_post.post_date
        if time_diff >= timedelta(hours=config.MAX_HOURS_DIFFERENCE):
            logger.info(f"The post is from {apartment_post.post_date} and is too old")
            return True

        return False
