import re
import json
import time
import torch
import emoji
import numpy as np
import networkx as nx

from PIL import Image
from datetime import datetime
from sentence_transformers import SentenceTransformer
from transformers import BeitFeatureExtractor, BeitModel, BertForSequenceClassification, BertTokenizer

emoji_pattern = re.compile("["
        u"\U00002700-\U000027BF"  # Dingbats
        u"\U0001F600-\U0001F64F"  # Emoticons
        u"\U00002600-\U000026FF"  # Miscellaneous Symbols
        u"\U0001F300-\U0001F5FF"  # Miscellaneous Symbols And Pictographs
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\U0001F680-\U0001F6FF"  # Transport and Map Symbols
        u'\U00002B55'
        u'\U0001F7E1'
        u'\U000023E9-\U000023FA'
                                "]+", flags=re.UNICODE)

def imgEmbedNormalize(embedding):
    img_max = 550
    img_min = -900
    labels_embedding = [ 2 * ((x - img_min) / (img_max - img_min)) - 1 for x in embedding]
    return labels_embedding

def postTimetoList(postTime):
    
    start_day= datetime.strptime('2010/01/01 00:00:00','%Y/%m/%d %H:%M:%S')
    end_day = datetime.now()
    max_day = (end_day - start_day).days
    post_day = datetime.strptime(postTime,'%Y/%m/%d %H:%M:%S')
    few_days = (post_day - start_day).days
    normalize = few_days / (max_day)
    return [normalize]
    

def removeHU(text):
    text = re.sub("#[\u4e00-\u9fa5A-Za-z0-9_]+","", text)
    text = re.sub(r'http\S+', '', text)
    text = emoji.replace_emoji(text, replace='')
    return text

def jaccard(list1, list2):
    list1_userID = []
    list2_userID = []

    for user in list1:
        list1_userID.append(user['user_ID'])
    
    for user in list2:
        list2_userID.append(user['user_ID'])
    
    set1 = set(list1_userID)
    set2 = set(list2_userID)
    score = float(len(set1.intersection(set2))) / len(set1.union(set2))
    return score


content = []
ws_content = []
pos_content = []


########### S-BERT ###########

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2') 

########### BEiT ###########

image_processor = BeitFeatureExtractor.from_pretrained("microsoft/beit-base-patch16-224-pt22k")
Beitmodel = BeitModel.from_pretrained("microsoft/beit-base-patch16-224-pt22k")

########### Sentiment ###########

Sentiment_tokenizer=BertTokenizer.from_pretrained('IDEA-CCNL/Erlangshen-Roberta-110M-Sentiment')
Sentiment_model=BertForSequenceClassification.from_pretrained('IDEA-CCNL/Erlangshen-Roberta-110M-Sentiment')


########### Start Process ###########

keyword_content = []
keyword_content_embedding = []

#####     讀取要偵測立場的檔案     #####
CCoE_keyword_file = open('../../Dataset/referendum.jsonl', 'r', encoding = "UTF-8")

for line in CCoE_keyword_file:

    jstring = json.loads(line)
    jstring['body'] = removeHU(jstring['body'])

    keyword_content.append(jstring)

########### text & sentiment & time & image ###########

image_count = 1
start = time.time()
for i in range(len(keyword_content)):
    print(keyword_content[i]['_rid'])
    
    #####     貼文內容     ####################
    text = keyword_content[i]['body']        #
    embeddings = model.encode(text)          #
    content_embedding = embeddings.tolist()  #
    ##########################################

    #####     情緒     ##################################################################
    output = Sentiment_model(torch.tensor([Sentiment_tokenizer.encode(text)]))          #
    sentiment_embedding = torch.nn.functional.softmax(output.logits,dim=-1).tolist()[0] #
    #####################################################################################

    #####     發文時間     ######################
    postTime = keyword_content[i]['post_time'] #
    postTime = postTimetoList(postTime)        #
    ############################################

    ######     圖片     ##########################################################
    labels_embedding = []                                                        #
                                                                                 #
    if len(keyword_content[i]['image_links']) >= 1:                              #
        image_name = keyword_content[i]['_rid']                                  #
        image = Image.open(f'../../Image/{image_name}.jpg')                      #
        print('image_count: ', image_count)                                      #
        print('img_size: ', image.size)                                          #
        if image.height == 1 or image.width == 1:                                #
            labels_embedding = [0] * 768                                         #
            image_count += 1                                                     #
        else:                                                                    #
            inputs = image_processor(image, return_tensors="pt")                 #
            with torch.no_grad():                                                #
                outputs = Beitmodel(**inputs, output_hidden_states=True)         #
            last_hidden_state = outputs.hidden_states[-1]                        #
            labels_embedding = (last_hidden_state[:, 0, :].detach())[0].tolist() #
            image_count += 1                                                     #
    else:                                                                        #
        labels_embedding = [0] * 768                                             #
                                                                                 #
    labels_embedding = imgEmbedNormalize(labels_embedding)                       #
    ##############################################################################

    #####     請注意，若要還原 abalation study 結果，需要調整此處，相關設定請參考readme     #######################
    keyword_content_embedding.append(content_embedding + sentiment_embedding + postTime + labels_embedding)#
    ########################################################################################################
    print('Embedding_len: ', len(keyword_content_embedding[i]))
end = time.time()
print('time: ', end-start)


########### Jaccard index ###########

embedding_similarity = [[0] * len(keyword_content_embedding) for col in range(len(keyword_content_embedding))]
start = time.time()
for i in range(len(embedding_similarity)):
    for j in range(i+1, len(embedding_similarity)):
        #####     請注意，若要還原 user abalation study 結果，需要調整此處，相關設定請參考readme     ########
        score = jaccard(keyword_content[i]['interactions'][:], keyword_content[j]['interactions'][:])#
        ##############################################################################################
        embedding_similarity[i][j] = score
        embedding_similarity[j][i] = score

embedding_similarity_1D = []
for i in range(len(embedding_similarity)):
    embedding_similarity_1D += embedding_similarity[i]

embedding_similarity_1D.sort()
cut_index = 0
for i in range(len(embedding_similarity_1D)):
    if embedding_similarity_1D[i] != 0:
        cut_index = i
        break
print('cut: ', cut_index)
embedding_similarity_1D = embedding_similarity_1D[cut_index:len(embedding_similarity_1D)]
#####     請注意，若要還原 threashold abalation study 結果，需要調整此處，相關設定請參考readme     #####
embedding_similarity_median = np.percentile(embedding_similarity_1D, 50)                        #
################################################################################################

#####     Jaccard index 根據建立邊     #####
for i in range(len(embedding_similarity)):
    for j in range(len(embedding_similarity[i])):
        if embedding_similarity[i][j] >= embedding_similarity_median:
            embedding_similarity[i][j] = 1
        else:
            embedding_similarity[i][j] = 0

########### For GraphSAGE ###########
Graphsage = nx.Graph()

# add nodes
for i in range(len(keyword_content_embedding)):
    Graphsage.add_nodes_from([(i, {'test': False, 'id': i, 'val': False})])

# add edges
for i in range(len(embedding_similarity)):
    for j in range(i+1, len(embedding_similarity)):
        if embedding_similarity[i][j] == 1:
            Graphsage.add_edge(i, j)
print(nx.node_link_data(Graphsage))

# get nodes id
print(nx.get_node_attributes(Graphsage, "id"))

#####     請注意，底線處可自行設定資料夾與名稱，惟連接號「-」後續的檔案名稱不可變更     ##########
with open('./GraphSAGE-master/master/_/_-G.json', 'w', encoding='utf-8') as f:        #
    json.dump(nx.node_link_data(Graphsage), f, ensure_ascii=False)                    #
                                                                                      #
with open('./GraphSAGE-master/master/_/_-id_map.json', 'w', encoding='utf-8') as f:   #
    json.dump(nx.get_node_attributes(Graphsage, "id"), f, ensure_ascii=False)         #
                                                                                      #
with open('./GraphSAGE-master/master/_/_-class_map.json', 'w', encoding='utf-8') as f:#
    json.dump(nx.get_node_attributes(Graphsage, "id"), f, ensure_ascii=False)         #
                                                                                      #
np.save('./GraphSAGE-master/master/_/_-feats', np.asarray(keyword_content_embedding)) #
#######################################################################################
