from typing import List

class Record:
    def __init__(self, timestamp: int, value: int, name: str):
        self.timestamp = timestamp
        self.value = value
        self.name = name

    def __repr__(self):
        return f"Record(t={self.timestamp}, v={self.value}, name='{self.name}')"

class TimeBin:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        self.records = []

    def add_record(self, record: Record):
        self.records.append(record)

    def finalize(self):
        self.records.sort(key=lambda r: r.name)

    def __repr__(self):
        return f"TimeBin(start={self.start}, end={self.end}, records={self.records})"
    

def build_time_histogram(records: List[Record], num_bins: int = 20) -> List[TimeBin]:
    # extract timestamps to determine bins
    timestamps = [r.timestamp for r in records]
    min_time = min(timestamps)
    max_time = max(timestamps)

    # edge case if all timestamps are the ssame
    # put them into the middle bin
    if min_time == max_time:
        bins = [TimeBin(min_time, max_time+1) for _ in range(num_bins)]
        mid = num_bins // 2
        for r in records:
            bins[mid].add_record(r)
        bins[mid].finalize()
        return bins

    # set the width of the bins
    # ensure we have at least 1
    bin_width = (max_time - min_time) // num_bins
    bin_width = max(bin_width, 1)

    # create the bins with the time ranges
    bins = []
    for i in range(num_bins):
        start_time = min_time + (i * bin_width)
        end_time = start_time + bin_width
        bins.append(TimeBin(start=start_time, end=end_time))

    # assign the records to the bins
    for r in records:
        # shift the timestamp to 0 and divide by bins
        index = (r.timestamp - min_time) // bin_width
        # ensure index can fit
        index = min(index, num_bins - 1)
        bins[index].add_record(r)

    # sort bins by the names
    for b in bins:
        b.finalize()

    return bins


if __name__ == "__main__":
    print("Inserting records into a histogram")

    records = [
        Record(100, 10, "c"),
        Record(150, 15, "a"),
        Record(200, 20, "b"),
        Record(400, 30, "d"),
        Record(180, 25, "z"),
        Record(120, 18, "m"),
    ]

    bins = build_time_histogram(records=records, num_bins=5)
    for i, b in enumerate(bins):
        print(f"Bin {i}: [{b.start}, {b.end}) → {b.records}")
