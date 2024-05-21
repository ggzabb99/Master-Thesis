import json
import networkx as nx


# 讀取 JSON 檔案
def load_graph_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    G = nx.Graph()
    for node in data['nodes']:
        G.add_node(node['id'])
    for edge in data['links']:
        G.add_edge(edge['source'], edge['target'])
    
    return G

# 指定 JSON 檔案的路徑
json_file_path = '../Framework/GraphSAGE-master/data/Table_4_1/TIU/TIU-G.json'

# 從 JSON 檔案加載圖
G = load_graph_from_json(json_file_path)

# 以下是之前的計算代碼
node_count = G.number_of_nodes()
edge_count = G.number_of_edges()
average_degree = sum(dict(G.degree()).values()) / node_count
graph_density = nx.density(G)
connected_components = nx.number_connected_components(G)
average_shortest_path_length = nx.average_shortest_path_length(G) if nx.is_connected(G) else "N/A"

# 輸出結果
print("Node Count:", node_count)
print("Edge Count:", edge_count)
print("Average Degree:", average_degree)
print("Graph Density:", graph_density)
print("Connected Components:", connected_components)
print("Average Shortest Path Length:", average_shortest_path_length)
