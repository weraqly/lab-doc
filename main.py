
from infrastructure import SqliteRepository
from business_logic import ShopService
from presentation import ConsolePresentationLayer


def main():
    repository = SqliteRepository(db_url="sqlite:///shop.db")

    service = ShopService(repository=repository)

    ui = ConsolePresentationLayer()

    import os
    if not os.path.exists("data.csv"):
        print("[INFO] data.csv не знайдено — генеруємо автоматично…")
        from generate_csv import generate_csv
        generate_csv("data.csv", rows=1050)

    service.import_data_from_file("data.csv")

    products = service.get_products()
    suppliers = service.get_suppliers()

    print("\n── Перші 10 продуктів ──")
    ui.display_products(products[:10])

    print("\n── Всі постачальники ──")
    ui.display_suppliers(suppliers)

    print("\n── Товари дорожче 3000 грн ──")
    expensive = service.get_expensive_products(min_price=3000.0)
    ui.display_products(expensive[:10])
    print(f"(показано 10 з {len(expensive)} дорогих товарів)")


if __name__ == "__main__":
    main()
