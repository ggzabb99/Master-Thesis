import json
import re
import emoji
from collections import Counter
import os


number_url = 0
number_post_emojis = 0
number_emojis = 0
number_hashtag = 0
emoji_post_len = 0
mou = 0
def removeHU(text):
    global number_url, number_emojis, mou, number_post_emojis, emoji_post_len, number_hashtag

    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    url_match = url_pattern.findall(text)
    hashtag_match = re.findall(r"#[\u4e00-\u9fa5A-Za-z0-9_]+", text)
    if len(url_match) > 0:
        if "https" in url_match[0]:
            mou += 1
        number_url += 1
    if len(hashtag_match) > 0:
        number_hashtag += 1
    if any(char in emoji.EMOJI_DATA for char in text):
        number_emojis += sum(1 for char in text if char in emoji.EMOJI_DATA)
        number_post_emojis += 1
        emoji_post_len += len(text)
        print(f'emojis:{number_emojis}')
        print(f'number_post_emojis:{number_post_emojis}')

    text = re.sub("#[\u4e00-\u9fa5A-Za-z0-9_]+","", text)
    text = re.sub(r'http\S+', '', text)
    text = text.replace("<br>", "")
    text = emoji.replace_emoji(text, replace='')
    
    return text

referendum_content = []


pan_green_pages = ['只是堵藍', '打馬悍將粉絲團', '莫羽静與她的墨水故事', '孟買春秋', '鄉民挺起來']
official_green_pages = ['蔡英文 Tsai Ing-wen', '賴清德', '蘇貞昌']
pan_blue_pages = ['普魯士藍', '大腦是個好東西，希望你也有一個', '政客爽']
official_blue_pages = ['朱立倫', '江啟臣', '立法委員吳斯懷', '羅智強', '趙少康']
npp = ['黃國昌', '時代力量 New Power Party']
tpp = ['柯文哲', '台灣民眾黨']

post_dict = {
    "只是堵藍" : 0,
    "打馬悍將粉絲團" : 0,
    "莫羽静與她的墨水故事" : 0,
    "孟買春秋" : 0,
    "鄉民挺起來" : 0,
    "蔡英文 Tsai Ing-wen" : 0,
    "賴清德" : 0,
    "蘇貞昌" : 0,
    "普魯士藍" : 0,
    "大腦是個好東西，希望你也有一個" : 0,
    "政客爽" : 0,
    "朱立倫" : 0,
    "江啟臣" : 0,
    "立法委員吳斯懷" : 0,
    "羅智強" : 0,
    "黃國昌" : 0,
    "時代力量 New Power Party" : 0,
    "柯文哲" : 0,
    "台灣民眾黨" : 0,
}

with open('../../Dataset/referendum.jsonl', 'r', encoding='utf-8') as referendum_file:
    for line in referendum_file:
        line = json.loads(line)
        line['body'] = removeHU(line['body'])
        referendum_content.append(line)

print(f'emoji_post_len:{emoji_post_len}')
print(f'number_emojis:{number_emojis}')
print(f'ratio:{number_emojis/emoji_post_len}')

fanpages = Counter()
posts_character = 0
image_path = '../../Image/'
image_count = 0
post_interacters = 0
max_interacters = 0
min_interacters = 10000000
for line in referendum_content:
    if 'from_name' in line:
        fanpages[line['from_name']] += 1
    
    posts_character += len(line['body'])

    file_path = os.path.join(image_path, line['_rid']+'.jpg')

    if os.path.exists(file_path):
        image_count += 1

    post_interacters += len(line['interactions'])

    if len(line['interactions']) > max_interacters:
        max_interacters = len(line['interactions'])
    
    if len(line['interactions']) < min_interacters:
        min_interacters = len(line['interactions'])

print(fanpages)
print(f'# fanpages: {len(fanpages)}')
print(f'# posts: {len(referendum_content)}')
print(f'# images: {image_count}')
print(f'# post characters: {posts_character/len(referendum_content)}')
print(f'# post interacters: {post_interacters/len(referendum_content)}')
print(f'max post interacters: {max_interacters}')
print(f'min post interacters: {min_interacters}')
print(f'# URLs: {number_url}')
print(f'# emojis: {number_emojis}')
print(f'# hashtag: {number_hashtag}')