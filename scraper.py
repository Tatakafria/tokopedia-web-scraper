from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

query = input('Barang yang ingin dicari: ')
tokopedia_products = input('Input nama file output: ')

# Setup Chrome options
options = Options()  # Run in background
options.add_argument("--window-size=900,700")
options.add_argument("--disable-logging")

# Path to ChromeDriver
service = Service('chromedriver')  # Replace with full path if needed
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

data = []

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
i_container = soup.find_all("div", class_="gG1uA844gIiB2+C3QWiaKA==")


# Target search URL
def scrape_data(search_query):
    url = f"https://www.tokopedia.com/search?page=1&q={search_query}"
    driver.get(url)
    
    # Scroll to load more products
    for i in range(2):
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, 1000);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(1000, 2000);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(2000, 3000);")
        time.sleep(2)

    # Extract product data
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    product_container = soup.find_all("div", class_="css-5wh65g")

    for i in product_container:
        name = i.find("span", class_="+tnoqZhn89+NHUA43BpiJg==")
        penjual = i.find("span", class_="si3CNdiG8AR0EaXvf6bFbQ== gxi+fsEljOjqhjSKqjE+sw== flip")
        location = i.find("span", class_="gxi+fsEljOjqhjSKqjE+sw== flip")
        price = i.find("span", class_="hC1B8wTAoPszbEZj80w6Qw==")
        discounted_price = i.find("div", class_="urMOIDHH7I0Iy1Dv2oFaNw== HJhoi0tEIlowsgSNDNWVXg==")
        try:
            price.get_text(strip=True)
        except:
            price = i.find("div", class_="urMOIDHH7I0Iy1Dv2oFaNw==")
            discounted_price = None
        promo = i.find("span", class_="_7UCYdN8MrOTwg0MKcGu8zg==")
        terjual = i.find("span", class_="u6SfjDD2WiBlNW7zHmzRhQ==")
        rating = i.find("span", class_="_2NfJxPu4JC-55aCJ8bEsyw==")
        link = i.find("a", class_="Ui5-B4CDAk4Cv-cjLm4o0g== XeGJAOdlJaxl4+UD3zEJLg==").get("href")


        data.append({
            "name": name.get_text(strip=True) if name else None,
            "price" : price.get_text(strip=True) if price else None,
            "discounted_price": discounted_price.get_text(strip=True) if discounted_price else None,
            "promo": promo.get_text(strip=True) if promo else None,
            "penjual": penjual.get_text(strip=True) if penjual else None,
            "lokasi_penjual": location.get_text(strip=True) if location else None,
            "rating": rating.get_text(strip=True) if rating else None,
            "unit_terjual": terjual.get_text(strip=True) if terjual else None,
            "url" : link
        })

scrape_data(query)

# Save to CSV
df = pd.DataFrame(data)
print(df.info())
df.to_csv(f'{tokopedia_products}.csv', index=False)
print(f"Scraping complete. Data saved to {tokopedia_products}.csv")