"""Decode a secret message stored in a published Google Doc.

https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub
https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub
"""

import sys
from io import StringIO

import pandas as pd
import requests


def decode_secret_message(url):
    """Download the coordinate table and print its hidden message."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    for table in pd.read_html(StringIO(response.text), header=0):
        columns = {
            str(column).lower().replace("-", "").replace(" ", ""): column
            for column in table.columns
        }
        if {"xcoordinate", "ycoordinate", "character"} <= columns.keys():
            break
    else:
        raise ValueError("No coordinate table was found in the Google Doc.")

    x_column = columns["xcoordinate"]
    y_column = columns["ycoordinate"]
    character_column = columns["character"]

    grid = {
        (int(row[x_column]), int(row[y_column])): str(row[character_column])
        for _, row in table.iterrows()
    }

    max_x = max(x for x, _ in grid)
    max_y = max(y for _, y in grid)

    for y in range(max_y, -1, -1):
        print("".join(grid.get((x, y), " ") for x in range(max_x + 1)))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python decode_secret_message.py <published-google-doc-url>"
        )
    decode_secret_message(sys.argv[1])
