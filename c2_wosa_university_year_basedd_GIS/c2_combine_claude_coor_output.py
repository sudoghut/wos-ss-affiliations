import pandas as pd
import os
import re

input_dir = os.path.join(os.getcwd(), "claude_coordinates_output")
output_header = ["university_name", "x_coor", "y_coor"]
output_file_name = os.path.join(os.getcwd(), "c2_wosa_university_year_basedd_GIS", "claude_coordinates_output.csv")

# read the text contents from the input_dir
text_list = []
for filename in os.listdir(input_dir):
    file_path = os.path.join(input_dir, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                rows = file.readlines()
                for row in rows:
                    row = row.strip()
                    if row == "": continue
                    if ("university_name" not in row) and \
                       (":-" not in row) and \
                       ("- | -" not in row) and \
                       ("-|-" not in row):
                        row = re.sub("\t", "|", row)
                        row = re.sub(r"\|[\s]*\|", "|", row)
                        row = re.sub(r"^\|", "", row)
                        row = re.sub(r"\|$", "", row)
                        # using | to split row into list
                        row_list = row.split("|")
                        row_list = [row.strip() for row in row_list]
                        text_list.append(row_list)
                        if len(row_list)>3:
                            print(row_list)
                            raise

    except Exception as e:
        print("Failed to read file {}.".format(file_path))
        raise e

print(text_list[:10])
output_df = pd.DataFrame(text_list, columns=output_header)
output_df.to_csv(output_file_name, index=False)

print("Done!")