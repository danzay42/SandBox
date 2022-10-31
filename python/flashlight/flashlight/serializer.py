import json
from dataclasses import dataclass, astuple


@dataclass(order=True)
class Command:
    command: str
    metadata: str


def desirealize(s) -> tuple[str, str] | None:
    try:
        parsed_to_dict_data = json.loads(s)
        validated_data = Command(**parsed_to_dict_data)
        return astuple(validated_data)
    except (TypeError, json.JSONDecodeError):
        print("Desirealize Error")

