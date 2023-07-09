import asyncio

import telegram

from apartments_finder.apartment_post_enricher import (ApartmentPost,
                                                       ApartmentPostEnricher)
from apartments_finder.apartment_post_filter import (ApartmentFilter,
                                                     ApartmentPostFilter)
from apartments_finder.config import config
from apartments_finder.exceptions import EnrichApartmentPostError
from apartments_finder.facebook_groups_scraper import FacebookGroupsScraper
from apartments_finder.logger import logger

bot = telegram.Bot(config.TELEGRAM_BOT_API_KEY)
facebook_groups_scraper = FacebookGroupsScraper(
    config.FACEBOOK_USERNAME, config.FACEBOOK_PASSWORD
)
apartment_post_parser = ApartmentPostEnricher()

apartment_filters = [
    ApartmentFilter(
        min_rooms=2,
        max_rooms=3,
        min_rent=4000,
        max_rent=5500
    )
]
apartment_post_filter = ApartmentPostFilter()


async def main():
    apartment_filters_formatted = "\n".join([str(a) for a in apartment_filters])
    facebook_groups_formatted = "\n ".join([str(f) for f in config.FACEBOOK_GROUPS])
    logger.info(
        "Starting run...\n\n"
        f"Configured apartment filters - \n"
        f" {apartment_filters_formatted}\n"
        f"Configured facebook groups - \n"
        f" {facebook_groups_formatted}\n"
        f"Configured post filters -\n "
        f" {config.MAX_TEXT_LEN=}\n"
        f" {config.MAX_HOURS_DIFFERENCE=}\n"
    )

    try:
        async for post in facebook_groups_scraper.get_posts(config.FACEBOOK_GROUPS):
            post_original_text = post["original_text"]
            post_url = post["post_url"]
            post_date = post["time"]

            apartment_post = ApartmentPost(
                post_original_text=post_original_text,
                post_url=post_url,
                post_date=post_date
            )

            if await apartment_post_filter.should_ignore_post(apartment_post):
                logger.info("Post should be ignored. Skipping it...")
                continue

            try:
                apartment_post = await apartment_post_parser.enrich(apartment_post)
            except EnrichApartmentPostError:
                logger.info("Could not enrich data from post. Skipping post...")
                continue

            logger.info("Successfully enriched this apartment with more data")

            if not await apartment_post_filter.is_match(apartment_post, apartment_filters):
                logger.info("Apartment post did not match any filter. Skipping it")
                continue

            logger.info("Successfully matched this apartment with one of the filters")

            apartment_post_text = await apartment_post.to_telegram_msg()
            await bot.send_message(
                text=apartment_post_text,
                chat_id=config.TELEGRAM_BOT_APARTMENTS_GROUP_CHAT_ID,
            )

            logger.info("Successfully sent this apartment to the telegram bot")

    except Exception:  # pylint: disable=W0718
        logger.exception("Unexpected error - stopping execution...")

    with open("../app.log", 'rb') as f:
        await bot.send_document(
            chat_id=config.TELEGRAM_BOT_APARTMENTS_LOGS_GROUP_CHAT_ID,
            document=f
        )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
