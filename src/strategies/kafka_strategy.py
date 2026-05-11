import json
from typing import List, Dict
from src.interfaces.output_strategy import OutputStrategy


class KafkaStrategy(OutputStrategy):

    BATCH_SIZE = 50

    def __init__(self, broker: str, topic: str = "booking-hotels"):
        self._broker = broker
        self._topic = topic
        self._producer = None

    def _ensure_connected(self) -> None:
        if self._producer is None:
            from kafka import KafkaProducer

            self._producer = KafkaProducer(
                bootstrap_servers=[self._broker],
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                retries=3,
            )

    def output(self, data: List[Dict[str, str]]) -> None:
        try:
            self._ensure_connected()
            sent = 0

            for i in range(0, len(data), self.BATCH_SIZE):
                batch = data[i : i + self.BATCH_SIZE]
                for row in batch:
                    self._producer.send(self._topic, value=row)
                    sent += 1
                self._producer.flush()

            print(
                f'[KafkaStrategy] Відправлено {sent} повідомлень '
                f'у топік "{self._topic}"'
            )
        except Exception as e:
            print(f"[KafkaStrategy] Помилка відправки: {e}")
        finally:
            if self._producer is not None:
                self._producer.close()
                self._producer = None
