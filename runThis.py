from link_collectror import LinkCollector
from scraper import DivarScraper
from data_cleaner import DataCleaner
import pandas as pd

link_collector = LinkCollector()
collected_links = link_collector.scrape(total_cycles=10, max_scroll_attempts=15)

scraper = DivarScraper(collected_links)
df = scraper.scrape()

cleaner = DataCleaner(df=df)
cleaned_df = cleaner.clean_data()

cleaned_df.to_csv('cleaned_data.csv', index=False, encoding='utf-8-sig')