import requests
from bs4 import BeautifulSoup

from database import BookDatabaseManager


URL = "https://books.toscrape.com/"


RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


def scrape_books():

    response = requests.get(URL, timeout=10)
    
    response.raise_for_status()
    response.encoding = "utf-8"


    soup = BeautifulSoup(response.text, "html.parser")

    book_elements = soup.select("article.product_pod")[:20]

    books = []

    for book in book_elements:

        # Title
        title = book.select_one("h3 a")["title"]

        # Price
        price_text = book.select_one(".price_color").get_text(strip=True)

        price = float(
            price_text.replace("£", "")
        )

        # Stock
        availability = book.select_one(
            ".availability"
        ).get_text(strip=True)

        in_stock = "In stock" in availability

        # Rating
        rating_element = book.select_one(".star-rating")

        rating_class = rating_element["class"]

        rating_word = rating_class[1]

        rating = RATING_MAP[rating_word]

        books.append({
            "title": title,
            "price": price,
            "in_stock": in_stock,
            "rating": rating
        })

    return books


if __name__ == "__main__":

    db = BookDatabaseManager()

    db.clear_books()

    books = scrape_books()

    for book in books:

        db.insert_book(
            book["title"],
            book["price"],
            book["in_stock"],
            book["rating"]
        )

    print(f"{len(books)} books inserted successfully.")