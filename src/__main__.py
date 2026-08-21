"""Entry point for the Naukri Job Scraper actor."""

import asyncio
from .main import main

if __name__ == "__main__":
    asyncio.run(main())
