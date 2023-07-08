import dataclasses
import json
from typing import Tuple

import openai
from facebook_scraper import Post

from apartments_finder.exceptions import ExtractDataFromPostError
from apartments_finder.logger import logger


@dataclasses.dataclass
class ApartmentPost:
    post_original_text: str
    post_url: str
    post_date: str
    rooms: float
    location: str
    rent: int

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


class ApartmentPostParser:
    functions = [
        {
            "name": "build_apartment_data",
            "description": "Returns the number of rooms, location and rent",
            "parameters": {
                "type": "object",
                "properties": {
                    "rooms": {
                        "type": "number",
                        "description": "The number of rooms, e.g. 3.5",
                    },
                    "location": {
                        "type": "string",
                        "description": "The location of the apartment, e.g. Tel Aviv, Hamashbir 4",
                    },
                    "rent": {
                        "type": "integer",
                        "description": "The rent of the apartment e.g. 6200",
                    },
                },
                "required": ["number_of_rooms", "rent"],
            },
        }
    ]

    async def parse(self, post: Post):
        post_original_text = post["original_text"]
        post_url = post["post_url"]
        post_date = str(post["time"])

        rooms, location, rent = await self._extract_data_from_post(post_original_text)

        apartment_post = ApartmentPost(
            post_original_text=post_original_text,
            post_url=post_url,
            post_date=post_date,
            rooms=rooms,
            location=location,
            rent=rent,
        )

        logger.info(
            f"Successfully extracted apartment post - \n"
            f"{apartment_post.post_original_text=}\n\n"
            f"{apartment_post.post_url=}\n\n"
            f"{apartment_post.post_date}\n\n"
            f"{apartment_post.rooms}\n\n"
            f"{apartment_post.location}\n\n"
            f"{apartment_post.rent}\n\n"
        )

        return apartment_post

    async def _extract_data_from_post(self, text) -> Tuple:
        messages = [
            {
                "role": "user",
                "content": f"Can you extract from the text the number of rooms, location and rent? \n {text}",
            }
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=self.functions,
            function_call={"name": "build_apartment_data"},
        )
        response_message = response["choices"][0]["message"]

        try:
            if not response_message.get("function_call"):
                raise KeyError("'function_call' key in openai response was not found")

            function_args = json.loads(response_message["function_call"]["arguments"])
            logger.info(f"Extracted the following data from the post - {function_args}")

            rooms = float(function_args.get("rooms") or 0)
            if not rooms:
                logger.warning(
                    "Could not extract number of rooms from the post, setting it to 0"
                )

            location = function_args.get("location") or "none"
            if not location:
                logger.info(
                    "Could not extract location from the post, setting it to none"
                )

            rent = int(function_args.get("rent") or 0)
            if not rent:
                logger.info("Could not extract rent from the post, setting it to 0")

            return rooms, location, rent
        except Exception:
            logger.exception(
                f"Openai response failed to parse correctly the following text - \n {text}"
            )
            raise ExtractDataFromPostError(
                f"Could not extract data from post text - \n {text}"
            )
