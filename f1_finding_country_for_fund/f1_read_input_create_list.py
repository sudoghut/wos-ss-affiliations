import pandas as pd
import os
import json

input_path = os.path.join(os.path.dirname(__file__), 'input')
print(input_path)
json_dir = [f for f in os.listdir(input_path) if f.endswith('.txt')]
print(json_dir[:10])
combined_data = {}
#create an empty json list
for file in json_dir:
    with open(os.path.join(input_path, file), 'r') as f:
        data = json.load(f)
        combined_data = {**combined_data, **data}
combined_json = json.dumps(combined_data)
key_list = list(combined_data.keys())
print(len(combined_json))
print(len(key_list))
print(key_list[:10])

df = pd.DataFrame(key_list)
output_path = os.path.join(os.path.dirname(__file__), 'fund_list.csv')
df.to_csv(output_path, index=False, header=False)



