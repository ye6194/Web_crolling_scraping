from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time

# 웹드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 네이버 지도 페이지로 이동
# url = "https://map.naver.com/v5/search"
url = "https://map.naver.com"
driver.get(url)
time.sleep(2)

# 검색창에 '서울특별시 라식 안과' 입력 후 검색
search_box = driver.find_element(By.CSS_SELECTOR, "input.input_search")
search_box.send_keys("서울특별시 라식 안과")
search_box.send_keys(Keys.RETURN)
time.sleep(3)

# 병원 이름 리스트, url 리스트 초기화
hospital_names = []
urls = []

while True:
    # 스크롤을 내려서 모든 검색 결과 로드
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # BeautifulSoup를 사용하여 페이지 소스 파싱
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    # 검색 결과에서 안과 병원 이름 추출
    results = soup.find_all("strong")
    hospital_names.extend(
        [result.get_text() for result in results if "안과" in result.get_text()]
    )

    # 다음 페이지 버튼 클릭
    try:
        next_button = driver.find_element(
            By.CSS_SELECTOR, "a.eUTV2[aria-disabled='false']"
        )
        next_button.click()
        time.sleep(5)
    except:
        break

# 고유한 병원 이름 리스트 생성
# unique_hospitals = set(hospital_names)
# print(unique_hospitals)
print(f"서울의 총 안과 수: {len(hospital_names)}")
print("")

# 각 병원을 검색하고 URL 추출
search_box.clear()
for hospital in hospital_names:
    search_box = driver.find_element(By.CSS_SELECTOR, "input.input_search")
    search_box.clear()  # 검색창 비우기
    time.sleep(5)  # clear 이후 잠시 대기

    # 검색창이 비워졌는지 확인
    while search_box.get_attribute("value") != "":
        search_box.clear()
        time.sleep(1)

    search_box.send_keys(hospital)
    search_box.send_keys(Keys.RETURN)
    time.sleep(1)  # 페이지 로드 대기
    urls.append(driver.current_url)

# 총 안과 수와 각 병원의 URL 출력
# for url in urls:
# print(url)

# 드라이버 종료
driver.quit()
