# backend/run_spider.py
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def run_spider():
    os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "scraper.settings")
    process = CrawlerProcess(get_project_settings())
    process.crawl("pnp")
    process.start()
