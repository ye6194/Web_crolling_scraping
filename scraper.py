from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from config import all_gu


# 검색 결과 페이지 스크래핑
def scraping_page(driver, hospital_names):
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

    search_box = driver.find_element(By.CSS_SELECTOR, "input.input_search")
    search_box.clear()


# 각 구별로 안과 검색 후 스크래핑 결과를 리스트에 저장
def search_gu(driver, hospital_names):
    for gu in all_gu:
        search_box = driver.find_element(By.CSS_SELECTOR, "input.input_search")
        # search_box.clear() 대신 컨트롤+a한 후 delete
        search_box.send_keys(Keys.CONTROL + "a")
        search_box.send_keys(Keys.DELETE)
        time.sleep(1)

        search_box.send_keys(f"{gu} 라식 안과")
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        scraping_page(driver, hospital_names)
        print(hospital_names)
        print(f"{gu}까지 리스트: {len(hospital_names)}")
        print()

    return hospital_names


# 리스트의 병원을 검색하고 스크래핑
def search_hospital_detail(driver, unique_hospitals):
    valid_hospitals = []  # 검색 시 검색 결과가 하나만 나오는 병원들

    for hospital in unique_hospitals:
        search_box = driver.find_element(By.CSS_SELECTOR, "input.input_search")
        search_box.send_keys(Keys.CONTROL + "a")
        search_box.send_keys(Keys.DELETE)
        time.sleep(1)

        search_box.send_keys(hospital)
        search_box.send_keys(Keys.RETURN)
        time.sleep(1)

        try:
            # '홈' span 태그가 나타날 때까지 최대 5초 대기
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.veBoZ"))
            )
            home_span = driver.find_element(By.CSS_SELECTOR, "span.veBoZ")
            if home_span:
                print("찾음")
                valid_hospitals.append(hospital)
        except:
            pass

        """
        # BeautifulSoup를 사용하여 페이지 소스 파싱
        page_source = driver.page_source
        print()
        # print(page_source)
        print()
        soup = BeautifulSoup(page_source, "html.parser")

        # '홈' span 태그를 찾기
        home_span = soup.find("span", class_="navbar_text")
        
        if home_span:
            valid_hospitals.append(hospital)
            print(valid_hospitals)
        """
