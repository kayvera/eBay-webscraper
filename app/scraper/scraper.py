import requests
import json
from bs4 import BeautifulSoup


class Scraper:
    def scrape_category():
        try:
            for url, filename in zip(CATEGORIES, JSON_FILES):
                soup = BeautifulSoup(requests.get(BASE_URL + url).text, "lxml")
                data = Scraper.extract_product_info(soup)
                with open("data/" + filename, "w+") as json_file:
                    json.dump(data, json_file, indent=2)
            print("Files created successfully!")

        except ConnectionError:
            print("Couldn't connect to ebay.com! Please try again.")
            exit(1)

    def extract_product_info(soup):
        title = soup.find_all("h3", class_="s-item__title")
        bid = soup.find_all("span", class_="s-item__price")
        link = soup.find_all("a", class_="s-item__link", href=True)
        bid_time = soup.find_all("span", class_="s-item__time-left")
        bid_count = soup.find_all("span", class_="s-item__bids s-item__bidCount")

        data = []

        for title, bid, link, bid_time, bid_count in zip(
            title, bid, link, bid_time, bid_count
        ):
            data.append(
                {
                    "Title": title.getText(),
                    "Bid": bid.getText(),
                    "Link": link["href"],
                    "Bid_Time": bid_time.getText(),
                    "Bid_Count": bid_count.getText(),
                }
            )
        return data


if __name__ == "__main__":
    BASE_URL = "https://www.ebay.com/b/"

    CATEGORIES = [
        "Apple-Cell-Phones-Smartphones/9355/bn_319682?LH_Auction=1&rt=nc",
        "Samsung-Cell-Phones-and-Smartphones/9355/bn_352130?LH_Auction=1&rt=nc",
        "Google-Cell-Phones-Smartphones/9355/bn_3904160?LH_Auction=1&rt=nc",
        "LG-Cell-Phones-and-Smartphones/9355/bn_353985?LH_Auction=1&rt=nc",
    ]

    JSON_FILES = ["apple.json", "samsung.json", "google.json", "lg.json"]

    Scraper.scrape_category()
