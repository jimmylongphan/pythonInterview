"""
expected_depth_status
"""

"""
Inventory class 
  - initialization step 
    - load the csv file, create stock objects 
    - store in a map product id -> stock object
    - handle low stock threshold 
      - low stock threshold
        - user defined (pass in as a parameter)
        - system defined 
            - if not user defined 
            - total units shipped over past 30 days (CSV file), or 5 unitts
        - calculate low stock threshold and save into the stock object
  - handle Inventory status 
    - implement the logic defined in the file
    - print string for now 
  
Stock class 
  - product id 
  - unallocated_available_qty
  - in_stock_qty
  - total_shipped_past_30_days
  - user_threshold
  - stock threshold 

Error handling 
  - bad csv file 
  - ??

"""

import csv 

class Stock:
    def __init__(self, product_id, unallocated_available_qty, in_stock_qty, total_shipped_past_30_days):
        self.product_id = product_id
        self.unallocated_available_qty = unallocated_available_qty
        self.in_stock_qty = in_stock_qty
        self.total_shipped_past_30_days = total_shipped_past_30_days

    def set_threshold(self, threshold):
        self.threshold = threshold
    
    def __str__(self):
        return f"product_id: {self.product_id}, unallocated_available_qty: {self.unallocated_available_qty}, in_stock_qty: {self.in_stock_qty}, total_shipped_past_30_days: {self.total_shipped_past_30_days}"


class Inventory:
    MIN_SYSTEM_THRESHOLD = 5

    def __init__(self):
        self.stocks = {}

    def load_csv(self, csv_file):
        # reads the csv file 
        # creates a stock object for each row
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            # skip the first row
            next(reader)
            for row in reader:
                product_id = row[0]
                unallocated_available_qty = 0
                try:
                    unallocated_available_qty = int(row[1])
                except Exception as e:
                    print(e)

                in_stock_qty = row[2]
                total_shipped_past_30_days = row[3]
                stock = Stock(product_id, unallocated_available_qty, in_stock_qty, total_shipped_past_30_days)
                self.stocks[product_id] = stock

                # handle user defined threshold
                user_threshold = row[4]
                if user_threshold != "null":
                    stock.set_threshold(int(user_threshold))
                else:
                    # system defined threshold
                    if total_shipped_past_30_days == "null":
                        total_shipped_past_30_days = self.MIN_SYSTEM_THRESHOLD
                    else:
                        total_shipped_past_30_days = int(total_shipped_past_30_days)
    
                    stock.set_threshold(max(self.MIN_SYSTEM_THRESHOLD, total_shipped_past_30_days))


    def get_stock(self, product_id):
        return self.stocks[product_id]

    def get_status(self, stock):
        if stock.unallocated_available_qty > stock.threshold:
            return "Full Stock"
        elif stock.unallocated_available_qty == 0:
            return "Out of Stock"
        elif stock.unallocated_available_qty < 0:
            return "Oversold"
        elif stock.unallocated_available_qty <= stock.threshold:
            # this may also match Oversold so this is checked last
            return "Low Stock"
        
    def get_all_stock_status(self):
        # print out all of the inventory status categories of all stocks

        for id, stock in self.stocks.items():
            status = self.get_status(stock)
            print(f"stock id: {id}, status: {status}")

    def get_stock_status_csv(self):
        
        pass

def main():
    my_inventory = Inventory()
    my_inventory.load_csv("inventory-depth-dataset.csv")
    my_inventory.get_all_stock_status()

if __name__ == "__main__":
    main()
    print("done")
    