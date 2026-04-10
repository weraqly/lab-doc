

import csv
import random
import sys

CATEGORIES = [
    "Електроніка", "Одяг", "Продукти харчування", "Побутова хімія",
    "Іграшки", "Спорт та відпочинок", "Книги", "Меблі", "Косметика", "Авто"
]

COUNTRIES = ["Україна", "Польща", "Німеччина", "Китай", "США", "Франція", "Туреччина"]

PRODUCT_TEMPLATES = [
    "Смартфон {}", "Ноутбук {}", "Футболка {}", "Джинси {}",
    "Кавоварка {}", "Навушники {}", "Книга «{}»", "Крісло {}",
    "Велосипед {}", "Помада {}", "Шампунь {}", "Чай {}",
    "Кросівки {}", "Планшет {}", "Монітор {}", "Клавіатура {}",
    "Мишка {}", "Рюкзак {}", "Куртка {}", "Холодильник {}",
]

SUPPLIER_NAMES = [
    "TechSupply UA", "EcoGoods Ltd", "GlobalMart", "ProTrade Co",
    "FastDelivery", "MegaStock", "AlphaWholesale", "BetaDistrib",
    "GammaTrade", "DeltaGoods", "EpsilonMarket", "ZetaSupply",
    "EtaCommerce", "ThetaLogistics", "IotaRetail", "KappaStore",
    "LambdaHub", "MuDistrib", "NuSupplies", "XiNetwork",
]


def generate_csv(filename: str = "data.csv", rows: int = 1050) -> None:
    if rows < 1000:
        print("[WARN] Мінімальна кількість рядків — 1000. Встановлено 1000.")
        rows = 1000

    num_suppliers = min(50, rows)
    suppliers = []
    for i in range(num_suppliers):
        name = SUPPLIER_NAMES[i % len(SUPPLIER_NAMES)] + (f" {i // len(SUPPLIER_NAMES) + 1}" if i >= len(SUPPLIER_NAMES) else "")
        suppliers.append({
            'name': name,
            'email': f"supplier{i}@trade.com",
            'phone': f"+380{random.randint(500000000, 999999999)}",
            'country': random.choice(COUNTRIES),
        })

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "product_name", "product_category", "price", "stock_quantity",
            "supplier_name", "supplier_email", "supplier_phone", "supplier_country"
        ])

        for i in range(rows):
            supplier = suppliers[i % num_suppliers]
            template = PRODUCT_TEMPLATES[i % len(PRODUCT_TEMPLATES)]
            writer.writerow([
                template.format(i + 1),
                random.choice(CATEGORIES),
                round(random.uniform(10.0, 5000.0), 2),
                random.randint(0, 1000),
                supplier['name'],
                supplier['email'],
                supplier['phone'],
                supplier['country'],
            ])

    print(f"[OK] Файл «{filename}» згенеровано: {rows} рядків даних.")


if __name__ == "__main__":
    _rows = int(sys.argv[1]) if len(sys.argv) > 1 else 1050
    _file = sys.argv[2] if len(sys.argv) > 2 else "data.csv"
    generate_csv(_file, _rows)
