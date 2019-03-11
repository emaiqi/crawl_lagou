from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import random

browser = webdriver.Firefox()
wait = WebDriverWait(browser, 10)
pages = 30


def main():
    try:
        url = "https://passport.lagou.com/login/login.html"
        browser.get(url)
        login_button = browser.find_element_by_css_selector("ul.form_head.clearfix > li:nth-child(2)")
        login_button.click()
        info = input("先别输入，先去浏览器登陆完毕再随便输入继续运行：")
        job_info = []
        url = "https://www.lagou.com/jobs/list_python?labelWords=sug&fromSearch=true&suginput=python"
        browser.get(url)
        for i in range(pages):
            lis = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                                  "ul.item_con_list li.con_list_item.default_list")))

            lis2 = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                                   "div.p_bot > div.li_b_l")))
            lis3 = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                                   "div.list_item_bot > div.li_b_r")))
            for li, li2, li3 in zip(lis, lis2, lis3):
                item = {}
                item["company"] = li.get_attribute("data-company")
                item["job"] = li.get_attribute("data-positionname")
                item["salary"] = li.get_attribute("data-salary")
                info = li2.text
                info = info.split(" ")
                item["experience"] = info[1]
                item["education"] = info[3]
                item["welfare"] = li3.text
                job_info.append(item)
            next_page = browser.find_element_by_css_selector(
                "div.item_con_pager > div.pager_container > span.pager_next")
            next_page.click()
            time.sleep(random.randrange(3, 6))
        with open("job_info.json", "w", encoding="utf8")as f:
            json.dump(job_info, f, ensure_ascii=False, indent="\t")
        browser.close()
    except Exception as e:
        print(repr(e))


if __name__ == '__main__':
    main()
