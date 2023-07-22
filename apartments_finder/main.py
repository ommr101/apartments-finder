import asyncio

import telegram

from apartments_finder.apartment_post_enricher import (ApartmentPostEnricher)
from apartments_finder.apartment_post_filter import (ApartmentPostFilterer)
from apartments_finder.apartments_scraper import FacebookGroupsScraper, ApartmentsScraper
from apartments_finder.config import config
from apartments_finder.exceptions import EnrichApartmentPostError
from apartments_finder.logger import logger

bot = telegram.Bot(config.TELEGRAM_BOT_API_KEY)
apartment_scraper: ApartmentsScraper = FacebookGroupsScraper(
    config.FACEBOOK_USERNAME,
    config.FACEBOOK_PASSWORD,
    config.FACEBOOK_GROUPS,
    config.POSTS_PER_GROUP_LIMIT,
    config.TOTAL_POSTS_LIMIT
)
apartment_post_parser = ApartmentPostEnricher()

apartment_post_filterer = ApartmentPostFilterer()


async def main():
    enriched_posts = 0

    try:
        apartment_posts_iter = apartment_scraper.get_apartments()

        async for apartment_post in apartment_posts_iter:
            if enriched_posts >= config.MAX_POSTS_TO_ENRICH_IN_RUN:
                logger.info("Enriched posts limit had been exceeded. Stopping run...")
                break

            if await apartment_post_filterer.should_ignore_post(apartment_post, config.POST_FILTERS):
                logger.info("Post should be ignored. Skipping it...")
                continue

            try:
                apartment_post = await apartment_post_parser.enrich(apartment_post)
                enriched_posts += 1

                logger.info("Successfully enriched this apartment with more data")
            except EnrichApartmentPostError:
                logger.info("Could not enrich data from post. Skipping post...")
                continue

            if not await apartment_post_filterer.is_match(apartment_post, config.APARTMENT_FILTERS):
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

    if config.TELEGRAM_BOT_APARTMENTS_LOGS_GROUP_CHAT_ID:
        with open("../app.log", 'rb') as f:
            await bot.send_document(
                chat_id=config.TELEGRAM_BOT_APARTMENTS_LOGS_GROUP_CHAT_ID,
                document=f
            )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
