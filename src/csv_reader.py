import csv
from typing import List, Dict


class CsvReader:

    @staticmethod
    def read(filepath: str) -> List[Dict[str, str]]:
        records: List[Dict[str, str]] = []

        with open(filepath, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(dict(row))

        return records
