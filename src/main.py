"""Main actor logic for scraping Naukri.com job listings."""

import asyncio
from datetime import datetime, timezone
from typing import Any, Dict, List

from apify import Actor
from playwright.async_api import async_playwright

from .parser import parse_job_listing
from .utils import extract_json_data, build_search_url


async def main() -> None:
    """Main actor entry point."""
    async with Actor:
        # Get input configuration
        actor_input = await Actor.get_input() or {}
        
        # Extract input parameters with defaults
        search_query = actor_input.get("searchQuery", "")
        location = actor_input.get("location", "")
        experience = actor_input.get("experience", "")
        max_results = actor_input.get("maxResults", 100)
        proxy_config = actor_input.get("proxyConfiguration")
        
        Actor.log.info(f"Starting Naukri.com scraper with query: '{search_query}', location: '{location}'")
        
        # Build search URL
        search_url = build_search_url(search_query, location, experience)
        Actor.log.info(f"Search URL: {search_url}")
        
        # Launch browser with Playwright
        Actor.log.info("Launching Playwright browser...")
        
        async with async_playwright() as p:
            # Browser launch options
            launch_options = {
                "headless": True,
            }
            
            # Add proxy if configured
            if proxy_config and proxy_config.get('useApifyProxy'):
                Actor.log.info("Using Apify Proxy")
                # Apify Proxy URL format
                proxy_groups = proxy_config.get('apifyProxyGroups', [])
                proxy_country = proxy_config.get('apifyProxyCountry', 'IN')
                
                # Build Apify proxy URL
                from apify import ProxyConfiguration
                proxy_conf = ProxyConfiguration(
                    groups=proxy_groups if proxy_groups else None,
                    country_code=proxy_country
                )
                proxy_info = await proxy_conf.new_url()
                
                if proxy_info:
                    Actor.log.info(f"Proxy configured for country: {proxy_country}")
                    # Parse proxy URL
                    import re
                    match = re.match(r'http://([^:]+):([^@]+)@([^:]+):(\d+)', proxy_info)
                    if match:
                        username, password, server, port = match.groups()
                        launch_options["proxy"] = {
                            "server": f"http://{server}:{port}",
                            "username": username,
                            "password": password
                        }
            
            browser = await p.firefox.launch(**launch_options)
            page = await browser.new_page()
            
            try:
                # Navigate to search results
                Actor.log.info(f"Navigating to {search_url}")
                await page.goto(search_url, wait_until="domcontentloaded", timeout=60000)
                
                # Wait a bit for dynamic content
                await asyncio.sleep(3)
                
                # Get page content
                content = await page.content()
                
                # Try to extract JSON data first (check for __NEXT_DATA__ or API responses)
                json_data = extract_json_data(content)
                
                jobs = []
                
                if json_data:
                    Actor.log.info("Found structured JSON data, parsing...")
                    # Parse jobs from JSON (implementation in parser)
                    jobs = parse_job_listing(content, from_json=True, json_data=json_data)
                else:
                    Actor.log.info("No JSON data found, parsing HTML...")
                    # Parse jobs from HTML
                    jobs = parse_job_listing(content, from_json=False)
                
                Actor.log.info(f"Found {len(jobs)} job listings")
                
                # Limit results
                jobs = jobs[:max_results]
                
                # Add scraped timestamp
                scraped_at = datetime.now(timezone.utc).isoformat()
                for job in jobs:
                    job["scrapedAt"] = scraped_at
                
                # Push results to dataset
                if jobs:
                    await Actor.push_data(jobs)
                    Actor.log.info(f"Successfully scraped {len(jobs)} jobs")
                else:
                    Actor.log.warning("No jobs found")
                
            except Exception as e:
                Actor.log.error(f"Error during scraping: {e}")
                raise
            finally:
                await page.close()
                await browser.close()
        
        Actor.log.info("Actor finished successfully")
