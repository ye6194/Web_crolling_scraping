from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


def scraping_blog_review(driver, info, blog_urls):
    # 블로그 리뷰탭으로 이동
    blog_review_tab = driver.find_element(By.XPATH, '//*[@id="_subtab_view"]/div/a[2]')
    blog_review_tab.click()
    time.sleep(2)  # 탭 이동 후 잠시 기다림

    # 더보기 버튼 눌러서 모든 블로그 리뷰 보기
    while True:
        try:
            load_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.fvwqf[role='button']"))
            )
            driver.execute_script("arguments[0].click();", load_more_button)
            time.sleep(1)  # 클릭 후 로딩 시간
        except Exception as e:
            break  # 더 이상 로드할 리뷰가 없으면 break

    # 모든 블로그 url 스크래핑
    urls = driver.find_elements(By.CSS_SELECTOR, "a.RHxFw")
    for url in urls:
        blog_urls.append(url.get_attribute("href"))

    info["blog_urls"] = blog_urls
    info["blog_urls_cnt"] = len(blog_urls)
