import pandas as pd

# Load CSV data into a DataFrame
df = pd.read_csv("location-2023-11-20.csv")
filter = {}
for row in df.values:
    filter[row[4]] = True

print("INSERT INTO regions (name) VALUES")
for v in filter.keys():
    print(f"( '{v}' ),")

print("INSERT INTO cities (name, region_id) VALUES")

for row in df.values:
    print(f"( '{row[1]}', {row[3]} ),")
