import pandas as pd

dataframe = pd.read_csv("inventory-depth-dataset.csv")

print(dataframe)

for row in dataframe:
    print(row)

print(dataframe.size)
print(dataframe.shape)

rows, cols = dataframe.shape
for r in range(dataframe.shape[0]):
    print(dataframe.iloc[r,:])
    print("====")