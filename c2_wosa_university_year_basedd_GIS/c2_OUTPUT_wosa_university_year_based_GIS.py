import pandas as pd
import os
import folium
from markupsafe import escape
import shutil

seven_universities_name_list = ["Beihang University", "Beijing Institute of Technology", "Harbin Engineering University", "Northwestern Polytechnical University", "Nanjing University of Science & Technology", "Nanjing University of Aeronautics & Astronautics", "Harbin Institute of Technology"]
year_list = ["2018", "2019", "2020", "2021", "2022"]
input_with_year = pd.read_csv(os.path.join('input-with-year.txt'), delimiter="\t", dtype=str).dropna().values.tolist()
year_dic = {}
for article in input_with_year:
    year = article[1]
    if year not in year_dic:
        year_dic[year] = []
    year_dic[year].append(article[0])

coord_dic = {}
coor_dic_path = os.path.join('node-with-country.xlsx')
coor_dic_pd = pd.read_excel(coor_dic_path, dtype=str).dropna().values.tolist()
# create coord_dic
for i in coor_dic_pd:
    coord_dic[i[1]] = [i[3], i[4]]

map_output_path = os.path.join('c2_wosa_university_year_basedd_GIS','maps')
# remove map_output_path folder
if os.path.exists(map_output_path):

    shutil.rmtree(map_output_path)
# create map_output_path folder
if not os.path.exists(map_output_path):
    os.makedirs(map_output_path)

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
        test = univ_pairs.items()
        pair_list = list(univ_pairs.items())
        # n+1 here because we want to remove the target_university itself
        if len(pair_list) <= n:
            n_without_target_university = len(pair_list)
        else:
            n_without_target_university = n+1
        univ_pairs_top_n = dict(pair_list[:n_without_target_university])
        univ_name_top_n_list = []
        for univ_pair in univ_pairs_top_n:
            if univ_pair[0] != target_university:
                univ_name_top_n_list.append(univ_pair[0])
            if univ_pair[1] != target_university:
                univ_name_top_n_list.append(univ_pair[1])
        univ_name_top_n_list = list(set(univ_name_top_n_list))
        map_center = coord_dic[target_university]
        m = folium.Map(location=map_center, zoom_start=2)      
        for name in univ_name_top_n_list:
            coords = coord_dic[name]
            folium.Marker(location=coords, popup=name).add_to(m)
        map_output_path = os.path.join('c2_wosa_university_year_basedd_GIS','maps')
        map_output_path = os.path.join(map_output_path, target_university)
        if not os.path.exists(map_output_path):
            os.makedirs(map_output_path)
        map_output_path = os.path.join(map_output_path, target_university + "_" +year + '.html')
        m.save(map_output_path)




print('Finished!')