import json

def processStream(stream, callback):
    """
    Reads each chunk from the stream without buffering the entire stream.
    Filters for items where type == "event" and counts them.
    Calls callback(count) each time a new event is processed.
    """
    event_count = 0
    for chunk in stream:
        try:
            data = json.loads(chunk)
            if data.get("type") == "event":
                event_count += 1
                callback(event_count)
        except json.JSONDecodeError:
            print(f"Warning: malformed chunk skipped -> {chunk!r}")

# Example: simulated data stream (could be file, network, etc.)
def simulated_stream():
    chunks = [
        '{"type": "event", "id": 1}',
        '{"type": "log", "id": 2}',
        '{"type": "event", "id": 3}',
        '{"type": "event", "id": 4}',
        'INVALID_JSON',
        '{"type": "event", "id": 5}'
    ]
    for chunk in chunks:
        yield chunk  # simulate arriving one chunk at a time

# Example callback
def print_count(count):
    print(f"Events processed: {count}")

if __name__ == "__main__":
    processStream(simulated_stream(), print_count)
