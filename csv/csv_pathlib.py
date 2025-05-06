import pathlib
import json
from dataclasses import dataclass, fields


@dataclass
class Supplement:
    brand: str = None
    supplement_type: str = None
    serving_size_oz: float = None
    weight_oz: int = None
    color: str = None
    flavor: str = None
    taste: str = None

    def __post_init__(self):
        for f in fields(self):
            value = getattr(self, f.name)
            # Strip strings
            # Optionally convert ints/floats if needed
            if f.type == int and isinstance(value, str):
                setattr(self, f.name, int(value.strip()))
            elif f.type == float and isinstance(value, str):
                setattr(self, f.name, float(value.strip()))
            else:
                setattr(self, f.name, value.strip())


def load_csv_all_data(filename) -> list:
    data = []
    try:
        lines = pathlib.Path(filename).read_text().splitlines()
        for row, line in enumerate(lines):
            if not line or row == 0:
                continue

            data.append(Supplement(*line.split(',')))

    except Exception as e:
        print(e)

    return data


data = load_csv_all_data("supplements.csv")
for d in data:
    print(json.dumps(d.__dict__, indent=4))
