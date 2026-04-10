from interfaces import IPresentationLayer


class ConsolePresentationLayer(IPresentationLayer):
    

    def display_products(self, products) -> None:
        print(f"\n{'='*70}")
        print(f"{'ID':<5} {'Назва':<30} {'Категорія':<18} {'Ціна':>8} {'Кількість':>10}")
        print(f"{'-'*70}")
        for p in products:
            print(f"{p.id:<5} {p.name:<30} {p.category:<18} {p.price:>8.2f} {p.stock_quantity:>10}")
        print(f"{'='*70}\nВсього продуктів: {len(products)}\n")

    def display_suppliers(self, suppliers) -> None:
        print(f"\n{'='*70}")
        print(f"{'ID':<5} {'Назва':<25} {'Email':<28} {'Країна':<12}")
        print(f"{'-'*70}")
        for s in suppliers:
            print(f"{s.id:<5} {s.name:<25} {s.contact_email:<28} {s.country:<12}")
        print(f"{'='*70}\nВсього постачальників: {len(suppliers)}\n")
