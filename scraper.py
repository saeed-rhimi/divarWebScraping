import os
import re
import time
import pandas as pd
from datetime import datetime
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class DivarScraper:
    def __init__(self, links, csv_path="scraped_links.csv", encoding="utf-8-sig"):
        self.links = links
        self.csv_path = csv_path
        self.encoding = encoding
        self.all_data = []
        self.scraped_links = self.load_scraped_links()
        self.driver = self.setup_driver()

    def load_scraped_links(self):
        if os.path.exists(self.csv_path):
            return set(pd.read_csv(self.csv_path, encoding=self.encoding)['links'].tolist())
        return set()

    def save_scraped_link(self, link):
        df = pd.DataFrame({"links": [link]})
        df.to_csv(self.csv_path, mode="a", encoding=self.encoding, index=False, header=not os.path.exists(self.csv_path))

    def setup_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        return webdriver.Firefox(options=options)

    def load_page(self, url, delay=3):
        self.driver.get(url)
        time.sleep(delay)
        return BeautifulSoup(self.driver.page_source, "html.parser")

    def extract_property_details(self, page_soup):
        ad_title = page_soup.find("h1", class_="kt-page-title__title kt-page-title__title--responsive-sized")
        ad_title_text = ad_title.get_text(strip=True) if ad_title else "Not found"

        info_row = page_soup.find("tr", class_="kt-group-row__data-row")
        if info_row:
            info_values = info_row.find_all("td",
                                            class_="kt-group-row-item kt-group-row-item__value kt-group-row-item--info-row")
            area_text, build_year_text, room_number_text = (
                info_values[i].get_text(strip=True) if i < len(info_values) else "Not found" for i in range(3))
        else:
            area_text, build_year_text, room_number_text = "Not found", "Not found", "Not found"

        return ad_title_text, area_text, build_year_text, room_number_text

    def extract_price_details(self, page_soup):
        price_tags = page_soup.find_all("p", class_="kt-unexpandable-row__value")
        if len(price_tags) >= 3:
            total_price_text, per_meter_price_text, floor_number_text = (price_tags[i].get_text(strip=True) for i in
                                                                         range(3))
        else:
            total_price_text, per_meter_price_text, floor_number_text = "Not found", "Not found", "Not found"
        return total_price_text, per_meter_price_text, floor_number_text

    def extract_description(self, page_soup):
        description_tag = page_soup.find("p", class_="kt-description-row__text kt-description-row__text--primary")
        return description_tag.get_text(strip=True) if description_tag else "Not found"

    def convert_persian_to_english(self, text):
        return text.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")) if isinstance(text, str) else text

    def extract_floor_info(self, floor_text):
        match = re.match(r"(\d+)\sاز\s(\d+)", self.convert_persian_to_english(floor_text))
        return match.groups() if match else ("Not Found", "Not Found")

    def click_button(self):
        try:
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "raw-button-cd669"))
            )
            self.driver.execute_script("arguments[0].click();", button)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "kt-modal"))
            )
            return True
        except Exception:
            return False

    def extract_popup_data(self):
        try:
            popup = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "kt-modal"))
            )
            rows = popup.find_elements(By.XPATH, ".//div[contains(@class, 'kt-unexpandable-row')]")

            characteristics_list = []
            for row in rows:
                try:
                    title = row.find_element(By.XPATH, ".//p[contains(@class, 'kt-base-row__title')]").text.strip()
                    value = row.find_element(By.XPATH,
                                             ".//p[contains(@class, 'kt-unexpandable-row__value')]").text.strip()
                    characteristics_list.append(f"{title}: {value}")
                except:
                    continue

            features_list = []
            features = popup.find_elements(By.XPATH, ".//div[contains(@class, 'kt-feature-row')]")
            for feature in features:
                try:
                    feature_name = feature.find_element(By.XPATH,
                                                        ".//p[contains(@class, 'kt-feature-row__title')]").text.strip()
                    features_list.append(feature_name)
                except:
                    continue

            characteristics = " | ".join(characteristics_list) if characteristics_list else "not found"
            features = " | ".join(features_list) if features_list else "not found"

            return characteristics, features
        except Exception:
            return "not found", "not found"

    def scrape(self):
        for listing_url in self.links:
            if listing_url in self.scraped_links:
                continue

            listing_soup = self.load_page(listing_url, delay=4)
            name, area, build_year, room_number = self.extract_property_details(listing_soup)
            total_price, per_meter_price, floor_text = self.extract_price_details(listing_soup)
            description = self.extract_description(listing_soup)
            floor_number, total_floors = self.extract_floor_info(floor_text)

            if self.click_button():
                time.sleep(3)
                characteristics, features = self.extract_popup_data()
            else:
                characteristics, features = "not found", "not found"

            data = {
                "Title": self.convert_persian_to_english(name),
                "Property Size": self.convert_persian_to_english(area),
                "Total Price": self.convert_persian_to_english(total_price),
                "Price per Meter": self.convert_persian_to_english(per_meter_price),
                "Room Count": self.convert_persian_to_english(room_number),
                "Build Year": self.convert_persian_to_english(build_year),
                "Floor Number": floor_number,
                "Total Floors": total_floors,
                "Characteristics": characteristics,
                "Features": features,
                "Description": self.convert_persian_to_english(description),
                "URL": listing_url,
                "Crawl Date": datetime.now().strftime("%Y-%m-%d")
            }
            self.all_data.append(data)
            self.save_scraped_link(listing_url)

        self.driver.quit()
        return pd.DataFrame(self.all_data)
