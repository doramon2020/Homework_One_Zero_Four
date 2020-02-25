#!/usr/bin/env python
# coding: utf-8

# In[2]:

import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options #不用視窗開啟
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from lxml import html
import time                              
"""chrome_options = Options()               #不用
option.add_argument("headless")          #視窗
chrome_options.add_argument('--headless') # 開啟
chrome_options.add_argument('--disable-gpu') #唷"""

browser = webdriver.Chrome(executable_path='/Users/James/python課堂練習/Python爬蟲/chromedriver')

browser.get("http://104.com.tw/") #用selenium開啟104網頁
browser.implicitly_wait(10) #避免固定等待時間

#用SelectorGadget套件找到搜尋欄位css屬性 
keyword = browser.find_element_by_css_selector("#ikeyword") 

keyword.send_keys("數據") #########輸入搜尋 此欄位應設定變數
keyword.send_keys(Keys.ENTER) #送出輸入的關鍵字
browser.implicitly_wait(10)
soup = bs(browser.page_source,'lxml')   ##用bs解析browser.page_source編碼
getpages = int(soup.select(".page-select option")[0].text[6:-2])
urlpage = browser.current_url
browser.quit()
##抓取總共頁數
                                        #將頁數變為int屬性 , 指派給變數getpages跑迴圈

# In[ ]:


#抓取資料
soups = soup.select('article')

for getpage in range(getpages+1)[1:]:
    browser = webdriver.Chrome(executable_path='/Users/James/python課堂練習/Python爬蟲/chromedriver') #啟動瀏覽器必定要加
    browser.get(urlpage)
    selectSite = Select(browser.find_element_by_css_selector(".page-select"))
    selectSite.select_by_value(str(getpage))
    time.sleep(10)
    soup = bs(browser.page_source,'lxml')
    soups = soup.select('article')
    browser.quit()
    for i in soups:
            if 'b-block--ad' in i.get('class'):
                continue #跳過有廣告標籤的公司
            if 'b-block--top-bord' in i.get('class'):
                url = "http:"+i.find("a").get("href") #職缺名稱網址
                browser = webdriver.Chrome(executable_path='/Users/James/python課堂練習/Python爬蟲/chromedriver')
                browser.get(url) #
                browser.implicitly_wait(10) #避免固定等待時間
                soup2 = bs(browser.page_source,'lxml')
                soup2.select('.job-description__content')[0].text.strip().replace('\n','').replace('\r','').replace('\t','')
            if 'b-block--top-bord' not in i.get('class'):
                break
#soup2.select('.job-description__content')[0].text.strip().replace('\n','').replace('\r','').replace('\t','') #工作內容
#           soup2.select('u')[0].text.strip() #職務類別
#           soup2.select('.monthly-salary')[0].text.strip() #工作待遇
#soup.find_all("p", class_="t3 mb-0")  #好像不能用會出錯,有些網頁沒此項
#總共可找到10筆資料,依序為
#0. 全職
#1. 地址
#2. 不需負擔管理責任
#3. 無需出差外派
#4. 日班
#5. 休假制度
#6. 可上班日
#7. 需求人數
#8. 工作經歷
#9. 學歷要求            
#########待解決問題: 1. 加入抓取公司網址 抓取人數規模等資訊,其他資訊欄位還需補齊
#          2. 判斷重複資料
#          3. 資料儲存方式
#          4. 連接mysql語法攥寫
#          5. 資料如何導入資料庫


# In[ ]:




