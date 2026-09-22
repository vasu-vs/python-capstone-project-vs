import requests
import pandas as pd
import matplotlib.pyplot as plt


API_URL = "http://127.0.0.1:8000/books"


def fetch_books():

    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()

    return response.json()


def main():

    # Fetch API data
    books = fetch_books()

    # Create DataFrame
    df = pd.DataFrame(books)

    print("\nBOOK DATA")
    print("=" * 82)
    print(df.to_string(index=False))

    # Export CSV
    df.to_csv(
        "exported_books.csv",
        index=False
    )

    print("\nData exported to exported_books.csv")

    # Scatter plot
    plt.scatter(
        df["price"],
        df["rating"]
    )

    plt.title("Book Price vs Rating")

    plt.xlabel("Price (£)")
    plt.ylabel("Rating")

    plt.yticks([1, 2, 3, 4, 5])

    plt.grid(True)

    plt.tight_layout()

    plt.savefig("price_vs_rating.png")

    print("Chart saved as price_vs_rating.png")

    plt.show()


if __name__ == "__main__":
    main()

