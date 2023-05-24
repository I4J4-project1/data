from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import time
import csv
import re

################################################
### 셀리니움 관련 초기 설정

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메세지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 브라우저 생성
browser=webdriver.Chrome("User/jjjk84/Documents/chromedriver")

# 크롬 드라이버 자동 업데이트
# from webdriver_manager.chrome import ChromeDriverManager
# service = Service(executable_path=ChromeDriverManager().install())


################################################
### 활용 함수 
  

## 크롤링 함수
def crawl(csv_path, depart_ap, desti_ap):
    # csv writer 설정
    f = open(f"/Users/hj/Documents/t1project/{csv_path}", 'w', newline="")
    writer = csv.writer(f)
    driver = webdriver.Chrome(options=chrome_options)

    # 웹페이지 해당 주소 이동
    driver.get(f"https://flight.naver.com/flights/domestic/{depart_ap}-{desti_ap}-20230601/?adult=2&fareType=YC")
    time.sleep(10)
    
    # 화면 최대화
    driver.maximize_window()
    
    
    for i in range(1, 31):

        if i != 1:
            # 출발 날짜 설정
            calender = driver.find_element(By.CSS_SELECTOR, '#__next > div > div.container > div.domestic_top__2ONl7 > div > div.layout_large__2AaMz > div > div > div.searchBox_tabpanel__1BSGR > div:nth-child(2) > button')
            calender.click()
            time.sleep(3)

            day = str(i) 
            days = driver.find_elements(By.XPATH, f'//b[text() = {day}]')
            days[1].click()

            # 검색 버튼 클릭
            search = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[3]/div/div[1]/div/div/button/span')
            search.click()
            time.sleep(10)

        date = driver.find_element(By.CSS_SELECTOR, '#__next > div > div.container > div.domestic_top__2ONl7 > div > div.layout_large__2AaMz > div > div > div.searchBox_tabpanel__1BSGR > div:nth-child(2) > button').text
        date = [date[:-2], date[-1]]

        # 무한 스크롤 
        # 스크롤 전 높이
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


        # 정보 csv 저장
        flights = driver.find_elements(By.XPATH, '//div[@class="domestic_Flight__sK0eA result"]')
        
        for flight in flights:
            flight_data = flight.text
            
            flight_data = re.sub('편도', '', flight_data)
            flight_data = re.sub(' ', '', flight_data)

            # 1%적립이벤트혜택, 네이버페이 결제시 1% 적립 불필요한 말 삭제
            if '1%적립이벤트혜택' in flight_data:
                flight_data = re.sub('1%적립이벤트혜택\n', '', flight_data)
            
            if '네이버페이' in flight_data:
                flight_data = re.sub(r'\n네이버페이결제시1%적립\n.*$', '', flight_data)

            flight_data = re.sub(r'(석)(\d+,\d+원)', r'\1\n\2', flight_data)
            
            flight_data = flight_data.split('\n')
            flight_data.extend(date)

            writer.writerow(flight_data)
            

        # 맨 위로 이동
        up_botton = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/footer/div[1]/button[2]')
        up_botton.click()
    
    driver.quit()
    f.close()

###################################################
### 김포에서 제주까지 비행기편 웹크롤링

## 입력 변수 : csv 파일 경로, 출발 공항, 도착지 공항
crawl('flight_gimpo_to_jeju.csv', 'GMP', 'CJU')

    
###################################################
### 김포에서 제주까지 비행기편 웹크롤링

crawl('flight_jeju_to_gimpo.csv', 'CJU', 'GMP')