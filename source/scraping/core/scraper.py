# source/scraping/core/scraper.py

from playwright.sync_api import sync_playwright
import pandas as pd
import random
from .config import BASE_URL
from .utils import extract_article_metadata


def scrape_top_articles(topic="all", trending_period="week", top_n=10):
    """
    Scrapes the most popular DEV.to articles based on a specified topic and trending period.

    Args:
        topic (str): the topic tag to filter DEV.to articles. Use "all" to scrape articles from all topics.
        trending_period (str): the time interval for which articles are trending.
            Accepted values are "year", "month", "week", or "day".
        top_n (int): the total number of top articles to scrape.

    Returns:
        pd.DataFrame: A DataFrame containing the scraped data with columns including:
                      title and URL.
    """
    # URL construction
    url = BASE_URL
    if topic != "all":
        url += f"/t/{topic}"
    if trending_period != "day":
        url += f"/top/{trending_period}"

    # Initialize variables
    metadata_list = []

    # Start scraping
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Default user-agent context for the main page
        main_context = browser.new_context()
        page = main_context.new_page()
        page.goto(url, timeout=10000)
        # Wait for dynamic content to load (until network is almost idle)
        page.wait_for_load_state("networkidle")
        print(f"Starting scraper to retrieve the top {top_n} DEV.to articles "
              f"for topic/tag '{topic}' and trending period '{trending_period}'")

        # Infinite scroll to load top_n articles
        articles = page.query_selector_all("article.crayons-story")
        scroll_attempts = 0
        max_scroll_attempts = 20
        while len(articles) < top_n and scroll_attempts < max_scroll_attempts:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            # Random wait time to mimic human behavior
            page.wait_for_timeout(random.randint(800, 1500))
            articles = page.query_selector_all("article.crayons-story")
            scroll_attempts += 1
            print(f"Found {len(articles)} articles after {scroll_attempts} scrolls")

        # Select top_n articles.
        top_articles = articles[:top_n]

        # Extract metadata from each article
        for i, article in enumerate(top_articles):
            try:
                metadata = extract_article_metadata(article)
                print(f"Scraped metadata of article {i + 1}: {metadata.get('title')}")
                metadata_list.append(metadata)
            except Exception as e:
                print(f"Error extracting metadata from an article: {e}")

        # Close main context
        main_context.close()

        browser.close()

    return pd.DataFrame(metadata_list)