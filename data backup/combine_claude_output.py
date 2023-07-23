import os, re

input_folder = "claude_output"
output_file = "claude_output.csv"

black_list = ["Here", "name | country", "|:-", "-:"]

output_list = []

for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()
                lines = [line.strip() for line in lines]
                lines = list(filter(None, lines))
                for line in lines:
                    if not any(black_str in line for black_str in black_list):
                        line = re.sub(r' {2,}', '\t', line)
                        output_list.append(line)
    except Exception as e:
        print('Failed to read %s. Reason: %s' % (file_path, e))

print(output_list[:10])
print(len(output_list))

# # insert "|-|-|" to output_list as the second line
# output_list.insert(1, "|-|-|")

# write to output file
with open(output_file, 'w') as file:
    for line in output_list:
        file.write(line + "\n")

