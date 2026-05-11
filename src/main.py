import os
import sys
import configparser

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.csv_reader import CsvReader
from src.data_processor import DataProcessor
from src.interfaces.output_strategy import OutputStrategy
from src.strategies.console_strategy import ConsoleStrategy
from src.strategies.kafka_strategy import KafkaStrategy
from src.strategies.redis_strategy import RedisStrategy


def create_strategy(config: configparser.ConfigParser) -> OutputStrategy:
    strategy_name = config.get("output", "strategy", fallback="console").lower()

    if strategy_name == "kafka":
        broker = config.get("kafka", "broker", fallback="localhost:9092")
        topic = config.get("kafka", "topic", fallback="booking-hotels")
        print(f"[Lab4] Використовується Kafka стратегія (broker={broker}, topic={topic})")
        return KafkaStrategy(broker=broker, topic=topic)

    elif strategy_name == "redis":
        host = config.get("redis", "host", fallback="localhost")
        port = config.getint("redis", "port", fallback=6379)
        print(f"[Lab4] Використовується Redis стратегія ({host}:{port})")
        return RedisStrategy(host=host, port=port)

    elif strategy_name == "console":
        print("[Lab4] Використовується Console стратегія")
        return ConsoleStrategy()

    else:
        print(f"[Lab4] Невідома стратегія '{strategy_name}', використовується Console")
        return ConsoleStrategy()


def main() -> None:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(project_root, "config.ini")

    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8")

    strategy = create_strategy(config)

    csv_path = os.path.join(project_root, "data", "booking_hotels.csv")

    try:
        print(f"[Lab4] Зчитування файлу: {csv_path}")
        reader = CsvReader()
        data = reader.read(csv_path)
        print(f"[Lab4] Завантажено {len(data)} записів")

        processor = DataProcessor(strategy)
        processor.process(data)

        print("[Lab4] Готово!")

    except FileNotFoundError:
        print(f"[Lab4] Помилка: файл '{csv_path}' не знайдено.")
        print("[Lab4] Спочатку запустіть: python scripts/generate_csv.py")
    except Exception as e:
        print(f"[Lab4] Помилка: {e}")


if __name__ == "__main__":
    main()
