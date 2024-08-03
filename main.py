from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from config import url, all_gu
from scraper import search_gu, search_hospital

# 웹드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 네이버 지도 페이지로 이동
driver.get(url)
time.sleep(2)

# 병원 이름 리스트 초기화
hospital_names = []

# 각 병원을 검색하고 URL 추출
hospital_names = search_gu(driver, hospital_names)
unique_hospitals = set(hospital_names)
print(
    f"서울 모든 안과 리스트(중복 제거): {unique_hospitals} ({len(unique_hospitals)}개)"
)

# 서울의 안과 중 검색 결과가 하나인 병원을 찾아 그 병원의 정보를 스크래핑
hospital_info = search_hospital(driver, unique_hospitals)
print("병원 정보:", hospital_info)

# 드라이버 종료
driver.quit()

"""
병원 정보: {
    '병원이름1': {
        'name': string,
        'thumbnail': string,
        'location': string,
        'hp': string,
        'rating': number,
        'visitor_review': string,
        'visitor_review_cnt': number,
        'blog_urls': string,
        'blog_urls_cnt': number,
    },
    '병원이름2': { 
        ...
    },
}
"""
