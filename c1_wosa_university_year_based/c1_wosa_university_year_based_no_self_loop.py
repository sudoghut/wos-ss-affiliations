import pandas as pd
import os
import textwrap
import matplotlib.pyplot as plt

seven_universities_name_list = ["Beihang University", "Beijing Institute of Technology", "Harbin Engineering University", "Northwestern Polytechnical University", "Nanjing University of Science & Technology", "Nanjing University of Aeronautics & Astronautics", "Harbin Institute of Technology"]
year_list = ["2018", "2019", "2020", "2021", "2022"]
input_with_year = pd.read_csv(os.path.join('input-with-year.txt'), delimiter="\t", dtype=str).dropna().values.tolist()
year_dic = {}
for article in input_with_year:
    year = article[1]
    if year not in year_dic:
        year_dic[year] = []
    year_dic[year].append(article[0])

for target_university in seven_universities_name_list:
    all_years_data = {}

    for year, year_content in year_dic.items():
        univ_pairs = {}
        for coauthorship_article in year_content:
            univ_pairs_base_on_one_article = {}
            try:
                coauthorship_article_author_list = [i.strip() for i in coauthorship_article.split(';')]
            except:
                print(coauthorship_article)
                continue
            for i in range(len(coauthorship_article_author_list)):
                for j in range(i + 1, len(coauthorship_article_author_list)):
                    univ_a = coauthorship_article_author_list[i].strip().replace(',', '')
                    univ_b = coauthorship_article_author_list[j].strip().replace(',', '')
                    univ_pair = tuple(sorted([univ_a,univ_b]))
                    if target_university not in univ_pair: continue
                    if univ_pair not in univ_pairs_base_on_one_article:
                        univ_pairs_base_on_one_article[univ_pair] = 1

            for univ_pair in univ_pairs_base_on_one_article:
                if univ_pair not in univ_pairs:
                    univ_pairs[univ_pair] = univ_pairs_base_on_one_article[univ_pair]
                else:
                    univ_pairs[univ_pair] += univ_pairs_base_on_one_article[univ_pair]

        univ_pairs = {k: v for k, v in sorted(univ_pairs.items(), key=lambda item: item[1], reverse=True)}
        n = 20
        univ_pairs_top_n = dict(list(univ_pairs.items())[:n])
        univ_pairs_top_n = {k: v for k, v in sorted(univ_pairs_top_n.items(), key=lambda item: item[1], reverse=True)}
        print('Top ' + str(n) +" "+ target_university + ' coauthorship pairs in ' + year + ':')
        print(univ_pairs_top_n)
        print('\n')
        for univ_pair, count in univ_pairs_top_n.items():
            if univ_pair not in all_years_data:
                all_years_data[univ_pair] = {year: count}
            else:
                all_years_data[univ_pair][year] = count
    # remove self loop
    del all_years_data[(target_university, target_university)]
    plt.figure(figsize=(15, 10))

    for univ_pair, data in all_years_data.items():
        years = sorted(data.keys())
        counts = [data[year] for year in years]
        plt.plot(years, counts, marker='o', label='-'.join(univ_pair))
    plt.title('Coauthorship Pairs of ' + target_university + ' with Other Universities')
    plt.xlabel('Year')
    plt.ylabel('Number of University Pairs')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join('c1_wosa_university_year_based','university_pairs_by_year', target_university + '_no_self_loop.png'), dpi=300)
    plt.close()

print('Finished!')