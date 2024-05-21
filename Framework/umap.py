import json
import numpy as np
from collections import OrderedDict, Counter
import matplotlib.pyplot as plt
import pandas as pd
import umap
import pyreadr

map = []
nodeID = []
ID_map = {}
#####     請修改底線處的名稱以確認要進行降維的檔案     ##############################################################
x = np.load("./GraphSAGE-master/unsup-_/graphsage_maxpool_small_0.000010/val.npy")                            #
with open('./GraphSAGE-master/unsup-_/graphsage_maxpool_small_0.000010/val.txt', 'r', encoding='utf-8') as f: #
###############################################################################################################
    for line in f:
        nodeID.append(int(line))

for i in range(len(nodeID)):
    ID_map[nodeID[i]] = x[i]
print(ID_map[0])
for i in range(len(ID_map)):
    map.append(ID_map[i])
print(map[0])
print(len(map[0]))

x1 = []
y1 = []
z = []

Umap = umap.UMAP()
Umap = Umap.fit_transform(map)
print(len(Umap))

fanpages_stance = {
    '朱立倫':'KMT',
    '江啟臣':'KMT',
    '羅智強':'KMT',
    '立法委員 吳斯懷':'KMT',
    '趙少康':'KMT',
    '普魯士藍':'Pan-blue celebrities',
    '大腦是個好東西，希望你也有一個':'Pan-blue celebrities',
    '政客爽':'Pan-blue celebrities',
    '蔡英文 Tsai Ing-wen':'DPP',
    '賴清德':'DPP',
    '蘇貞昌':'DPP',
    '黃國昌':'NPP',
    '時代力量 New Power Party':'NPP',
    '柯文哲':'TPP',
    '台灣民眾黨':'TPP',
    '不禮貌鄉民團':'Neutral celebrities',
    '特急件小周的人渣文本':'Neutral celebrities',
    '只是堵藍':'Pan-green celebrities',
    '打馬悍將粉絲團':'Pan-green celebrities',
    '莫羽静與她的墨水故事':'Pan-green celebrities',
    '孟買春秋':'Pan-green celebrities',
    '鄉民挺起來':'Pan-green celebrities',
}

fanpages_ablation = {
    '朱立倫':'Disagree',
    '江啟臣':'Disagree',
    '羅智強':'Disagree',
    '立法委員 吳斯懷':'Disagree',
    '趙少康':'Disagree',
    '普魯士藍':'Disagree',
    '大腦是個好東西，希望你也有一個':'Disagree',
    '政客爽':'Disagree',
    '蔡英文 Tsai Ing-wen':'Agree',
    '賴清德':'Agree',
    '蘇貞昌':'Agree',
    '黃國昌':'Neutral',
    '時代力量 New Power Party':'Neutral',
    '柯文哲':'Neutral',
    '台灣民眾黨':'Neutral',
    '不禮貌鄉民團':'Neutral',
    '特急件小周的人渣文本':'Neutral',
    '只是堵藍':'Agree',
    '打馬悍將粉絲團':'Agree',
    '莫羽静與她的墨水故事':'Agree',
    '孟買春秋':'Agree',
    '鄉民挺起來':'Agree',
}

stance = []
#####     若要針對其他四項議題進行畫圖，請修改檔案名稱     #################
with open('./Dataset/referendum.jsonl', 'r', encoding='utf-8') as f:#
#####################################################################
    for line in f:
        line = json.loads(line)
#####     執行 abalataion 使用 fanpages_ablation；執行畫圖使用 fanpages_stance     #####
        stance.append(fanpages_stance[line['from_name']])                           #
#####################################################################################
fanpages = list(OrderedDict.fromkeys(stance))
print(Counter(stance))

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

for i in range(len(Umap)):
    x1.append(Umap[i][0])
    y1.append(Umap[i][1])

df = pd.DataFrame({
    'x':x1,
    'y':y1,
    'Political leanings':stance,
})
#####     執行 abalation 請使用csv；執行畫圖請使用RData，並請根據不同用途設定檔案名稱     ##################################
#df.to_csv('../../Result/_/_.csv', index=False)                                                                    #
pyreadr.write_rdata('../../Result/_/_.RData', df)                                                                  #
####################################################################################################################
