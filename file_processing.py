import pandas as pd
from main import file_2

data = pd.read_json('./'+file_2)

print(data.to_string())