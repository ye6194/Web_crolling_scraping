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

# 병원 이름 리스트 초기화
hospital_names = []

# 서울시 전체 구 리스트
all_gu = [
    "강남구",
    "강동구",
    "강북구",
    "강서구",
    "관악구",
    "광진구",
    "구로구",
    "금천구",
    "노원구",
    "도봉구",
    "동대문구",
    "동작구",
    "마포구",
    "서대문구",
    "서초구",
    "성동구",
    "성북구",
    "송파구",
    "양천구",
    "영등포구",
    "용산구",
    "은평구",
    "종로구",
    "중구",
    "중랑구",
]


def scraping_page():
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

    # 검색창 비우기
    search_box = driver.find_element(By.CSS_SELECTOR, "input.input_search")
    search_box.clear()
    time.sleep(2)  # clear 이후 잠시 대기

    # 검색창이 비워졌는지 확인
    while search_box.get_attribute("value") != "":
        search_box.clear()
        time.sleep(1)

    return hospital_names


for gu in all_gu:
    search_box = driver.find_element(By.CSS_SELECTOR, "input.input_search")
    search_box.send_keys(f"{gu} 라식 안과")
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)
    hospital_names = scraping_page()
    print(hospital_names)
    print(f"{gu} 리스트: {len(hospital_names)}")
    print()


# 검색창에 '강남구 라식 안과' 입력 후 검색
# search_box = driver.find_element(By.CSS_SELECTOR, "input.input_search")
# search_box.send_keys("강남구 라식 안과")
# search_box.send_keys(Keys.RETURN)
# time.sleep(3)
# hospital_names = scraping_page()
# print(hospital_names)
# print(f"강남구 리스트: {len(hospital_names)}")
# print()


# 고유한 병원 이름 리스트 생성
unique_hospitals = set(hospital_names)
print(unique_hospitals)
print(f"집합: {len(unique_hospitals)}")
print("")

# 각 병원을 검색하고 URL 추출
search_box.clear()
for hospital in unique_hospitals:
    search_box = driver.find_element(By.CSS_SELECTOR, "input.input_search")
    search_box.clear()  # 검색창 비우기
    time.sleep(2)  # clear 이후 잠시 대기

    # 검색창이 비워졌는지 확인
    while search_box.get_attribute("value") != "":
        search_box.clear()
        time.sleep(1)

    search_box.send_keys(hospital)
    search_box.send_keys(Keys.RETURN)
    time.sleep(1)  # 페이지 로드 대기

# 총 안과 수와 각 병원의 URL 출력
# for url in urls:
# print(url)

# 드라이버 종료
driver.quit()
