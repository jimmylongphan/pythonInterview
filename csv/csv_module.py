import csv

def load_csv_file(filename) -> list:
    data = []
    try:
        with open(filename, 'r') as file:
            headers = file.readline().strip().split(",")
            data.append(headers)

            for line in file:
                line = line.strip()
                if not line:
                    continue
                row = line.split(",")
                data.append(row)

    except Exception as e:
        print(e)

    return data

def load_csv_module(filename) -> list:
    data = []

    try:
        with open(filename, "r") as file:
            reader = csv.reader(file)
            headers = next(reader, None)
            if headers:
                data.append(headers)

            for row in reader:
                if not row:
                    continue
                data.append(row)

    except Exception as e:
        print(e)

    return data


data1 = load_csv_file("supplements.csv")
print(f"data using file reader")
for d in data1:
    print(d)


data2 = load_csv_module("supplements.csv")
print(f"data using csv reader")
for d in data2:
    print(d)
