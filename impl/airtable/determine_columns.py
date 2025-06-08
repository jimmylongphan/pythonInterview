"""
return  ['text','checkbox','text','integer']

Assumptions
Only 4 columns

"""

data = [
    ["Name",                        "Approved by external auditor", "Status",     "Estimated hours"],
    ["Summer-inspired bites",       "",                             "checked",    ""               ],
    ["Poolside views",              "",                             "editing",    "5"              ],
    ["11 summer beach looks",       "",                             "editing",    ""               ],
    ["Mt. Kilimanjaro adventure",   "checked",                      "staging",    "4"              ],
  ]


def isCheckBox(values: set) -> bool:
    if len(values) > 2:
        return False
    
    # checkbox type
    if len(values) == 2:
        if "checked" in values and "" in values:
            return True

    # length is 1 so check for either
    return "checked" in values or "" in values

def isInteger(values: set) -> bool:
    for val in values:
        # can be empty 
        if val == "":
            continue

        if not val.isdigit():
            return False
        
    # all values are int
    return True

def getColumnType(values: set) -> type:
    if isCheckBox(values):
        return "checkbox"
    
    if isInteger(values):
        print(f"values are integer")
        return "integer"
    
    # default type
    return "text"

def examineColumn(column: int, data: list) -> type:
    values = set()

    # iterate through all rows and just get the values of the target column
    for row in data:
        val = row[column]
        values.add(val)

    column_type = getColumnType(values)
    return column_type

def getColumnTypes(data: list) -> list:
    # extract the column names
    column_names = data[0]

    num_columns = len(column_names)

    # process just the data
    data = data[1:]

    result = []
    for column in range(num_columns):
        column_type = examineColumn(column, data)
        result.append(column_type)

    return result

types = getColumnTypes(data)
print(f"types are {types}")
