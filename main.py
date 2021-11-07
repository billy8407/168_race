import selenium
import time, copy
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options

def check_time():
    print('對時中...')
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(executable_path=r'geckodriver.exe', options=options)
    driver.get("https://1680380.com/view/jisusaiche/pk10kai.html")
    st = time.time()
    time.sleep(4)
    driver.find_element_by_id("pupbtn").click() 
    soup=BeautifulSoup(driver.page_source,'lxml')
    p_tag_min = soup.find("span", class_="bgtime minute")
    minute = int(p_tag_min.text)
    p_tag_second = soup.find("span", class_="bgtime second")
    second = int(p_tag_second.text)
    end = time.time()
    remain_time = minute * 60 + second - int(end - st)#01:11倒數
    if remain_time < 0:
        #print(remain_time)
        remain_time = 71 + remain_time
    driver.quit()
    return remain_time

def get_js(wait_time):
    time.sleep(wait_time)
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(executable_path=r'geckodriver.exe', options=options)
    driver.get("https://1680380.com/view/jisusaiche/pk10kai.html")
    st = time.time()
    time.sleep(4)
    driver.find_element_by_id("pupbtn").click() 
    soup=BeautifulSoup(driver.page_source,'lxml')
    ultag=soup.find('ul', {'class': 'imgnumber'})
    litag=ultag.find_all('i')
    li_list = [li_cell.text for li_cell in litag]

    p_tag_min = soup.find("span", class_="bgtime minute")
    minute = int(p_tag_min.text)
    p_tag_second = soup.find("span", class_="bgtime second")
    second = int(p_tag_second.text)
    p_tag_issue = soup.find("span", class_="preDrawIssue")
    issue = p_tag_issue.text
    end = time.time()
    #print('last',int(end - st)) #
    remain_time = minute * 60 + second - int(end - st)#01:11倒數

    if remain_time < 0:
        #print('---',remain_time) #
        remain_time = 71 + remain_time

    #print(remain_time) #
    driver.quit()
    return remain_time, li_list, issue

def post_js(driver, road_num, bit_nums_list, bat_money):
    driver.switch_to.frame(0)
    #driver.switch_to.frame("frame")
    for bit in bit_nums_list:
        name="B" + str(road_num) + "_" + bit
        #print(name) #
        try:
            driver.find_element_by_name(name).click()
            driver.find_element_by_name(name).clear()
            driver.find_element_by_name(name).send_keys(str(bat_money))
        except:
            print('發生錯誤!')
            time.sleep(1)
            return -1
    try:
        driver.find_element_by_xpath(u"(//input[@value='确定'])[2]").click()
        driver.switch_to.parent_frame()
        driver.find_element_by_xpath("//div[3]/div/button/span").click()
        print('車道',road_num,'下注數字',bit_nums_list,'成功!')
    except:
        print('發生錯誤!')
        time.sleep(1)
        return -1
    



def main():
    global lose
    lose=0
    try:
        driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
        driver.get("https://0736268923-fcs.cp168.ws/member/index#")
    except:
        print('開啟 firefox瀏覽器 發生錯誤!')
        time.sleep(1)
        return -1
    try:
        f=open('關數設定.txt','r')
    except:
        print('開啟 關數設定檔案 發生錯誤!')
        time.sleep(1)
        return -1
        
    bat_list=f.readline().split()

    if len(bat_list)<1 or len(bat_list)>15:
        print('關數設定錯誤(小於1關 或 大於15關)')
        time.sleep(1)
        return -1
    
    if False in list(map(lambda x:x.isdigit(), bat_list)):
        print('關卡倍率設定錯誤!')
        time.sleep(1)
        return -1
    
    

    try:
        search_num=input('請輸入想搜尋的數字: ')
    except:
        print('輸入錯誤')
        time.sleep(1)
        return -1
    if int(search_num) <=10 and int(search_num) >= 1:
        pass
    else:
        print('輸入錯誤')
        time.sleep(1)
        return -1

    try:
        bat_money=int(input('請輸入下注大小: '))
    except:
        print('輸入錯誤')
        time.sleep(1)
        return -1

    if bat_money >0 :
        pass
    else:
        print('輸入錯誤')
        time.sleep(1)
        return -1

    if False in list(map(lambda x:(int(x) * bat_money) < 2000, bat_list)):
        print('倍率設定過大，金額超過兩千')
        time.sleep(1)
        return -1

    try:
        bit_nums=input('請輸入想下注的數字列(例如:3 5 8): ')
        bit_nums_list=bit_nums.split()
        #print(bit_nums_list)
        for b in bit_nums_list:
            if int(b) <=10 and int(b) >= 1:
                pass
            else:
                print('輸入錯誤')
                time.sleep(1)
                return -1
    except:
        print('輸入錯誤')
        time.sleep(1)
        return -1
    try:
        login=input('網頁登入完成 並切換到 极速赛车 单号1 ~ 10 頁面後輸入 ok : ').lower()
        if login != 'ok':
            print('輸入錯誤')
            time.sleep(1)
            return -1 
    except:
        print('輸入錯誤')
        time.sleep(1)
        return -1

    remain_time = check_time()
    print('執行中...')
    get_time, li_list, issue = get_js(remain_time + 2)
    print('第 {0} 期 中獎號碼 {1}'.format(issue, li_list))

    for i in range(len(li_list)):
        if int(li_list[i]) == int(search_num):
            road_num = i + 1
            print('搜尋車道',road_num)
    copy_driver = copy.copy(driver)
    print('目前關數為第',lose+1,'關')
    if bat_list[lose]!='0': #倍率不是0下注
        post_js(copy_driver, road_num, bit_nums_list, bat_money * int(bat_list[lose])) 
    
    while 1:
        get_time, li_list, issue = get_js(get_time + 2)
        print('\n第 {0} 期 中獎號碼 {1}'.format(issue, li_list))

        if str(int(li_list[road_num - 1])) in bit_nums_list: #是否中獎
            win = True
        else:
            #print('li',li_list[road_num - 1])
            #print('bit_nums_list',bit_nums_list)
            win = False

        if win == True:
            print('恭喜中獎!, 搜尋數字',int(search_num),'的新車道')
            print('中獎關數為第',lose+1,'關')
            lose=0 
            print('關數重置為第',lose+1,'關')
            for i in range(len(li_list)): #找下一個
                if int(li_list[i]) == int(search_num):
                    road_num = i + 1
                    print('新車道為第',road_num,'車道') 
                    if bat_list[lose]!='0': #倍率不是0下注
                        post_js(copy_driver, road_num, bit_nums_list, bat_money * int(bat_list[lose]))#繼續找新車道
        else: #沒中獎
            print('尚未中獎 , 第',road_num,'車道繼續嘗試')
            lose+=1
            if lose != len(bat_list): #關卡未完成!
                print('目前關數為第',lose+1,'關')
                if bat_list[lose] != '0': #倍率不是0下注 放外面lose 會index outof range!
                    post_js(copy_driver, road_num, bit_nums_list, bat_money * int(bat_list[lose])) #同車道繼續試
            if lose == len(bat_list): #關卡已完成
                lose=0
                print('關卡已完成，放棄嘗試原車道')
                print('關數重置為第',lose+1,'關') 
                for i in range(len(li_list)): #找下一個
                    if int(li_list[i]) == int(search_num):
                        road_num = i + 1
                        print('新車道為第',road_num,'車道') 
                        if bat_list[lose]!='0': #倍率不是0下注
                            post_js(copy_driver, road_num, bit_nums_list, bat_money * int(bat_list[lose]))#繼續找新車道
            


if __name__ == '__main__':
    main()