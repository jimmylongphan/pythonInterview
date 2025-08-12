import requests

BASE_URL = "https://api.example.com"

def fetch_all_pages(endpoint_path, params):
    """
    Fetch all pages from a paginated API.
    Assumes the API JSON response includes:
      - 'data': list of records
      - 'page': current page number
      - 'total_pages': total number of pages
    """
    all_records = []
    current_page = params.get("page", 1)

    while True:
        params["page"] = current_page
        url = BASE_URL + endpoint_path  # endpoint_path must start with '/'

        try:
            resp = requests.get(url, params=params)
            if resp.status_code != 200:
                print(f"API request to {url} failed with status {resp.status_code}")
                break

            data = resp.json()
        except (requests.RequestException, ValueError) as e:
            print(f"Error fetching or parsing data from {url}: {e}")
            break

        records = data.get("data", [])
        all_records.extend(records)

        page = data.get("page", current_page)
        total_pages = data.get("total_pages", page)

        if page >= total_pages:
            break

        current_page += 1

    return all_records


def process_records(records):
    for record in records:
        if record.get("type") == "event":
            print(f"Processing event: {record}")


if __name__ == "__main__":
    user_events_endpoint = "/users/events"
    params = {"page": 1, "limit": 50}

    records = fetch_all_pages(user_events_endpoint, params)
    process_records(records)
