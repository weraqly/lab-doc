import csv
import os
import random

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "booking_hotels.csv")

HOTEL_CHAINS = [
    "Marriott International",
    "Hilton Hotels",
    "IHG Hotels",
    "Accor Group",
    "Hyatt Hotels",
    "Radisson Hotel Group",
    "Wyndham Hotels",
    "Best Western",
    "Four Seasons",
    "Kempinski Hotels",
]

HOTEL_PREFIXES = [
    "Grand", "Royal", "Palace", "City", "Park",
    "Harbour", "Central", "Riverside", "Mountain", "Sunset",
]

HOTEL_SUFFIXES = [
    "Resort & Spa", "Inn", "Suites", "Plaza", "Lodge",
    "Boutique Hotel", "Residence", "Tower", "Court", "House",
]

CITIES = [
    "Київ", "Львів", "Одеса", "Барселона", "Прага",
    "Рим", "Париж", "Лондон", "Відень", "Стамбул",
    "Варшава", "Будапешт", "Амстердам", "Берлін", "Лісабон",
]

ROOM_TYPES = ["Стандарт", "Напівлюкс", "Люкс", "Сімейний", "Економ"]

AVAILABILITY_STATUSES = ["Доступний", "Зайнятий", "Останній номер", "Очікування"]


def generate_records(count: int = 50) -> list:
    records = []

    for i in range(count):
        chain = random.choice(HOTEL_CHAINS)
        city = random.choice(CITIES)

        hotel_name = f"{random.choice(HOTEL_PREFIXES)} {random.choice(HOTEL_SUFFIXES)}"

        rating = round(random.uniform(5.0, 10.0), 1)

        room_type = random.choice(ROOM_TYPES)
        base_price = {
            "Економ": random.uniform(25, 60),
            "Стандарт": random.uniform(50, 120),
            "Напівлюкс": random.uniform(100, 250),
            "Сімейний": random.uniform(80, 200),
            "Люкс": random.uniform(200, 600),
        }[room_type]

        city_multiplier = {
            "Київ": 0.7, "Львів": 0.65, "Одеса": 0.75,
            "Барселона": 1.3, "Прага": 0.9, "Рим": 1.4,
            "Париж": 1.6, "Лондон": 1.8, "Відень": 1.2,
            "Стамбул": 0.8, "Варшава": 0.85, "Будапешт": 0.8,
            "Амстердам": 1.5, "Берлін": 1.1, "Лісабон": 1.0,
        }[city]

        price = round(base_price * city_multiplier, 2)

        reviews_count = random.randint(10, 5000)
        free_rooms = random.randint(0, 15)

        if free_rooms == 0:
            status = "Зайнятий"
        elif free_rooms <= 2:
            status = "Останній номер"
        else:
            status = random.choice(["Доступний", "Очікування"])

        record = {
            "hotel_id": f"BKG-{2000 + i}",
            "hotel_name": hotel_name,
            "hotel_chain": chain,
            "city": city,
            "rating": str(rating),
            "room_type": room_type,
            "price_per_night_usd": str(price),
            "free_rooms": str(free_rooms),
            "reviews_count": str(reviews_count),
            "availability_status": status,
            "has_free_cancellation": random.choice(["Так", "Ні"]),
        }
        records.append(record)

    return records


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    records = generate_records(50)

    fieldnames = [
        "hotel_id", "hotel_name", "hotel_chain",
        "city", "rating", "room_type",
        "price_per_night_usd", "free_rooms", "reviews_count",
        "availability_status", "has_free_cancellation",
    ]

    with open(OUTPUT_FILE, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Згенеровано {len(records)} записів у {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
