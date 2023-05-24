from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
import re

# csv writer 설정
hotel_2n3d = open("C:/Users/jiyeon/Desktop/project1/hotel/3_name_23.csv", 'w', newline="")
writer_2n3d = csv.writer(hotel_2n3d)
price_2n3d = open("C:/Users/jiyeon/Desktop/project1/hotel/3_price_23.csv", 'w', newline="")
writer_2n3d_2 = csv.writer(price_2n3d)

hotel_3n4d = open("C:/Users/jiyeon/Desktop/project1/hotel/3_name_34.csv", 'w', newline="")
writer_3n4d = csv.writer(hotel_3n4d)
price_3n4d = open("C:/Users/jiyeon/Desktop/project1/hotel/3_price_34.csv", 'w', newline="")
writer_3n4d_2 = csv.writer(price_3n4d)

hotel_4n5d = open("C:/Users/jiyeon/Desktop/project1/hotel/3_name_45.csv", 'w', newline="")
writer_4n5d = csv.writer(hotel_4n5d)
price_4n5d = open("C:/Users/jiyeon/Desktop/project1/hotel/3_price_45.csv", 'w', newline="")
writer_4n5d_2 = csv.writer(price_4n5d)

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메세지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 브라우저 생성
#browser = webdriver.Chrome("chromedriver.exe")
service = Service("C:/Users/jiyeon/Desktop/project1/hotel/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# 크롬 드라이버 자동 업데이트
#from webdriver_manager.chrome import ChromeDriverManager
#service = Service(executable_path=ChromeDriverManager().install())
#driver = webdriver.Chrome(service=service, options=chrome_options)

# 웹페이지 해당 주소 이동
driver.get("https://hotels.naver.com/list?placeFileName=place%3AJeju_Province&adultCnt=3&checkIn=2023-06-01&checkOut=2023-06-02&includeTax=false&sortField=popularityKR&sortDirection=descending")
time.sleep(10)

# 화면 최대화
#driver.maximize_window()

for i in range(1, 30):
    for j in range(2,5):
        if (i+j) > 30:
            continue
        
        #체크인 날짜 설정
        calender = driver.find_element(By.CSS_SELECTOR, "#__next > div > div > div > div.Contents_ListComponent__39yRH > div.Contents_options__nmI6s > div > div.SearchBox_SearchBox__zYN5i > div > div > div > div.SearchBox_select_checkinout__D_EtG._calendar > button.SearchBox_btn_checkin__Pre_6")
        calender.click()
        time.sleep(3)

        dayin = str(i)
        checkin_date = driver.find_elements(By.XPATH, f'//b[text() = {dayin}]')
        checkin_date[1].click()

        #체크아웃 날짜 설정
        dayout = str(i+j)
        checkout_date = driver.find_elements(By.XPATH, f'//b[text() = {dayout}]')
        checkout_date[1].click()


        #적용 버튼 클릭(검색)
        search = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[4]/button')
        search.click()
        time.sleep(10)

        #날짜 저장
        date_in = driver.find_element(By.CSS_SELECTOR, '#__next > div > div.list_ListPage__dipO7.hotel_list > div > div.Contents_ListComponent__39yRH > div.Contents_options__nmI6s > div > div.SearchBox_SearchBox__zYN5i > div > div > div > div.SearchBox_select_checkinout__D_EtG._calendar > button.SearchBox_btn_checkin__Pre_6').text
        date_out = driver.find_element(By.CSS_SELECTOR, '#__next > div > div.list_ListPage__dipO7.hotel_list > div > div.Contents_ListComponent__39yRH > div.Contents_options__nmI6s > div > div.SearchBox_SearchBox__zYN5i > div > div > div > div.SearchBox_select_checkinout__D_EtG._calendar > button.SearchBox_btn_checkout__Ryvyu').text
        date_in = [date_in[:-2], date_in[-1]]
        date_out = [date_out[:-2], date_out[-1]]

        #1~5페이지 이동
        page = 1
        while page < 6:
            #맨 아래까지 무한 스크롤
            #스크롤 전 높이
            before_h = driver.execute_script("return window.scrollY")

            while True:
                # 맨 아래로 스크롤 내리기
                driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)

                # 스크롤 사이 페이지 로딩 시간
                time.sleep(3)

                # 스크롤 후 높이
                after_h = driver.execute_script("return window.scrollY")

                if after_h == before_h:
                    break
                before_h = after_h        
        
            #정보 저장
            hotels = driver.find_elements(By.XPATH, '//div[@class="Detail_InfoArea__uZ4qT"]')
            for hotel in hotels:
                hotel_data = hotel.text
                hotel_data = re.sub('제주특별자치도관광협회 심사', '', hotel_data)
                hotel_data = hotel_data.split('\n')
                if j == 2:
                    writer_2n3d.writerow(hotel_data)
                elif j == 3:
                    writer_3n4d.writerow(hotel_data)
                else:
                    writer_4n5d.writerow(hotel_data)
    
            prices = driver.find_elements(By.XPATH,'//em[@class="Price_show_price__iQpms"]')
            for price in prices:
                price_data = price.text
                price_data = price_data.split('\n')
                price_data.extend(date_in)
                price_data.extend(date_out)
                if j == 2:
                    writer_2n3d_2.writerow(price_data)
                elif j == 3:
                    writer_3n4d_2.writerow(price_data)
                else:
                    writer_4n5d_2.writerow(price_data)
        
            nextpage = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/div[1]/div[3]/div[2]/button[7]')
            nextpage.click()
            time.sleep(10)

            page += 1


        #맨 위로 이동
        up_botton = driver.find_element(By.XPATH, '//*[@id="__next"]/div/footer/div[1]/button[2]')
        up_botton.click()

driver.quit()
writer_2n3d.close()
writer_2n3d_2.close()
writer_3n4d.close()
writer_3n4d_2.close()
writer_4n5d.close()
writer_4n5d_2.close()