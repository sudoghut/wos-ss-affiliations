import pandas as pd
import os
import re

def clean_data(input_text):
    text = re.sub(r'\n\\t', '\t', input_text)
    return text

input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",'claude_output')
# get file names from input directory
file_names = os.listdir(input_dir)
# file_names = file_names[:5]
skip_list = ["In", "JSPS Core-"]
error_list = []

output_list = []
for file_name in file_names:
    with open(os.path.join(input_dir,file_name), 'r') as f:
        # read the files as text files
        text = f.read()
        text = clean_data(text)
        # split the text into lines
        lines = text.split('\n')
        # get the line with the data
        for line in lines:
            if "funder" in line or "Funders" in line: continue
            if line == "": continue
            line = re.sub(r'\s{2,}', '\t', line)
            row = line.split('\t')
            if row[-1] == "": row = row[:-1]
            if len(row) > 2:
                print(row)
                error_list.append(row)
            if len(row) > 1:
                output_list.append(row)
            else:
                new_row = row[0].split('\\t')
                if len(new_row) > 1:
                    output_list.append(new_row)
                else:
                    if new_row[0] not in skip_list:
                        print(new_row)
                        error_list.append(new_row)

# write the error list to a file
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "error_list.txt"), 'w') as f:
    for item in error_list:
        f.write("%s\n" % item[0])

# save the output as a csv file
output_df = pd.DataFrame(output_list)
output_df.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.csv"), index=False, header=False, sep='\t')





    