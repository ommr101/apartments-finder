import asyncio

import telegram

from apartments_finder.apartment_post_filter import (ApartmentFilter,
                                                     ApartmentPostFilter,
                                                     PostFilter)
from apartments_finder.apartment_post_parser import ApartmentPostParser
from apartments_finder.config import config
from apartments_finder.exceptions import ExtractDataFromPostError
from apartments_finder.facebook_groups_scraper import FacebookGroupsScraper
from apartments_finder.logger import logger

bot = telegram.Bot(config.TELEGRAM_BOT_API_KEY)
facebook_groups_scraper = FacebookGroupsScraper(
    config.FACEBOOK_USERNAME, config.FACEBOOK_PASSWORD
)
apartment_post_parser = ApartmentPostParser()

apartment_filters = [
    # ApartmentFilter(
    #     min_rooms=0,
    #     max_rooms=3,
    #     min_rent=4000,
    #     max_rent=5500
    # ),
    ApartmentFilter(min_rooms=0, max_rooms=5, min_rent=1000, max_rent=20000)
]
apartment_post_filter = ApartmentPostFilter(apartment_filters)

post_filter = PostFilter(config.MAX_TEXT_LEN, config.MAX_HOURS_DIFFERENCE)


async def main():
    apartment_filters_formatted = "\n".join([str(a) for a in apartment_filters])
    facebook_groups_formatted = "\n".join([str(f) for f in config.FACEBOOK_GROUPS])
    post_filters_formatted = str(post_filter)
    logger.info(
        "Starting run...\n"
        f"Configured apartment filters - \n {apartment_filters_formatted}\n"
        f"Configured facebook groups - \n {facebook_groups_formatted}\n"
        f"Configured post filters - \n {post_filters_formatted}\n"
    )

    try:
        async for post in facebook_groups_scraper.get_posts(config.FACEBOOK_GROUPS):
            if post_filter.should_ignore_post(post):
                logger.info("Post should be ignored. Skipping it...")
                continue

            try:
                apartment_post = await apartment_post_parser.parse(post)
            except ExtractDataFromPostError:
                logger.info("Could not extract data from post. Skipping post...")
                continue

            if not await apartment_post_filter.is_match(apartment_post):
                logger.info("Apartment post did not match any filter. Skipping it")
                continue

            apartment_post_text = await apartment_post.to_telegram_msg()
            await bot.send_message(
                text=apartment_post_text,
                chat_id=config.TELEGRAM_BOT_APARTMENTS_GROUP_CHAT_ID,
            )
    except Exception:  # pylint: disable=W0718
        logger.exception("Unexpected error - stopping execution...")

    with open("../app.log", "r", encoding="utf-8") as f:
        logs = "\n".join(f.readlines())
        await bot.send_message(
            text=logs, chat_id=config.TELEGRAM_BOT_APARTMENTS_LOGS_GROUP_CHAT_ID
        )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
