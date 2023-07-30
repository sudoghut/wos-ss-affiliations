import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import textwrap
import os

year_list = ["2018", "2019", "2020", "2021", "2022"]
year_dic = {}

# input_with_year = pd.read_csv(os.path.join('input-with-year-small.txt'), delimiter="\t", dtype=str).values.tolist()
input_with_year = pd.read_csv(os.path.join('input-with-year.txt'), delimiter="\t", dtype=str).dropna().values.tolist()
for article in input_with_year:
    year = article[1]
    if year not in year_dic:
        year_dic[year] = []
    year_dic[year].append(article[0])


univ_country_df = pd.read_csv(os.path.join('node-with-country.csv'))
print(univ_country_df.head())

name_standardization_dict = {"USA": "United States", "Hong Kong": "China", "Taiwan": "China"}

for i in range(len(univ_country_df)):
    country_name = univ_country_df['country'][i].strip()
    if country_name in name_standardization_dict:
        univ_country_df['country'][i] = name_standardization_dict[country_name]

univ_country_dict = dict(zip(univ_country_df['Label'], univ_country_df['country']))

def wrap_label(label, width):
    return '\n'.join(textwrap.wrap(label, width))

all_years_data = {}

for year, year_content in year_dic.items():
    country_pairs = {}
    for coauthorship_article in year_content:
        country_pairs_base_on_one_article = {}
        try:
            coauthorship_article_author_list = [i.strip() for i in coauthorship_article.split(';')]
        except:
            print(coauthorship_article)
            continue
        for i in range(len(coauthorship_article_author_list)):
            for j in range(i + 1, len(coauthorship_article_author_list)):
                univ_a = coauthorship_article_author_list[i].strip().replace(',', '')
                univ_b = coauthorship_article_author_list[j].strip().replace(',', '')
                if univ_a in name_standardization_dict:
                    univ_a = name_standardization_dict[univ_a]
                if univ_b in name_standardization_dict:
                    univ_b = name_standardization_dict[univ_b]
                if univ_a == "" or univ_b == "": continue
                if univ_a not in univ_country_dict:
                    print(univ_a)
                    continue
                if univ_b not in univ_country_dict:
                    print(univ_b)
                    continue
                country_pair = tuple(sorted([univ_country_dict[univ_a],
                                            univ_country_dict[univ_b]]))
                if 'China' not in country_pair: continue
                if country_pair not in country_pairs_base_on_one_article:
                    country_pairs_base_on_one_article[country_pair] = 1

        for country_pair in country_pairs_base_on_one_article:
            if country_pair not in country_pairs:
                country_pairs[country_pair] = country_pairs_base_on_one_article[country_pair]
            else:
                country_pairs[country_pair] += country_pairs_base_on_one_article[country_pair]

    country_pairs = {k: v for k, v in sorted(country_pairs.items(), key=lambda item: item[1], reverse=True)}
    
    n = 20
    country_pairs_top_n = dict(list(country_pairs.items())[:n])
    country_pairs_top_n = {k: v for k, v in sorted(country_pairs_top_n.items(), key=lambda item: item[1], reverse=True)}
    print('Top ' + str(n) + ' country pairs in ' + str(year) + ':')
    print(country_pairs_top_n)

    plt.figure(figsize=(20, 10), facecolor='white')
    plt.barh(range(len(country_pairs_top_n)), list(country_pairs_top_n.values()), align='center')
    plt.yticks(range(len(country_pairs_top_n)), [wrap_label(str(label), 20) for label in country_pairs_top_n.keys()])
    plt.title('Top ' + str(n) + ' country pairs' + ' in ' + str(year))
    plt.xlabel('Count')
    plt.ylabel('Country pair')
    plt.gca().invert_yaxis()  # invert y axis to have max value at top
    plt.savefig(os.path.join('b1_wosa_year_based','country_pairs_by_year', 'coauthorship-country_' + str(year) + '.png'), dpi=300)
    plt.close()
    
    for country_pair, count in country_pairs_top_n.items():
        if country_pair not in all_years_data:
            all_years_data[country_pair] = {year: count}
        else:
            all_years_data[country_pair][year] = count

plt.figure(figsize=(15, 10))

for country_pair, data in all_years_data.items():
    years = sorted(data.keys())
    counts = [data[year] for year in years]
    plt.plot(years, counts, marker='o', label='-'.join(country_pair))

plt.title('Country Pair Counts Over Years')
plt.xlabel('Year')
plt.ylabel('Number of Country Pairs')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(os.path.join('b1_wosa_year_based','country_pairs_by_year', 'coauthorship-country_all_years.png'), dpi=300)
plt.close()

# remove China-China from the plot
del all_years_data[('China', 'China')]
plt.figure(figsize=(15, 10))

for country_pair, data in all_years_data.items():
    years = sorted(data.keys())
    counts = [data[year] for year in years]
    plt.plot(years, counts, marker='o', label='-'.join(country_pair))
plt.title('Country Pair Counts Over Years - Without China-China')
plt.xlabel('Year')
plt.ylabel('Number of Country Pairs')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(os.path.join('b1_wosa_year_based','country_pairs_by_year', 'coauthorship-country_all_years_without_china.png'), dpi=300)
plt.close()

print('Finished')