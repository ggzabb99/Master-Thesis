from ckiptagger import WS, construct_dictionary
from ckip_transformers.nlp import CkipPosTagger
from collections import Counter
import pandas as pd
import json
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

def clean(sentence_ws):
    sentence_ws = sentence_ws[0]
    short_sentence = []
    for word_ws in sentence_ws:
        is_not_one_charactor = not (len(word_ws) == 1)
        # 組成串列
        is_no_br = 'br' not in word_ws
        is_no_http = 'http' not in word_ws
        if is_not_one_charactor and is_no_br and is_no_http:
            short_sentence.append(f"{word_ws}")
    return short_sentence

def cleanPOS(sentence_ws, sentence_pos):
    short_sentence = []
    stop_pos = set(['Nep', 'Nh', 'Nb']) # 這 3 種詞性不保留
    for word_ws, word_pos in zip(sentence_ws, sentence_pos):
        # 只留名詞和動詞
        is_N_or_V = word_pos.startswith("V") or word_pos.startswith("N")
        # 去掉名詞裡的某些詞性
        is_not_stop_pos = word_pos not in stop_pos

        if is_N_or_V and is_not_stop_pos:
            short_sentence.append(f"{word_ws}")
    return short_sentence

def segSentance(content, dictionary):
    return ws([content], coerce_dictionary=dictionary, sentence_segmentation = True, segment_delimiter_set = {",", "。", ":", "?", "!", ";"})

ws = WS("./ws/data")

dictionary = construct_dictionary({
    "公投綁大選": 10,
    "4個不同意": 10,   # 指定權重
    "四個不同意": 9,
    "台灣更有力": 10,
    "不同意": 8,
    "四個都同意": 10,
    "三接": 10,
    "美豬": 10,
    "反萊豬": 10,
    "萊豬": 9,
    "反核四": 10,
    "核四": 9,
    "中國國民黨": 10,
    "核電廠": 10,
    "國民黨": 9,
    "民進黨": 10,
    "核電廠": 10,
    "藻礁": 10,
    "蔡英文": 10,
    "台灣": 10,
    "萊克多巴胺": 10,
    "瘦肉精": 10,
    "萊劑": 10,
    "四大公投": 10,
    "公民投票": 10,
    "1218": 10,
    "12月18日": 10,
    "氣候變遷": 10,
    '反對台獨': 10,
    '反台獨': 9,
    '台獨': 8,
    '九二共識': 10,
    '天然氣第三接收站': 10,
    '第三天然氣接收站': 10,
})

green_pages = ['只是堵藍', '打馬悍將粉絲團', '莫羽静與她的墨水故事', '孟買春秋', '蔡英文 Tsai Ing-wen', '賴清德', '蘇貞昌', '鄉民挺起來']
pan_green_pages = ['只是堵藍', '打馬悍將粉絲團', '莫羽静與她的墨水故事', '孟買春秋', '鄉民挺起來']
official_green_pages = ['蔡英文 Tsai Ing-wen', '賴清德', '蘇貞昌']
blue_pages = ['普魯士藍', '大腦是個好東西，希望你也有一個', '朱立倫', '江啟臣', '立法委員吳斯懷', '羅智強', '政客爽', '趙少康']
pan_blue_pages = ['普魯士藍', '大腦是個好東西，希望你也有一個', '政客爽']
official_blue_pages = ['朱立倫', '江啟臣', '立法委員吳斯懷', '羅智強', '趙少康']
npp = ['黃國昌', '時代力量 New Power Party']
tpp = ['柯文哲', '台灣民眾黨']


green_pages_content = []
pan_green_pages_content = []
official_green_pages_content = []
pan_blue_pages_content = []
blue_pages_content = []
official_blue_pages_content = []
npp_content = []
tpp_content = []

with open('../../Dataset/referendum.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        line = json.loads(line)

        #Pan Green#
        if any([x in line['from_name'] for x in pan_green_pages]):
            if line['from_name'] == '莫羽静與她的墨水故事':
                if line['body'].find('同島一命') != -1:
                    line['body'] = line['body'][:line['body'].find('同島一命')]
                
            pan_green_pages_content.append(line['body'])
            green_pages_content.append(line['body'])

        #Official Green#
        if any([x in line['from_name'] for x in official_green_pages]):
            if '非核家園' in  line['body']:
                print(line['body'])
            official_green_pages_content.append(line['body'])
            green_pages_content.append(line['body'])

        #Pan Blue#
        if any([x in line['from_name'] for x in pan_blue_pages]):                
            pan_blue_pages_content.append(line['body'])
            blue_pages_content.append(line['body'])    

        #Official Blue#
        if any([x in line['from_name'] for x in official_blue_pages]):                
            official_blue_pages_content.append(line['body'])
            blue_pages_content.append(line['body'])

        if any([x in line['from_name'] for x in npp]):                
            npp_content.append(line['body'])

        if any([x in line['from_name'] for x in tpp]):                
            tpp_content.append(line['body'])


green_pages_ws = []
pan_green_pages_ws = []
official_green_pages_ws = []
blue_pages_ws = []
pan_blue_pages_ws = []
official_blue_pages_ws = []
npp_ws = []
tpp_ws = []


for line in pan_green_pages_content:
    line = ws([line], coerce_dictionary=dictionary, sentence_segmentation = True, segment_delimiter_set = {",", "。", ":", "?", "!", ";"})
    pan_green_pages_ws.append(line)
    green_pages_ws.append(line)

for line in official_green_pages_content:
    line = ws([line], coerce_dictionary=dictionary, sentence_segmentation = True, segment_delimiter_set = {",", "。", ":", "?", "!", ";"})
    official_green_pages_ws.append(line)
    green_pages_ws.append(line)

for line in pan_blue_pages_content:
    line = ws([line], coerce_dictionary=dictionary, sentence_segmentation = True, segment_delimiter_set = {",", "。", ":", "?", "!", ";"})
    pan_blue_pages_ws.append(line)
    blue_pages_ws.append(line)

for line in official_blue_pages_content:
    line = ws([line], coerce_dictionary=dictionary, sentence_segmentation = True, segment_delimiter_set = {",", "。", ":", "?", "!", ";"})
    official_blue_pages_ws.append(line)
    blue_pages_ws.append(line)

for line in npp_content:
    line = ws([line], coerce_dictionary=dictionary, sentence_segmentation = True, segment_delimiter_set = {",", "。", ":", "?", "!", ";"})
    npp_ws.append(line)


for line in tpp_content:
    line = ws([line], coerce_dictionary=dictionary, sentence_segmentation = True, segment_delimiter_set = {",", "。", ":", "?", "!", ";"})
    tpp_ws.append(line)

clean_green_pages = []
clean_pan_green_pages = []
clean_official_green_pages = []
clean_blue_pages = []
clean_pan_blue_pages = []
clean_official_blue_pages = []
clean_npp = []
clean_tpp = []


for sentence_ws in pan_green_pages_ws:
    short = clean(sentence_ws)
    clean_pan_green_pages.append(short)
    clean_green_pages.append(short)

for sentence_ws in official_green_pages_ws:
    short = clean(sentence_ws)
    clean_official_green_pages.append(short)
    clean_green_pages.append(short)

for sentence_ws in pan_blue_pages_ws:
    short = clean(sentence_ws)
    clean_pan_blue_pages.append(short)
    clean_blue_pages.append(short)

for sentence_ws in official_blue_pages_ws:
    short = clean(sentence_ws)
    clean_official_blue_pages.append(short)
    clean_blue_pages.append(short)

for sentence_ws in npp_ws:
    short = clean(sentence_ws)
    clean_npp.append(short)

for sentence_ws in tpp_ws:
    short = clean(sentence_ws)
    clean_tpp.append(short)

pos_driver = CkipPosTagger(model="bert-base")

result_green_pages = []
result_pan_green_pages = []
result_official_green_pages = []
result_blue_pages = []
result_pan_blue_pages = []
result_official_blue_pages = []
result_china_pages = []
result_pro_china_pages = []
result_official_china_pages = []
result_npp = []
result_tpp = []


pos_list = pos_driver(clean_pan_green_pages)
for sentence_ws,  sentence_pos in zip(clean_pan_green_pages, pos_list):
    short = cleanPOS(sentence_ws, sentence_pos)
    result_pan_green_pages.append(short)
    result_green_pages.append(short)

pos_list = pos_driver(clean_official_green_pages)
for sentence_ws,  sentence_pos in zip(clean_official_green_pages, pos_list):
    short = cleanPOS(sentence_ws, sentence_pos)
    result_official_green_pages.append(short)
    result_green_pages.append(short)

pos_list = pos_driver(clean_pan_blue_pages)
for sentence_ws,  sentence_pos in zip(clean_pan_blue_pages, pos_list):
    short = cleanPOS(sentence_ws, sentence_pos)
    result_pan_blue_pages.append(short)
    result_blue_pages.append(short)

pos_list = pos_driver(clean_official_blue_pages)
for sentence_ws,  sentence_pos in zip(clean_official_blue_pages, pos_list):
    short = cleanPOS(sentence_ws, sentence_pos)
    result_official_blue_pages.append(short)
    result_blue_pages.append(short)

pos_list = pos_driver(clean_npp)
for sentence_ws,  sentence_pos in zip(clean_npp, pos_list):
    short = cleanPOS(sentence_ws, sentence_pos)
    result_npp.append(short)

pos_list = pos_driver(clean_tpp)
for sentence_ws,  sentence_pos in zip(clean_tpp, pos_list):
    short = cleanPOS(sentence_ws, sentence_pos)
    result_tpp.append(short)

green_merge = []
pan_green_merge = []
official_green_merge = []
blue_merge = []
pan_blue_merge = []
official_blue_merge = []
npp_merge = []
tpp_merge = []


for line in result_green_pages:
    green_merge += line
green_merge = Counter(green_merge)

for line in result_pan_green_pages:
    pan_green_merge += line
pan_green_merge = Counter(pan_green_merge)

for line in result_official_green_pages:
    official_green_merge += line
official_green_merge = Counter(official_green_merge)

for line in result_blue_pages:
    blue_merge += line
blue_merge = Counter(blue_merge)

for line in result_pan_blue_pages:
    pan_blue_merge += line
pan_blue_merge = Counter(pan_blue_merge)

for line in result_official_blue_pages:
    official_blue_merge += line
official_blue_merge = Counter(official_blue_merge)

for line in result_npp:
    npp_merge += line
npp_merge = Counter(npp_merge)

for line in result_tpp:
    tpp_merge += line
tpp_merge = Counter(tpp_merge)

green_df = pd.DataFrame.from_dict(green_merge, orient='index', columns=['value'])
green_df = green_df.sort_values(by='value', ascending=False)
pan_green_df = pd.DataFrame.from_dict(pan_green_merge, orient='index', columns=['value'])
pan_green_df = pan_green_df.sort_values(by='value', ascending=False)
official_green_df = pd.DataFrame.from_dict(official_green_merge, orient='index', columns=['value'])
official_green_df = official_green_df.sort_values(by='value', ascending=False)
blue_df = pd.DataFrame.from_dict(blue_merge, orient='index', columns=['value'])
blue_df = blue_df.sort_values(by='value', ascending=False)
pan_blue_df = pd.DataFrame.from_dict(pan_blue_merge, orient='index', columns=['value'])
pan_blue_df = pan_blue_df.sort_values(by='value', ascending=False)
official_blue_df = pd.DataFrame.from_dict(official_blue_merge, orient='index', columns=['value'])
official_blue_df = official_blue_df.sort_values(by='value', ascending=False)
npp_df = pd.DataFrame.from_dict(npp_merge, orient='index', columns=['value'])
npp_df = npp_df.sort_values(by='value', ascending=False)
tpp_df = pd.DataFrame.from_dict(tpp_merge, orient='index', columns=['value'])
tpp_df = tpp_df.sort_values(by='value', ascending=False)

green_df.to_csv('../../Result/Table_4_6/green.csv', encoding='utf-8')
official_green_df.to_csv('../../Result/Table_4_6/official_green.csv', encoding='utf-8')
blue_df.to_csv('../../Result/Table_4_6/blue.csv', encoding='utf-8')
official_blue_df.to_csv('../../Result/Table_4_6/official_blue.csv', encoding='utf-8')
npp_df.to_csv('../../Result/Table_4_6/npp.csv', encoding='utf-8')
tpp_df.to_csv('../../Result/Table_4_6/tpp.csv', encoding='utf-8')