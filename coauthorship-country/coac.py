import pandas as pd
import matplotlib.pyplot as plt
import textwrap

# Read id, university, country mapping table
univ_country_df = pd.read_csv('node-with-country.csv')
print(univ_country_df.head())

# Name standardization dictionary
name_standardization_dict = {"USA": "United States"}

# Standardize univ_country_df['country'] in univ_country_df by name_standardization_dict
for i in range(len(univ_country_df)):
    country_name = univ_country_df['country'][i].strip()
    if country_name in name_standardization_dict:
        univ_country_df['country'][i] = name_standardization_dict[country_name]

univ_country_dict = dict(zip(univ_country_df['Label'], univ_country_df['country']))

# Read coauthorship data
# coauthorship_list = pd.read_csv('input-small.txt', delimiter="\t", header=None).values.tolist()
coauthorship_list = pd.read_csv('input.txt', delimiter="\t", header=None).values.tolist()
print(coauthorship_list[:5])

# Create country pairs
country_pairs = {}
for coauthorship_article in coauthorship_list:
    country_pairs_base_on_one_article = {}
    coauthorship_article_author_list = [i.strip() for i in coauthorship_article[0].split(';')]
    # Create country pairs by using coauthorship_article_author_list, also sort the country pairs
    for i in range(len(coauthorship_article_author_list)):
        for j in range(i + 1, len(coauthorship_article_author_list)):
            univ_a = coauthorship_article_author_list[i].strip().replace(',', '')
            univ_b = coauthorship_article_author_list[j].strip().replace(',', '')
            # Standardize university name in coauthorship_article_author_list
            if univ_a in name_standardization_dict:
                univ_a = name_standardization_dict[univ_a]
            if univ_b in name_standardization_dict:
                univ_b = name_standardization_dict[univ_b]
            if univ_a == "" or univ_b == "": continue
            if univ_a not in univ_country_dict:
                print(univ_a)
                continue
                # raise Exception('University not found in mapping table')
            if univ_b not in univ_country_dict:
                print(univ_b)
                continue
                # raise Exception('University not found in mapping table')
            country_pair = tuple(sorted([univ_country_dict[univ_a],
                                         univ_country_dict[univ_b]]))
            if country_pair not in country_pairs_base_on_one_article:
                country_pairs_base_on_one_article[country_pair] = 1
            # If we want to count by pairs, use the following code. If we want to count by articles, comment it.
            # else:
            #     country_pairs_base_on_one_article[country_pair] += 1
    # Merge country pairs from different articles
    for country_pair in country_pairs_base_on_one_article:
        if country_pair not in country_pairs:
            country_pairs[country_pair] = country_pairs_base_on_one_article[country_pair]
        else:
            country_pairs[country_pair] += country_pairs_base_on_one_article[country_pair]

# Sort country_pairs by value
country_pairs = {k: v for k, v in sorted(country_pairs.items(), key=lambda item: item[1], reverse=True)}
# Write country pairs to file
with open('coauthorship-country\coauthorship-country_output.txt', 'w') as f:
    f.write('Country pair,Count\n')
    for country_pair in country_pairs:
        f.write(country_pair[0] + '-' + country_pair[1] + ',' + str(country_pairs[country_pair]) + '\n')

print("Finished!")

# Visualize country_pairs by hirizontal bar chart
# Define function to wrap label
def wrap_label(label, width):
    return '\n'.join(textwrap.wrap(label, width))

# Get top n country pairs
n = 20
country_pairs_top_n = dict(list(country_pairs.items())[:n])
country_pairs_top_n = {k: v for k, v in sorted(country_pairs_top_n.items(), key=lambda item: item[1], reverse=True)}
print(country_pairs_top_n)

# Plot
plt.figure(figsize=(20, 10))
plt.barh(range(len(country_pairs_top_n)), list(country_pairs_top_n.values()), align='center')
plt.yticks(range(len(country_pairs_top_n)), [wrap_label(str(label), 20) for label in country_pairs_top_n.keys()])
plt.title('Top ' + str(n) + ' country pairs')
plt.xlabel('Count')
plt.ylabel('Country pair')
plt.gca().invert_yaxis()  # invert y axis to have max value at top
plt.show()