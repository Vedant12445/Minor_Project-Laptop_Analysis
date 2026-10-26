import requests
import time
import csv
from lxml import html

def get_brand(title):
    return title.split()[0] if title else "Unknown"

def get_text(element):
    return element.text_content().strip() if element is not None else ""

def get_items_xpath(category):
    if category == "laptop":
        return '//div[contains(@class,"tUxRFH")]'
    else:
        return '//div[contains(@class,"slAVV4")]'

def scrape_flipkart(category, num_pages):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    all_data = []

    for page in range(1, num_pages + 1):
        url = f"https://www.flipkart.com/search?q={category}&page={page}"
        r = requests.get(url, headers=headers)
        tree = html.fromstring(r.content)

        items_xpath = get_items_xpath(category)
        items = tree.xpath(items_xpath)

        for item in items:
            if category == "laptop":
                title_tag = item.xpath('.//div[contains(@class,"KzDlHZ")]')
            else:
                title_tag = item.xpath('.//a[contains(@class,"wjcEIp")]')

            title = get_text(title_tag[0]) if title_tag else "N/A"
            brand = get_brand(title)

            price_tag = item.xpath('.//div[contains(@class,"Nx9bqj")]')
            original_price_tag = item.xpath('.//div[contains(@class,"yRaY8j")]')
            discount_tag = item.xpath('.//div[contains(@class,"UkUFwK")]')
            rating_tag = item.xpath('.//div[contains(@class,"XQDdHH")]')

            price = get_text(price_tag[0]) if price_tag else ""
            original_price = get_text(original_price_tag[0]) if original_price_tag else ""
            discount = get_text(discount_tag[0]) if discount_tag else ""
            rating = get_text(rating_tag[0]) if rating_tag else ""

            all_data.append([brand, title, price, original_price, discount, rating, category])

        print(f"Scraped page {page} for category '{category}'")
        time.sleep(1.25)

    # Save to CSV
    csv_filename = f"{category}.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["brand", "title", "price", "original_price", "discount", "rating", "category"])
        writer.writerows(all_data)
    print(f"Saved data to {csv_filename}")

# Run scraper
scrape_flipkart("laptop", 15)
scrape_flipkart("mouse", 10)
scrape_flipkart("keyboard", 10)
