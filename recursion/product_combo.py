


"""
Given a budget of $3200 dollars to buy Apple products, create an algorithm to print all possible combinations of products you can buy?
Given the below product categories, each combination should contain one product from each category.

NOTES:
  - Backtracking
  - recursive
  - 


dfs method(limit, current_balance, current_list, index_cat_1, index_cat_2, product_tuples_1, ...)


Have a list of tuples for each category

[(MacBook air, 1249), ...]

MacBooks:
MacBook Air - $1249
MacBook Pro 13 Inch - $1399
MacBookPro 15 Inch - $2299
MacPro - $5999

iPads:
ipad Pro - $1299
ipad Air - $729
iPad - $459

iPhones:
iPhone 14 Pro - $1299
iPhone 12 - $799
iPhone 14 - $699
iPhone 12 Pro Max - $1499

Apple Watch :
Apple Watch Nike - $499
Apple Watch Hermes - $1099
Apple Watch Series 6 - $499


AirPods:
AirPods Pro - $299
AirPods - $149
AirPods Max - $549
"""

macbooks = [("MacBook Air" , 1249), ("MacBook Pro 13 Inch", 1399), ("MacBookPro 15 Inch" , 2299), ("MacPro" , 5999)]   
ipads = [ ("ipad Pro" , 1299), ("ipad Air", 729), ("iPad", 459) ]
iphones = [ ("iPhone 14 Pro" , 1299), ("iPhone 12" , 799), ("iPhone 14" , 699), ("iPhone 12 Pro Max" , 1499) ]
apple_watch = [ ("Apple Watch Nike" ,499), ("Apple Watch Hermes" , 1099), ("Apple Watch Series 6" , 499)  ]
air_pods = [ ("AirPods Pro" , 299), ("AirPods" , 149), ("AirPods Max" , 549) ]

categories = [
    macbooks,
    ipads,
    iphones,
    apple_watch,
    air_pods
]

result = []

import copy

NUM_OF_CATEGORIES = len(categories)

def get_product_combinations(limit, categories):
    # initialize beginning state for backtracking
    backtrack(limit, 0, [], categories, 0)

def backtrack(limit, current_balance, current_list, categories, category_index):
    # valid combination
    # current_list is of size 5 and balance is less than limit

    if len(current_list) == NUM_OF_CATEGORIES and current_balance <= limit:
        # add this to the result
        # make a deepcopy
        list_copy = copy.deepcopy(current_list)
        result.append((list_copy, current_balance)) 

        return

    # check for invalid combinations 
    if len(current_list) > 5:
        return

    # check for invalid balance
    if current_balance > limit:
        return

    # iterate through remaining items
    for c_index in range(category_index, len(categories)):
        category_list = categories[c_index]

        for c_i_index in range(len(category_list)):
            # use the next category and next item 
            item_name, item_price = category_list[c_i_index]

            # update values 
            current_balance += item_price
            current_list.append(item_name)

            # recursive call
            backtrack(limit, current_balance, current_list, categories, c_index + 1)

            # undo selection
            current_balance -= item_price
            current_list.pop()
            
get_product_combinations(3200, categories)
for r in result:
    print(f"result {r}")
