import requests
from bs4 import BeautifulSoup
import pandas as pd


def main():
    # Базова адреса сайту
    base_url = "https://books.toscrape.com/"

    # Список для збереження книг
    books = []

    print("Починаємо збір даних...")

    try:
        # Перебираємо всі 50 сторінок
        for page in range(1, 51):

            # Формуємо URL
            if page == 1:
                url = base_url
            else:
                url = f"https://books.toscrape.com/catalogue/page-{page}.html"

            print(f"Обробка сторінки {page}...")

            # Отримуємо HTML
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Аналізуємо HTML
            soup = BeautifulSoup(response.text, "html.parser")

            # Знаходимо всі книги
            for book in soup.select("article.product_pod"):

                title = book.h3.a["title"]
                price = book.select_one(".price_color").text

                books.append({
                    "Title": title,
                    "Price": price
                })

        # Створюємо таблицю
        df = pd.DataFrame(books)

        # Зберігаємо у CSV
        df.to_csv("output.csv", index=False, encoding="utf-8")

        print(f"\nГотово! Зібрано {len(books)} книг.")

    except requests.exceptions.RequestException as error:
        print("Помилка при підключенні до сайту.")
        print(error)

    except Exception as error:
        print("Сталася помилка.")
        print(error)


if __name__ == "__main__":
    main()