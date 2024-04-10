import csv
from io import StringIO
from typing import Any, Dict, List


def flatten_json(json_obj, parent_key="", separator="/"):
    items = {}
    for key, value in json_obj.items():
        new_key = parent_key + separator + key if parent_key else key
        if isinstance(value, dict):
            items.update(flatten_json(value, new_key, separator))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                items[f"{new_key}/{i}"] = item
        else:
            items[new_key] = value
    return items


def convert_json_to_csv(json_data: List[Dict[str, Any]]) -> str:
    csv_content = StringIO()
    writer = csv.DictWriter(
        csv_content, fieldnames=flatten_json(json_data[0]).keys()
    )
    writer.writeheader()
    for data in json_data:
        flattened_data = flatten_json(data)
        writer.writerow(flattened_data)

    return csv_content.getvalue()
