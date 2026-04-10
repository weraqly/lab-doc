from interfaces import IRepository


class ShopService:
  
    def __init__(self, repository: IRepository):
        self._repository = repository  # Впровадження залежності

    # ── Import ─────────────────────────────────────────────────────────────────
    def import_data_from_file(self, file_path: str) -> None:
        """
        1. Зчитує дані з CSV (рівень доступу до даних).
        2. Перетворює рядки на моделі (бізнес-логіка).
        3. Зберігає в базу (рівень доступу до даних).
        """
        raw_rows = self._repository.read_csv(file_path)
        total = len(raw_rows)
        print(f"[INFO] Зчитано рядків: {total}")

        for idx, row in enumerate(raw_rows, start=1):
            supplier_data = {
                'name': row['supplier_name'],
                'contact_email': row['supplier_email'],
                'phone': row['supplier_phone'],
                'country': row['supplier_country'],
            }
            product_data = {
                'name': row['product_name'],
                'category': row['product_category'],
                'price': row['price'],
                'stock_quantity': row['stock_quantity'],
            }
            self._repository.save_supplier_with_product(supplier_data, product_data)

            if idx % 100 == 0 or idx == total:
                print(f"[INFO] Збережено {idx}/{total} записів…")

        print("[INFO] Імпорт завершено успішно.")

    # ── Queries ────────────────────────────────────────────────────────────────
    def get_products(self):
        return self._repository.get_all_products()

    def get_suppliers(self):
        return self._repository.get_all_suppliers()

    def get_expensive_products(self, min_price: float):
        """Бізнес-правило: фільтрація дорогих товарів"""
        return [p for p in self._repository.get_all_products() if p.price >= min_price]
