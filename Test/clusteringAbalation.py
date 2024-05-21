from sklearn.cluster import MeanShift
import pandas as pd
from sklearn.metrics import adjusted_rand_score
from sklearn.cluster import HDBSCAN

def compute_purity(df, cluster_col='Cluster', label_col='Political leanings'):
    # 遍歷每個群集
    clusters = df[cluster_col].unique()
    print(f"Total {len(clusters)} Clusters")
    total_purity = 0
    for cluster in clusters:
        cluster_df = df[df[cluster_col] == cluster]
        most_common = cluster_df[label_col].value_counts().idxmax()
        purity = cluster_df[label_col].value_counts().max() / len(cluster_df)
        total_purity += len(cluster_df) * purity
        print(f"Cluster {cluster} purity: {purity:.4f}")
    total_purity /= len(df)
    print(f"Overall purity: {total_purity:.4f}")

def compute_recall(df, cluster_col='Cluster', label_col='Political leanings'):
    labels = df[label_col].unique()
    total_recall = 0
    for label in labels:
        label_df = df[df[label_col] == label]
        most_common_cluster = label_df[cluster_col].value_counts().idxmax()
        recall = label_df[cluster_col].value_counts().max() / len(label_df)
        total_recall += len(label_df) * recall
        print(f"Label {label} recall: {recall:.4f}")
    total_recall /= len(df)
    print(f"Overall recall: {total_recall:.4f}")

def compute_precision(df, cluster_col='Cluster', label_col='Political leanings'):
    clusters = df[cluster_col].unique()
    total_precision = 0
    for cluster in clusters:
        cluster_df = df[df[cluster_col] == cluster]
        most_common = cluster_df[label_col].value_counts().idxmax()
        precision = cluster_df[label_col].value_counts().max() / len(cluster_df)
        total_precision += len(cluster_df) * precision
        print(f"Cluster {cluster} precision: {precision:.4f}")
    total_precision /= len(df)
    print(f"Overall precision: {total_precision:.4f}")

def compute_f1(df, cluster_col='Cluster', label_col='Political leanings'):
    clusters = df[cluster_col].unique()
    labels = df[label_col].unique()
    
    total_f1 = 0
    for cluster in clusters:
        cluster_df = df[df[cluster_col] == cluster]
        for label in labels:
            precision = len(cluster_df[cluster_df[label_col] == label]) / len(cluster_df)
            recall = len(cluster_df[cluster_df[label_col] == label]) / len(df[df[label_col] == label])
            if precision + recall != 0:
                f1 = 2 * precision * recall / (precision + recall)
                total_f1 += len(cluster_df) * f1
                print(f"F1-measure for Cluster {cluster} with label {label}: {f1:.4f}")
    total_f1 /= len(df)
    print(f"Overall F1-measure: {total_f1:.4f}")
#####     請根據要進行 abalation 的檔案修改底線處     #########
df = pd.read_csv('../../Result/_/_.csv')                  #
###########################################################

X = df[['x', 'y']]

# 使用 Mean Shift 來進行聚類
ms = MeanShift()
ms.fit(X)

# 使用 HDBScan 來進行聚類
#ms = HDBSCAN()
#ms.fit(X)


# 取得分群結果
labels = ms.labels_
print((labels))
# 把分群結果添加回 DataFrame
df['Cluster'] = labels

cluster_sizes = df['Cluster'].value_counts()

print("Cluster sizes:")
print(cluster_sizes)

# 顯示結果
print('-----Purity-----')
compute_purity(df)
print('\n-----Recall-----')
compute_recall(df)
print('\n-----ARI-----')
ari = adjusted_rand_score(df['Political leanings'], df['Cluster'])
print(f"Adjusted Rand Index: {ari}")
