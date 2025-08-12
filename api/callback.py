def source_func(page_num):
    """
    Simulates a data source function that returns data based on the page_num parameter.
    Returns None or empty list when no more data.
    """
    data_pages = {
        1: ["row1,data1,100", "row2,data2,200"],
        2: ["row3,data3,300", "row4,data4,400"],
        3: []  # no more data
    }
    return data_pages.get(page_num, [])


def process_data(source_func, callback):
    """
    Calls source_func with increasing page_num until no data is returned.
    Calls callback on each item in the returned data.
    """
    page = 1
    while True:
        data_chunk = source_func(page)
        if not data_chunk:
            break  # no more data

        for item in data_chunk:
            row = item.split(",")
            callback(row)

        page += 1


def print_row(row):
    print("Processed row:", row)


if __name__ == "__main__":
    process_data(source_func, print_row)
