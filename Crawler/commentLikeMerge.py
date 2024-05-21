import json
import re

like_content = []
comment_content = []
merge_content = []

likeList_content = []

#####     讀取按讚與留言的使用者，同時處理只讓重複出現的使用者保留一次     #####
with open('./output_like.jsonl', 'r', encoding='utf-8') as like, open('./output_comment.jsonl', 'r', encoding='utf-8') as comment:

    for like_line in like:

        like_line = json.loads(like_line)
        like_content.append(like_line)

    for comment_line in comment:

        comment_line = json.loads(comment_line)
        comment_content.append(comment_line)

    for like_line in like_content:
        
        comment_search = next((comment for comment in comment_content if comment["url"] == like_line['url']), None)

        if comment_search == None:
            merge_content.append(like_line)
        else:
            merge = {**comment_search, **like_line}
            merge_content.append(merge)

        



with open('D:\Project_File\china_fb_fanpage\china_fb_fanpage_merge.jsonl', 'r', encoding='utf-8') as likeList:
    for likeList_line in likeList:
        likeList_line = json.loads(likeList_line)
        likeList_content.append(likeList_line)
    
    for merge_line in merge_content:
        ridSearch = next((rid for rid in likeList_content if rid["url"] == merge_line['url']), None)
        
        if ridSearch == None:
            print('Error: ', merge_line['url'])
        else:
            merge_line['_rid'] = ridSearch['_rid']


likeList_content = []
Done_content = []
#####     讀取 input_example，篩選後留下有使用者互動的貼文     #####
with open('./input_example.jsonl', 'r', encoding='utf-8') as likeList:    
    for likeList_line in likeList:
        likeList_line = json.loads(likeList_line)
        likeList_content.append(likeList_line)

    for likeList_line in likeList_content:

        ridSearch = next((rid for rid in merge_content if rid["_rid"] == likeList_line['_rid']), None)
        if ridSearch == None:
            print('Error: ', likeList_line['url'])
        else:
            likeList_line['interactions'] = ridSearch['interactions']
            Done_content.append(likeList_line)
print('Done_content: ', len(Done_content))


with open('./output_merge.jsonl', 'w', encoding='utf-8') as merge:
    for likeList_line in Done_content:
        json.dump(likeList_line, merge, ensure_ascii=False)
        merge.write('\n')

