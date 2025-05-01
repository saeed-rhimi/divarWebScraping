# divarWebScraping


# 🏠 Divar Real Estate Scraper

This project is a fully modular web scraping pipeline designed to extract and clean structured real estate listings from [divar.ir](https://divar.ir), a popular Persian classifieds platform.

---

## 📌 Purpose

- Automatically collect real estate listing links from Divar.
- Extract structured data from individual property pages (title, price, size, features, etc.).
- Clean, normalize, and convert Persian numeric/textual data into structured formats.
- Save the cleaned dataset in a UTF-8 encoded CSV, ready for data analysis or BI tools.

---

## 📂 Project Structure

```
├── runThis.py             # Entry point – orchestrates the full scraping and cleaning process
├── link_collectror.py     # Collects links to property listings via automated scrolling
├── scraper.py             # Scrapes detailed property data from each listing page
├── data_cleaner.py        # Cleans and normalizes the raw scraped data
└── cleaned_data.csv       # Final CSV output (generated after execution)
```

---

## ⚙️ Requirements

- Python 3.8+
- Firefox browser installed
- [Geckodriver](https://github.com/mozilla/geckodriver/releases) accessible via system PATH

Install Python dependencies:

```bash
pip install pandas numpy selenium beautifulsoup4 tqdm
```

---

## 🚀 How to Run

Ensure Firefox and geckodriver are properly set up. Then, simply run:

```bash
python runThis.py
```

The script will:
1. Collect listing links using `LinkCollector`
2. Scrape data from each property page using `DivarScraper`
3. Clean and format the data using `DataCleaner`
4. Save the result to `cleaned_data.csv` in `utf-8-sig` encoding (for full Persian compatibility in Excel)

---

## 🧠 Technical Highlights

- Headless Selenium automation using Firefox
- Robust parsing with BeautifulSoup
- Persian digit conversion handled via string mapping
- Dynamic modal interaction and popup parsing for additional features
- Duplicate listing prevention via saved `scraped_links.csv`

---

## 📈 Possible Improvements

- Support for multiple cities beyond Tehran
- Integration with SQLite/PostgreSQL for persistent storage
- Interactive dashboard using Streamlit or Dash
- Machine learning for property clustering or price estimation

---

## 🛑 Disclaimer

This project is created **purely for educational purposes** to demonstrate how web scraping works.  
**Any use of this tool beyond learning and research is solely the responsibility of the user.**
 
**The author assumes no responsibility for misuse or legal consequences arising from use of this tool.**
"""
