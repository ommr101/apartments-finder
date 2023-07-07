import dataclasses
from typing import List

from apartment_post_parser import ApartmentPost


@dataclasses.dataclass
class ApartmentFilter:
    min_rooms: float
    max_rooms: float
    min_rent: int
    max_rent: int

    def __str__(self):
        return f'{self.min_rooms=}, {self.max_rooms=}, {self.min_rent=}, {self.max_rent=}'


class ApartmentPostFilter:
    def __init__(self, apartment_filters: List[ApartmentFilter]):
        self._apartment_filters = apartment_filters

    async def is_match(self, apartment_post: ApartmentPost):
        for apartment_filter in self._apartment_filters:
            if apartment_filter.min_rooms <= apartment_post.rooms <= apartment_filter.max_rooms and \
               apartment_filter.min_rent <= apartment_post.rent <= apartment_filter.max_rent:
                return True

        return False
