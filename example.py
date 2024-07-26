from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

# 웹드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 네이버 지도 특정 식당 리뷰 페이지로 이동
# url = "https://map.naver.com/p/entry/place/31237863?c=16.92,0,0,0,dh&placePath=/review" 왜그런지 모르겠는데 pc버전 말고 밑에 모바일 버전으로 수정하니까 됐음
url = "https://m.place.naver.com/restaurant/31237863/review"
driver.get(url)

# 페이지 로드 대기
time.sleep(7)

# "내용 더보기" 버튼 모두 클릭
while True:
    try:
        more_buttons = driver.find_elements(By.CSS_SELECTOR, "span.rvCSr")
        if not more_buttons:
            break
        for button in more_buttons:
            button.click()
            time.sleep(1)  # 클릭 후 잠시 대기
    except Exception as e:
        print(f"Exception occurred while clicking '내용 더보기' button: {e}")
        break

# BeautifulSoup를 사용하여 페이지 소스 파싱
page_source = driver.page_source
# print(page_source)  # 페이지 소스를 출력하여 올바른 클래스 이름을 찾음
soup = BeautifulSoup(page_source, "html.parser")

# 리뷰 내용 스크래핑
# reviews = soup.find_all("span", class_="zPfVt")
# reviews = soup.select("span")
reviews = soup.find_all("span", class_="zPfVt")
# print(reviews)
for review in reviews:
    print(f"리뷰: {review.get_text()}")

# 드라이버 종료
driver.quit()
