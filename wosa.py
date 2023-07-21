import pandas as pd

# input data to list
# input_list = pd.read_csv('input-small.txt', delimiter="\t").values.tolist()
input_list = pd.read_csv('input.txt', delimiter="\t").values.tolist()
node_output_dic = {}
edge_output_list = []
idx = 0
print(input_list[:5])
counter = 0

total_article = len(input_list)
for article in input_list:
    if counter % 50000 == 0:
        print("Processing {}/{} article".format(input_list.index(article)+1, total_article))
    counter += 1
    article_list = []
    # split article insts by ; and strip space
    article_insts = [inst.strip().replace(",","") for inst in article[0].split(';')]
    article_insts = list(set(article_insts))
    if len(article_insts) == 1: continue
    # Create article insts pairs, no repeat
    for i in range(len(article_insts)):
        if article_insts[i] not in node_output_dic:
            idx += 1
            node_output_dic[article_insts[i]] = idx
        for j in range(i+1, len(article_insts)):
            if article_insts[j] not in node_output_dic:
                idx += 1
                node_output_dic[article_insts[j]] = idx
            article_list.append([node_output_dic[article_insts[i]], node_output_dic[article_insts[j]]])
    edge_output_list += article_list

df = pd.DataFrame(list(node_output_dic.items()), columns=['Label', 'Id'])
df = df[['Id', 'Label']]
df.to_csv('node.csv', index=False, encoding='utf-8')
df = pd.DataFrame(edge_output_list, columns=['Source', 'Target'])
df.to_csv('edge.csv', index=False, encoding='utf-8')
print(df.head())
print("Finished!")
