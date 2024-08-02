from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


def scraping_visitor_review(driver, hospital_info, reviews):
    # 더보기 버튼을 계속 눌러서 모든 방문자 리뷰 로드
    while True:
        try:
            load_more_button = WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.fvwqf[role='button']"))
            )
            driver.execute_script("arguments[0].click();", load_more_button)
            time.sleep(2)  # 클릭 후 로딩 시간
        except Exception as e:
            break  # 더 이상 로드할 리뷰가 없으면 break

    # 긴 방문자 리뷰의 더보기 버튼 클릭
    more_buttons = driver.find_elements(By.CSS_SELECTOR, "a.xHaT3[role='button']")
    for button in more_buttons:
        try:
            driver.execute_script("arguments[0].click();", button)
            time.sleep(1)  # 클릭 후 로딩 시간
        except Exception as e:
            print(f"긴 리뷰 더보기 버튼 클릭 중 에러 발생: {e}")

    # 모든 방문자 리뷰 스크래핑
    review_elements = driver.find_elements(By.CSS_SELECTOR, "span.zPfVt")
    for review in review_elements:
        reviews.append(review.text)

    hospital_info["visitor_review"] = reviews
    hospital_info["visitor_review_cnt"] = len(reviews)
