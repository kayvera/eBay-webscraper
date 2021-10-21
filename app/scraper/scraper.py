import requests
import json
from bs4 import BeautifulSoup


class Scraper:
    def display_menu():
        print("Choose category to scrape: ")
        print("1. iPhone")
        print("2. Samsung")
        print("3. Google")
        print("4. LG")

    def get_category_choice():
        choice = int(input("Enter choice: "))
        try:
            category_url = CATEGORIES[choice]
        except KeyError:
            print("Wrong Choice Entered.")
            exit(1)
        return category_url

    def extract_source(url):
        source = requests.get(url).text
        return source

    def scrape_category(category_url):
        try:
            soup = BeautifulSoup(
                Scraper.extract_source(BASE_URL + category_url), "lxml"
            )
        except ConnectionError:
            print("Couldn't connect to ebay.com! Please try again.")
            exit(1)
        return soup

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

        print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    BASE_URL = "https://www.ebay.com/b/"

    CATEGORIES = {
        1: "Apple-Cell-Phones-Smartphones/9355/bn_319682?LH_Auction=1&rt=nc",
        2: "Samsung-Cell-Phones-and-Smartphones/9355/bn_352130?LH_Auction=1&rt=nc",
        3: "Google-Cell-Phones-Smartphones/9355/bn_3904160",
        4: "LG-Cell-Phones-and-Smartphones/9355/bn_353985",
    }
    Scraper.display_menu()
    category_url = Scraper.get_category_choice()
    soup = Scraper.scrape_category(category_url)
    Scraper.extract_product_info(soup)
