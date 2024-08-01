from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


def scraping_blog_review(driver, hospital_info, blog_urls):
    # 블로그 리뷰 페이지로 이동
    review_tab_button = driver.find_element(
        By.CSS_SELECTOR, "a[role='tab'].tpj9w._tab-menu"
    )
    driver.execute_script("arguments[0].click();", review_tab_button)
    time.sleep(2)  # 페이지 로딩을 기다리는 시간

    # 더보기 버튼 눌러서 모든 블로그 리뷰 보기
    while True:
        try:
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.fvwqf[role='button']"))
            )
            driver.execute_script("arguments[0].click();", load_more_button)
            time.sleep(2)  # 클릭 후 로딩 시간
        except Exception as e:
            # 더 이상 로드할 리뷰가 없으면 break
            break

    # 모든 블로그 url 스크래핑
    urls = driver.find_elements(By.CSS_SELECTOR, "a.uUMhQ")
    for url in urls:
        blog_urls.append(url.get_attribute("href"))

    hospital_info["blog_urls"] = blog_urls
    hospital_info["blog_urls_cnt"] = len(blog_urls)
