import dataclasses
from datetime import datetime
from typing import List


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


@dataclasses.dataclass
class PostFilter:
    words_to_ignore_post_on: List[str]
    max_post_minutes_difference: int
    max_post_text_len: int

    def __str__(self):
        return (
            f"{self.words_to_ignore_post_on=}, {self.max_post_minutes_difference=}, {self.max_post_text_len=}"
        )


@dataclasses.dataclass
class ApartmentPost:
    post_original_text: str
    post_url: str
    post_date: datetime
    rooms: float = 0
    location: str = ''
    rent: int = 0

    async def to_telegram_msg(self):
        return f"""
Found the following apartment -

post_original_text
{self.post_original_text}

post_url
{self.post_url}

post_date
{self.post_date}

rooms
{self.rooms}

location
{self.location}

rent
{self.rent}
        """
