import csv
from io import StringIO

file1 = "file1.csv"
file2 = "file2.csv"

# Simulate the CSV files as string variables (example data)
# Mocked CSV data for data1
file1_data = """
id,col1,col2
1,10,15
2,20,25
3,30,35
"""

# Mocked CSV data for data2
file2_data = """
id,col1,col2
1,5,10
2,10,5
3,15,10
"""

# Convert the string data to file-like objects using StringIO
file1 = StringIO(file1_data)
file2 = StringIO(file2_data)

primary_key = "id"

def read_csv_data(csv_filename: str, primary_key: str) -> dict:
    data = {}

    try :
        with open(csv_filename, mode='r') as file:
            reader = csv.DictReader(file)
            for r in reader:
                key_value = r[primary_key]
                data[key_value] = r
    except Exception as e:
        print(f"Error: {e}")

    return data

def read_csv_data_from_string(csv_data: str, primary_key: str) -> dict:
    data = {}
    try:
        # Using StringIO to simulate a file from a string
        file = StringIO(csv_data.strip())
        reader = csv.DictReader(file)  # DictReader expects a file-like object

        # Debugging: print header to check if CSV is read correctly
        print(f"Headers: {reader.fieldnames}")

        for row in reader:
            data[row[primary_key]] = row
    except Exception as e:
        print(f"Error reading the CSV data: {e}")
    return data

def merge_csv_data(data1: dict, data2: dict, primary_key: str) -> list:
    merged_data = []

    # iterate through the dicts
    for k, row1 in data1.items():
        # only use common keys
        if k in data2:
            row2 = data2[k]
            new_row = {
                primary_key: k,
            }

            row_sum = 0
            for column in row1:
                # add all colummns that is not the primary key
                # and is in both rows
                if column != primary_key and column in row2:
                    row_sum += float(row1[column]) + float(row2[column])

            new_row["computed_value"] = row_sum
            new_row["data1"] = row1
            new_row["data2"] = row2
            merged_data.append(new_row)

    return merged_data

def sort_data_by_computed_value(merged_data: list) -> list:
    return sorted(merged_data, key = lambda x: x["computed_value"], reverse=True)

# Function to print the sorted results
def print_sorted_data(sorted_data: list):
    print(f"id,computed_value,data1,data2")
    for row in sorted_data:
        print(f"{row['id']},{row['computed_value']},{row['data1']},{row['data2']}")


# Read data from the CSV files
# data1 = read_csv_data(file1, "id")
# data2 = read_csv_data(file2, "id")

execute = True
read = True

def main():
    if execute:
        # Read data from the mocked CSV content
        data1 = read_csv_data_from_string(file1_data, "id")
        data2 = read_csv_data_from_string(file2_data, "id")

        # Merge data from both CSVs
        merged_data = merge_csv_data(data1, data2, "id")

        # Sort merged data by computed value
        sorted_data = sort_data_by_computed_value(merged_data)

        # Print the sorted data
        print_sorted_data(sorted_data)

if __name__ == "__main__":
    main()
