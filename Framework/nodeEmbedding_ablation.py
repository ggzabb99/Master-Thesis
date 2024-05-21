import re
import time
import json
import umap
import torch
import emoji
import pandas as pd

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

all_agree = ['蔡英文 Tsai Ing-wen', '賴清德', '蘇貞昌', '只是堵藍', '打馬悍將粉絲團', '莫羽静與她的墨水故事', '孟買春秋', '鄉民挺起來']
all_disagree = ['朱立倫', '江啟臣', '羅智強', '立法委員 吳斯懷', '普魯士藍', '大腦是個好東西，希望你也有一個', '政客爽' , '趙少康']
neutral = ['黃國昌', '時代力量 New Power Party', '柯文哲', '台灣民眾黨', '不禮貌鄉民團', '特急件小周的人渣文本']

stance = []


for line in CCoE_keyword_file:  
    #print(line)
    jstring = json.loads(line)
    jstring['body'] = removeHU(jstring['body'])
    
    if jstring['from_name'] in all_agree:
        stance.append('Agree')
    elif jstring['from_name'] in all_disagree:
        stance.append('Disagree')
    elif jstring['from_name'] in neutral:
        stance.append('Neutral')
    else:
        print(jstring['from_name'])
    keyword_content.append(jstring)

print(f'content len:{len(keyword_content)}')
print(f'stance len:{len(stance)}')


########### body & sentiment & time & image ###########

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

########### For UMAP ###########

Umap = umap.UMAP()
Umap = Umap.fit_transform(keyword_content_embedding)
print(f'umap len:{len(Umap)}')

x1 = []
y1 = []
for i in range(len(Umap)):
    x1.append(Umap[i][0])
    y1.append(Umap[i][1])

print('x:', len(x1))
print('y:', len(y1))
print('stance:', len(stance))
df = pd.DataFrame({
    'x':x1,
    'y':y1,
    'Political leanings':stance,
})
#####     請根據產生T、I或TI來設定檔名     ################
df.to_csv('../../Result/Table_4_1/_.csv', index=False)#
#######################################################
