from __future__ import annotations

import logging
from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler

from financial_news_engine.config import settings
from financial_news_engine.main import NewsPipeline

logger = logging.getLogger(__name__)


def start_scheduler() -> None:
    scheduler = BackgroundScheduler(timezone="UTC")
    pipeline = NewsPipeline()
    scheduler.add_job(pipeline.run, "interval", hours=settings.scheduler_hours, id="news_pipeline")
    scheduler.start()
    logger.info("Scheduler started: every %s hour(s)", settings.scheduler_hours)

    try:
        while True:
            sleep(60)
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown(wait=False)


if __name__ == "__main__":
    start_scheduler()
