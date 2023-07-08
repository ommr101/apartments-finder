import dataclasses
from datetime import datetime, timedelta
from typing import Any, Dict, List

from apartments_finder.apartment_post_parser import ApartmentPost
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
    def __init__(self, apartment_filters: List[ApartmentFilter]):
        self._apartment_filters = apartment_filters

    async def is_match(self, apartment_post: ApartmentPost):
        for apartment_filter in self._apartment_filters:
            if (
                apartment_filter.min_rooms
                <= apartment_post.rooms
                <= apartment_filter.max_rooms
                and apartment_filter.min_rent
                <= apartment_post.rent
                <= apartment_filter.max_rent
            ):
                return True

        return False


class PostFilter:
    def __init__(self, max_text_len: int, max_hours_difference: int):
        self.max_text_len = max_text_len
        self.max_hours_difference = max_hours_difference

    async def should_ignore_post(self, post: Dict[str, Any]):
        if not post["original_text"]:
            logger.info("No text was found in post")
            return True

        text_length = len(post["original_text"])
        if text_length > self.max_text_len:
            logger.info(f"Text length in post is {text_length} and is too long")
            return True

        now = datetime.now()
        time_diff = now - post["time"]
        if time_diff <= timedelta(hours=self.max_hours_difference):
            logger.info(f"The post is from {post['time']} and is too old")
            return True

        return False

    def __str__(self):
        return f"{self.max_text_len=}, {self.max_hours_difference=}"
