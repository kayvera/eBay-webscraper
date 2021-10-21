import requests
import json
from bs4 import BeautifulSoup

def display_menu():
    print("Choose category to scrape: ")
    print("1. IPhone")
    print("2. TVs")
    print("3. MacBook")
    
def get_category_choice():
    choice = int(input("Enter choice: "))
    try:
        category_url = CATEGORIES[choice]
    except KeyError:
        print("Wrong Choice Entered.")
        exit(1)
    return category_url

def extract_source(url):
    source=requests.get(url).text
    return source
  
def scrape_category(category_url):
  try:
    soup = BeautifulSoup(extract_source(BASE_URL + category_url), 'lxml')
  except ConnectionError:
    print("Couldn't connect to grailed.com! Please try again.")
    exit(1)
  return soup

def extract_product_info(soup):
  title = soup.find_all('h3', class_='s-item__title')
  price = soup.find_all('span', class_='s-item__price')
  link = soup.find_all('a', class_='s-item__link', href=True)
  
  data = []
  
  for title, price, link in zip(title, price, link):
    data.append({
      'Title': title.getText(),
      'Price': price.getText(),
      'Link': link['href']
    })
    
  print(json.dumps(data, indent = 2, ensure_ascii = False))  
  
if __name__ == "__main__":
  BASE_URL = 'https://www.ebay.com/b/'
    
  CATEGORIES = {
    1: "Apple-Cell-Phones-Smartphones/9355/bn_319682",
    2: "TVs/11071/bn_738302",
    3: "Apple-Laptops/111422/bn_320025"
  }
  display_menu()
  category_url = get_category_choice()
  soup = scrape_category(category_url)
  extract_product_info(soup)