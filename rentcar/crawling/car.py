from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import time
import csv
import re
import os

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
driver = webdriver.Chrome(options=chrome_options)

#######################################
base_path = os.getcwd()
car_2n3d = open(base_path + '/data/car_data/crawling/car_2n3d.csv', 'w', newline="")
writer_2n3d = csv.writer(car_2n3d)

car_3n4d = open(base_path + '/data/car_data/crawling/car_3n4d.csv', 'w', newline="")
writer_3n4d = csv.writer(car_3n4d)

car_4n5d = open(base_path + '/data/car_data/crawling/car_4n5d.csv', 'w', newline="")
writer_4n5d = csv.writer(car_4n5d) 

driver.get("https://www.lotterentacar.net/hp/kor/reservation/index.do?areaFlag=6#")
time.sleep(5)

# 화면 최대화
driver.maximize_window()

# 로그인 하지 않고 예약 클릭
driver.find_element(By.XPATH, '//*[@id="is-login-popup"]/div/a[1]').click()

# 다음 버튼 클릭
next_buttons = driver.find_elements(By.XPATH, '//button[text() = "다음"]')
next_buttons[0].click()
time.sleep(2)
next_buttons[1].click()
time.sleep(2)

# 7월로 넘어가는 버튼
# driver.find_element(By.XPATH, '//*[@id="calNextBtn"]').click()

for i in range(1, 29):
    # 대여기간 및 시간 선택
   
    for j in range(2, 5):
        if (i+j) > 30:
            continue
        start_date = driver.find_elements(By.XPATH, f'//button[text()="{str(i)}"]')
        start_date[1].click()
        time.sleep(2)

        end_date = driver.find_elements(By.XPATH, f'//button[text()="{str(i+j)}"]')
        end_date[1].click()
        time.sleep(2)

        # 날짜 정보
        start = driver.find_element(By.XPATH, '//*[@id="content-date"]/div[2]/div[1]/div[1]/span[2]').text
        start = re.sub('2023. |\. |\.', '' , start)
        end = driver.find_element(By.XPATH, '//*[@id="content-date"]/div[2]/div[2]/div[1]/span[2]').text
        end = re.sub('2023. |\. |\.', '' , end)

        if len(start) == 2:
            start = start[0] + '0' + start[-1]
        if len(end) == 2:
            end = end[0] + '0' + end[-1]

        # 요일정보
        day_lst = ['수', '목', '금', '토', '일', '월', '화']
        start_day = day_lst[int(start[1:]) % 7]
        end_day = day_lst[int(end[1:]) % 7]

        ## 나중에 추가할 정보
        date = [start, start_day, end, end_day]
        # 시간 선택
        hours = driver.find_elements(By.XPATH, '//option[text()="12시"]')
        hours[0].click()
        time.sleep(2)
        hours[1].click()
        time.sleep(2)

        # 다음버튼 클릭
        driver.find_element(By.XPATH, '//*[@id="tab-3"]/button').click()
        time.sleep(5)

        # 차 정보 받아오기
        cars = driver.find_elements(By.CLASS_NAME, "vehicle-element")
        for car in cars:
            car_info = car.text
            reservation = None
            
            car_img = car.find_element(By.TAG_NAME, "img")
            img_url = car_img.get_attribute('src')

            if '회원가' in car_info:
                car_info = re.sub('\n회원가', '', car_info)
                
            if '예약이 마감 되었습니다.' in car_info:
                car_info = re.sub('\n예약이 마감 되었습니다.', '', car_info)
                reservation = 0
            else:
                reservation = 1
            
            # (...) 제거
            car_info = re.sub(r'\([^()]*\)', '' , car_info)

            # |를 \n으로 대체
            car_info = re.sub('\s\|\s', '\n', car_info)

            # 1종보통, 110km/h제한 제거
            if '1종 보통' in car_info:
                car_info = re.sub('\n1종 보통\n.*$', '', car_info)                

            car_data = car_info.split('\n')
            car_data.extend(date)
            car_data.append(reservation)
            car_data.append(f'{j}박 {j+1}일')
            car_data.append(img_url)

            if j == 2:
                writer_2n3d.writerow(car_data)
            elif j == 3:
                writer_3n4d.writerow(car_data)
            else:
                writer_4n5d.writerow(car_data)

        # 다음 일정으로 변경
        change = driver.find_elements(By.XPATH, '//button[text()="변경"]')
        change[2].click()

        # 경고 팝업창 클릭
        time.sleep(3)
        Alert(driver).accept()

driver.close()


