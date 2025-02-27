
import re

# Pre-compile the regular expression pattern
pattern = re.compile(r"select\s+(\S+)\s+from\s+(\S+)\s+where\s+(.+)\s*.*", re.IGNORECASE)

LIBRARY = [
    {
        'title': 'foo',
        'author': 'bob',
        'year': 2020
    },
    {
        'title': 'bar',
        'author': 'alice',
        'year': 2012
    }
]

def execute(query: str) -> list[dict]:
    # Use the pre-compiled regex pattern to search for a match
    match = pattern.match(query.strip())
    
    if match:
        # Return the tuple of (field, database, clause)
        print(match.groups())
    pass

def main():
    query1 = "select title from library where year = 2012"
    execute(query1)

main()
