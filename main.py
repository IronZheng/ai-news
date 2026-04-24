from __future__ import annotations

import argparse

import uvicorn

from financial_news_engine.main import NewsPipeline
from financial_news_engine.scheduler.runner import start_scheduler


def run_pipeline() -> None:
    NewsPipeline().run()


def run_api() -> None:
    uvicorn.run("financial_news_engine.api.server:app", host="0.0.0.0", port=8000, reload=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Financial News Intelligence System")
    parser.add_argument("mode", choices=["pipeline", "api", "scheduler"], help="Execution mode")
    args = parser.parse_args()

    if args.mode == "pipeline":
        run_pipeline()
    elif args.mode == "api":
        run_api()
    else:
        start_scheduler()


if __name__ == "__main__":
    main()
