from typing import List, Dict
from src.interfaces.output_strategy import OutputStrategy


class ConsoleStrategy(OutputStrategy):

    def output(self, data: List[Dict[str, str]]) -> None:
        print("-" * 110)
        print(
            f"{'Готель':<25} | {'Мережа':<18} | "
            f"{'Місто':<15} | {'Рейтинг':<8} | {'Ціна ($/ніч)':<12} | {'Статус':<12}"
        )
        print("-" * 110)

        for row in data:
            hotel_name = row.get("hotel_name", "N/A")
            chain = row.get("hotel_chain", "N/A")
            city = row.get("city", "N/A")
            rating = row.get("rating", "N/A")
            price = row.get("price_per_night_usd", "N/A")
            status = row.get("availability_status", "N/A")

            print(
                f"{hotel_name:<25} | {chain:<18} | "
                f"{city:<15} | {rating:<8} | {price:<12} | {status:<12}"
            )

        print("-" * 110)
        print(f"[ConsoleStrategy] Виведено {len(data)} записів")
