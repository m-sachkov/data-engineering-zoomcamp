import sys
import pandas as pd

day = sys.argv[1]

df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
df.to_parquet(f"output_day_{day}.parquet")

print("day: ", day)