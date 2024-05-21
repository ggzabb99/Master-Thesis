import json
from selenium.webdriver.common.by import By
from datetime import datetime
import undetected_chromedriver as uc
from undetected_chromedriver import ChromeOptions
from bs4 import BeautifulSoup
import time
from random import randint
import re

fb_url = "https://www.facebook.com/"

like_class_name = {
    'open' : '_45m8',
    'close' : 'x1i10hfl x6umtig x1b1mbwd xaqea5y xav7gou x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x87ps6o x1lku1pv x1a2a7pz x6s0dn4 x14yjl9h xudhj91 x18nykt9 xww2gxu x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xl56j7k xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xc9qbxq x14qfxbe x1qhmfi1',
    'window' : 'x1qjc9v5 x78zum5 xdt5ytf x1n2onr6 x1al4vs7 x1jx94hy x1qpq9i9 xdney7k xu5ydu1 xt3gfkd x104qc98 x1gj8qfm x1iyjqo2 x6ikm8r x10wlt62 x1likypf x7b354b x1e9k66k x12l8kdc',
    'users' : 'x78zum5 xdt5ytf xz62fqu x16ldp7u',
    'name' : 'x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f',
    'scroll': 'x14nfmen x1s85apg xds687c x5yr21d xg01cxk x10l6tqk x13vifvy x1wsgiic x19991ni xwji4o3 x1kky2od x1sd63oq',
}

def login(driver, login_flag):
    #####     請填寫FB帳號密碼供爬蟲使用，因可能被暫時停止功能，請填寫以供輪流使用     #####
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
        login_flag = 3
    elif login_flag == 3:
        email = ''
        password = ''
        login_flag = 0



    print('Email: ', email)

    context = driver.find_element("name", 'email')
    context.send_keys(email)
    context = driver.find_element("name", 'pass')
    context.send_keys(password)
    commit = driver.find_element("name", 'login')
    commit.click()
    time.sleep(5)
    return login_flag

def set_drive():
    options = ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-notifications")

# 設定 WebDriver
    driver = uc.Chrome(options=options)

    url = "https://www.facebook.com/"
    driver.get(url)
    time.sleep(3)
    return driver

def check_ban(driver):
    #####     檢測是否被 FB 暫停功能     #####
    print('check ban')
    url = 'https://www.facebook.com/chingte/posts/5119906628026315'
    driver.get(url)
    time.sleep(randint(4, 10))

    try:
        like_button = driver.find_element(By.XPATH, "//div[@class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1n2onr6 x87ps6o x1lku1pv x1a2a7pz x1heor9g xnl1qt8 x6ikm8r x10wlt62 x1vjfegm x1lliihq']")
    except:
        soup = BeautifulSoup(driver.page_source, 'lxml')
                
        if re.search('你暫時遭到封鎖', soup.text) != None:
            print('-----Account ban-----')
            time.sleep(1200)
            return 1
        else:
            print('No like button')
            return 0
    
    like_button.click()
    time.sleep(randint(4, 10))

    old = 0
    like_button_cnt = 0

    for i in range(3):
            #try:
            ban_popup_div = driver.find_element(By.XPATH, f"(//div[@data-visualcompletion='ignore-dynamic' and not (@role) and not (@class)])[last()]")
            driver.execute_script("arguments[0].scrollIntoView(true);", ban_popup_div)
            print('popup_div: ', ban_popup_div)

            if ban_popup_div == old:
                like_button_cnt += 1
            
            if like_button_cnt ==2:
                print('Account ban')
                return 1
            
            old = ban_popup_div
            time.sleep(5)

    return 2
    

def get_like(url, interactions, login_flag, driver):

    print('in like :', len(interactions))  


    for i in range(10):
        print(datetime.now())
        old = 0
        like_button_cnt = 0
        soup = None
        scroll_down_flag = 0
        driver.get(url)
        time.sleep(randint(4, 10))

        #####    打開按讚清單     #####
        try:
            like_button = driver.find_element(By.XPATH, "//div[@class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1n2onr6 x87ps6o x1lku1pv x1a2a7pz x1heor9g xnl1qt8 x6ikm8r x10wlt62 x1vjfegm x1lliihq']")
        except:
            print('No like button')
            return 0, driver, login_flag
        like_button.click()
        time.sleep(randint(4, 10))
        
        #####    開始抓按讚使用者     #####
        for i in range(100):
            try:
                popup_div = driver.find_element(By.XPATH, f"(//div[@data-visualcompletion='ignore-dynamic' and not (@role) and not (@class)])[last()]")
                driver.execute_script("arguments[0].scrollIntoView(true);", popup_div)
                print('popup_div: ', popup_div)
                time.sleep(2)

                if popup_div == old:
                    #####    檢測是否有成功滾動按讚清單     #####
                    like_button_cnt += 1
                
                if like_button_cnt == 5:
                    #####    連續失敗五次，檢查是已到清單底部或被暫停功能     #####
                    soup = BeautifulSoup(driver.page_source, 'lxml')
                    ban_flag = check_ban(driver)
                    print('ban_flag: ', ban_flag)
                    if ban_flag == 0:
                        print('No like button')
                        return 0, driver, login_flag
                    elif ban_flag == 1:
                        driver.quit()
                        time.sleep(1800)
                        driver = set_drive()
                        login_flag = login(driver, login_flag)
                        break
                    elif ban_flag == 2:
                        like_button_cnt = 0
                        scroll_down_flag = 1
                        break
                
                old = popup_div
                time.sleep(5)
            except:
                print('like scrolling error')
                break

        if like_button_cnt == 5:
            continue
        
        if scroll_down_flag == 0:
            #####    成功爬完     #####
            soup = BeautifulSoup(driver.page_source, 'lxml')


        data = soup.find_all('span', {'class' : 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h'})

        for d in data:
            name = d.find('a').text
            link = d.find('a')['href']

            interactions.append({
                'user_ID' : link,
                'author' : name,
                
            })

        #####     過濾名字與ID     #####
        for d in interactions:
            if re.search('id=', d['user_ID']) != None:
                try:
                    d['user_ID'] = re.findall('id=([0-9]*)', d['user_ID'])[0]
                except:
                    print('ID: ' ,d['user_ID'])
                    continue
            else:
                try:
                    d['user_ID'] = re.findall('com/([0-9A-Za-z./_]*)\?', d['user_ID'])[0]
                except:
                    print('No ID: ' ,d['user_ID'])
                    continue
        
        seen = set()
        result = []

        #####    重複者僅保留一次     #####
        for dic in interactions:
            key = (dic['user_ID'], dic['author'])
            if key in seen:
                continue

            result.append(dic)
            seen.add(key)
        
        interactions = result
        
        print('last like :', len(interactions))
        break
    return interactions, driver, login_flag


options = ChromeOptions()
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("--disable-web-security")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--disable-notifications")

# 設定 WebDriver
driver = set_drive()

time.sleep(3)


login_flag = 5
login_flag = login(driver, login_flag)
time.sleep(3)

#####     檔案格式可以參考input_example.jsonl     #####
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
        print('read url: ', url)
        time.sleep(5)
        interactions, driver, login_flag = get_like(url, interactions, login_flag, driver)

        if interactions == 0:
            print('next post')
            continue

        post = {
            '_rid': line['_rid'],
            'url': url,
            'interactions': interactions,
        }

        #####     輸出檔案格式可參考./output_like.jsonl     #####
        f = open('./output_like.jsonl', 'a', encoding='utf-8')
        json.dump(post, f, ensure_ascii=False)
        f.write('\n')
        f.close()
        print('process done: ', url)
