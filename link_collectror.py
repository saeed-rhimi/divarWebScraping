from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


class LinkCollector:
    def __init__(self, base_url="https://divar.ir/s/tehran/buy-residential", total_cycles=50, max_scroll_attempts=15):
        self.base_url = base_url
        self.total_cycles = total_cycles
        self.max_scroll_attempts = max_scroll_attempts
        self.collected_links = set()

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Firefox(options=options)

    def scrape(self, total_cycles=50, max_scroll_attempts=15):
        if total_cycles is not None:
            self.total_cycles = total_cycles

        if max_scroll_attempts is not None:
            self.max_scroll_attempts = max_scroll_attempts

        self.driver.get(self.base_url)
        time.sleep(3)

        for cycle in range(self.total_cycles):
            scroll_attempts = 0
            previous_count = len(self.collected_links)
            button_found = False

            while scroll_attempts < self.max_scroll_attempts:
                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(2)

                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                links = soup.find_all("a", href=True)
                new_links = {f"https://divar.ir{link['href']}" for link in links if "/v/" in link['href']}

                if new_links:
                    self.collected_links.update(new_links)

                if len(self.collected_links) == previous_count:
                    scroll_attempts += 1
                else:
                    previous_count = len(self.collected_links)
                    scroll_attempts = 0

                try:
                    more_button = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "post-list__load-more-btn-be092"))
                    )
                    more_button.click()
                    button_found = True
                    break
                except Exception:
                    pass

            if not button_found:
                break

        self.collected_links = list(set(self.collected_links))
        self.driver.quit()
        return self.collected_links