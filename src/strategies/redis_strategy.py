from typing import List, Dict
from src.interfaces.output_strategy import OutputStrategy


class RedisStrategy(OutputStrategy):

    def __init__(self, host: str = "localhost", port: int = 6379):
        self._host = host
        self._port = port
        self._client = None

    def _ensure_connected(self) -> None:
        if self._client is None:
            import redis

            self._client = redis.Redis(
                host=self._host,
                port=self._port,
                decode_responses=True,
            )

    def output(self, data: List[Dict[str, str]]) -> None:
        try:
            self._ensure_connected()
            pipe = self._client.pipeline()

            for row in data:
                hotel_id = row.get("hotel_id", "unknown")
                city = row.get("city", "unknown")
                key = f"hotel:{hotel_id}:{city}"
                pipe.hset(key, mapping=row)

            pipe.execute()
            print(f"[RedisStrategy] Збережено {len(data)} записів у Redis")

        except Exception as e:
            print(f"[RedisStrategy] Помилка збереження: {e}")
        finally:
            if self._client is not None:
                self._client.close()
                self._client = None
