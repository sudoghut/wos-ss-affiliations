import pandas as pd
import networkx as nx

seven_universities_name_list = ["Beihang University", "Beijing Institute of Technology", "Harbin Engineering University", "Northwestern Polytechnical University", "Nanjing University of Science & Technology", "Nanjing University of Aeronautics & Astronautics", "Harbin Institute of Technology"]

def create_top_centrality_groups():
    top_centrality = {}
    for centrality_type, centrality in centrality_dict.items():
        print(f"Creating Top {centrality_type} Groups...")
        for university_id in sever_universities_id_list:
            neighbors_centrality = {neighbor_id: centrality[neighbor_id] for neighbor_id in G.neighbors(university_id)}
            top_neighbors = sorted(neighbors_centrality.items(), key=lambda x: x[1], reverse=True)[:top_count]
            top_centrality[university_id] = top_neighbors
        output_data = []

        for university_id, neighbors in top_centrality.items():
            university_label = G.nodes[university_id]['Label']
            for neighbor_id, centrality in neighbors:
                neighbor_label = G.nodes[neighbor_id]['Label']
                output_data.append({
                    'University Label': university_label,
                    'University ID': university_id,
                    'Neighbor Label': neighbor_label,
                    'Neighbor ID': neighbor_id,
                    centrality_type: centrality
                })
        output_df = pd.DataFrame(output_data)
        output_df.to_csv(f'top_{centrality_type}.csv', index=False)

nodes_df = pd.read_csv('node.csv')
edges_df = pd.read_csv('edge.csv')

print("Creating Graph...")
G = nx.from_pandas_edgelist(edges_df, 'Source', 'Target', create_using=nx.Graph())
print("Adding Labels...")
for _, row in nodes_df.iterrows():
    G.nodes[row['Id']]['Label'] = row['Label']
print("Computing Degreeness Centrality...")
degree_centrality = nx.degree_centrality(G)
print("Computing Closeness Centrality...")
closeness_centrality = nx.closeness_centrality(G)
# closeness_centrality = degree_centrality
print("Computing Betweenness Centrality...")
betweenness_centrality = nx.betweenness_centrality(G)
# betweenness_centrality = degree_centrality
print("Computing Eigenvector Centrality...")
eigenvector_centrality = nx.eigenvector_centrality(G)
# eigenvector_centrality =degree_centrality

centrality_dict = {
    "degree_centrality": degree_centrality,
    "closeness_centrality": closeness_centrality,
    "betweenness_centrality": betweenness_centrality,
    "eigenvector_centrality": eigenvector_centrality
}

degree_df = pd.DataFrame(list(degree_centrality.items()), columns=['Id', 'Degree Centrality'])
closeness_df = pd.DataFrame(list(closeness_centrality.items()), columns=['Id', 'Closeness Centrality'])
betweenness_df = pd.DataFrame(list(betweenness_centrality.items()), columns=['Id', 'Betweenness Centrality'])
eigenvector_df = pd.DataFrame(list(eigenvector_centrality.items()), columns=['Id', 'Eigenvector Centrality'])

centrality_df = pd.merge(nodes_df, degree_df, on='Id')
centrality_df = pd.merge(centrality_df, closeness_df, on='Id')
centrality_df = pd.merge(centrality_df, betweenness_df, on='Id')
centrality_df = pd.merge(centrality_df, eigenvector_df, on='Id')

print("Saving Centrality Measures...")
centrality_df.to_csv('centrality_measures.csv', index=False)

# seven_universities_name_list = ['Beijing University of Technology','University of Houston']
sever_universities_id_list = [node_id for node_id, node_label in G.nodes(data='Label') if node_label in seven_universities_name_list]
top_count = 50
print("Creating Top Centrality Groups...")
create_top_centrality_groups()
print("Finished!")
