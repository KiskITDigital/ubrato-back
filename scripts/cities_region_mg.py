import pandas as pd

# Load CSV data into a DataFrame
df = pd.read_csv("location-2023-11-20.csv")
filter: list[str] = []
for row in df.values:
    if len(filter) == 0:
        filter.append(row[4])
    if filter[len(filter)-1] != row[4]:
        filter.append(row[4])

print("INSERT INTO regions (name) VALUES")
for v in filter:
    print(f"( '{v}' ),")

print("INSERT INTO cities (name, region_id) VALUES")

for row in df.values:
    print(f"( '{row[1]}', {filter.index(row[4]) + 1} ),")
