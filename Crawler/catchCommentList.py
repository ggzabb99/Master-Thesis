import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
from random import randint
import re

fb_url = "https://m.facebook.com/"


like_class_name = {
    'open' : '_45m8',
    'close' : 'x1i10hfl x6umtig x1b1mbwd xaqea5y xav7gou x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x87ps6o x1lku1pv x1a2a7pz x6s0dn4 x14yjl9h xudhj91 x18nykt9 xww2gxu x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xl56j7k xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xc9qbxq x14qfxbe x1qhmfi1',
    'window' : 'x1qjc9v5 x78zum5 xdt5ytf x1n2onr6 x1al4vs7 x1jx94hy x1qpq9i9 xdney7k xu5ydu1 xt3gfkd x104qc98 x1gj8qfm x1iyjqo2 x6ikm8r x10wlt62 x1likypf x7b354b x1e9k66k x12l8kdc',
    'users' : 'x78zum5 xdt5ytf xz62fqu x16ldp7u',
    'name' : 'x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f',
    'scroll': 'x14nfmen x1s85apg xds687c x5yr21d xg01cxk x10l6tqk x13vifvy x1wsgiic x19991ni xwji4o3 x1kky2od x1sd63oq',
}

def login(driver, login_flag):

    #####     請填寫FB帳號密碼供爬蟲使用，因可能被暫時停止功能，請填寫三組以輪流使用     #####
    if login_flag == 0:
        email = ''
        password = ''
        login_flag = 1
    elif login_flag == 1:
        email = ''
        password = ''
        login_flag = 2
    elif login_flag == 2:
        email = ''
        password = ''
        login_flag = 0
    
    print('Email: ', email)
    driver.get('https://m.facebook.com/')
    time.sleep(2)

    context = driver.find_element("name", 'email')
    context.send_keys(email)
    context = driver.find_element("name", 'pass')
    context.send_keys(password)
    commit = driver.find_element("name",'login')
    commit.click()
    time.sleep(5)
    return login_flag

def set_drive():
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--disable-notifications')
    driver = uc.Chrome(chrome_options=chrome_options)
    userAgent = "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" 
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": userAgent})
    url = "https://m.facebook.com/"
    driver.get(url)
    time.sleep(3)
    return driver


def get_post_id(url, driver):

    soup = BeautifulSoup(driver.page_source, 'lxml')
    if re.search('看來你過度使用了這項功能', soup.text) != None:
        print('Error get post id')
        time.sleep(5)
        return 0
    try:
        data = json.loads((soup.find('div', {'class' : '_5rgr async_like'}))['data-store'])
    except:
        print(f'{url} not a post')
        return 1
    return data['feedback_target']


def open_like_window():
    btms = driver.find_elements(By.CLASS_NAME ,like_class_name['open'])
    
    if len(btms) > 0:
        btms[0].click()
        time.sleep(randint(3,5))
        return True
    else:
        return False
    
def get_comment(url, interactions, driver, login_flag):

        driver.get(url)
        time.sleep(3)

        post_id = get_post_id(url, driver)
        print('post id:', post_id)
        
        time.sleep(3)
        while url != None:
            for i in range(100):
                print('start')
                driver.get(url)
                time.sleep(3)
                if post_id == 0:
                    #####     被FB檢測到，暫停功能使用，進行帳號更換     #####
                    driver.quit()
                    time.sleep(1200)
                    driver = set_drive()
                    login_flag = login(driver, login_flag)
                    print('change account')
                    time.sleep(3)
                    driver.get(url)
                    post_id = get_post_id(url, driver)
                    continue

                elif post_id == 1:
                    #####     不屬於貼文     #####
                    return None, driver, login_flag
                
                #####     被FB檢測到，暫停功能使用，進行帳號更換(此情況屬於爬同一篇貼文爬到一半被鎖)     #####
                soup = BeautifulSoup(driver.page_source, 'lxml')
                if re.search('看來你過度使用了這項功能', soup.text) != None:
                    print('Error Page', i)
                    driver.quit()
                    time.sleep(1800)
                    driver = set_drive()
                    login_flag = login(driver, login_flag)
                    print('change account')
                    continue
                else:
                    break
            
            #####     抓取當前頁面的使用者，並顯示下一部分的留言     #####
            soup = BeautifulSoup(driver.page_source, 'lxml')
            print('start commit url: ', url)
            try:
                url = fb_url + soup.find('div', {'id' : 'see_next_' + str(post_id)}).find('a')['href']
            except:
                url = None
            print('combine commit url: ', url)
            data = soup.find_all('div', {'class' : '_2a_i'})

            #####     過濾名字與ID     #####
            for d in data:
                user_id = d.find('a')['href']
                print(user_id)
                if re.search('php\?id=', user_id) != None:
                    user_id = re.findall('id=([0-9]*)', user_id)[0]
                else:
                    user_id = re.findall('/([0-9A-Za-z./_]*)\?', user_id)[0]
                name = re.findall('(.*?), profile picture', d.find('i')['aria-label'])[0]

                interactions.append({
                        'user_ID' : user_id,
                        'author' : name,
                    })
            
            seen = set()
            result = []

        #####    重複留言者僅保留一次     #####
        for dic in interactions:
            key = (dic['user_ID'], dic['author'])
            if key in seen:
                continue

            result.append(dic)
            seen.add(key)
        
        interactions = result
        print(len(interactions))
        
        return interactions, driver, login_flag


driver = set_drive()
time.sleep(3)
wait = WebDriverWait(driver, 20)

login_flag = 1
login_flag = login(driver, login_flag)
time.sleep(3)

#####     輸入檔案格式可參考./input_example.jsonl     #####
with open('./input_example.jsonl', 'r', encoding='utf-8') as dataset:
    
    flag = 0
    for line in dataset:
        line = json.loads(line)
        interactions = []

        if 'videos' in line['url']:
            continue
        else:
            flag = 1
        url = line['url']
        rid = line['_rid']
        print('read url: ', url)
        interactions, driver, login_flag = get_comment(url ,interactions, driver, login_flag)
        if interactions == None:
            print('Continue next post')
            continue

        time.sleep(5)


        post = {
            '_rid': rid,
            'url': url,
            'interactions': interactions,
        }

        #####     輸出檔案格式可參考./output_comment.jsonl     #####
        f = open('./output_comment.jsonl', 'a', encoding='utf-8')
        json.dump(post, f, ensure_ascii=False)
        f.write('\n')
        f.close()
        print('process done: ', url)

