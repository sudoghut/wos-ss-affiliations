import requests
import pandas as pd
import os
import time

# https://nominatim.openstreetmap.org/search?q=x&format=json

def geocode_address(address):
    url = "https://nominatim.openstreetmap.org/search?q=" + address + "&format=json"
    user_agent_info = "A Python script"
    headers = {'User-Agent': user_agent_info}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            return data[0]
        else:
            return None
    else:
        return None

input_excel = "node-with-country.xlsx"
input_df = pd.read_excel(input_excel, sheet_name="node-with-countries", dtype=str).fillna("")
label_list = input_df["Label"].tolist()
label_list = label_list[101:]

output_file_name = os.path.join(os.getcwd(), "c2_wosa_university_year_basedd_GIS", "osm_coordinates_output.csv")
output_header = ["university_name", "x_coor", "y_coor"]

with open(output_file_name, "w", encoding="utf-8") as file:
    file.write(",".join(output_header) + "\n")

output_list = []
counter = 0
for label in label_list:
    counter += 1
    address = label
    time.sleep(1)
    data = geocode_address(address)
    if data is None:
        address = " ".join(address.split(" ")[:-1])
        time.sleep(1)
        data = geocode_address(address)
    if data is not None:
        output_list.append([label, data["lat"], data["lon"]])
    else:
        output_list.append([label, "", ""])
    # save the output(add to the end of the file) once 100 records are processed
    if len(output_list) % 100 == 0:
        output_df = pd.DataFrame(output_list, columns=output_header)
        output_df.to_csv(output_file_name, mode='a', index=False, header=False)
        print("Saved {} records.".format(counter))
        time.sleep(1)
        output_list = []
if len(output_list) > 0:
    output_df = pd.DataFrame(output_list, columns=output_header)
    output_df.to_csv(output_file_name, mode='a', index=False)
    print("Saved {} records.".format(counter))

print("Done!")