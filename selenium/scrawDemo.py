from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



browser = webdriver.Chrome("C:/Code/Tools/chromedriver.exe")
browser.get('https://sbswebapp.azurewebsites.net/TasksV2?filterId=124950')

element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'passwd')))
element = browser.find_element_by_name("login")
element.clear()
element.send_keys("hengyliu@microsoft.com")
element = browser.find_element_by_name("passwd")
element.clear()
element.send_keys("lhy_71171111111")



element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginMessage"]/a')))

#browser.find_element_by_xpath('//button[@id="cred_sign_in_button"]').click()
ele = browser.find_element_by_xpath('//*[@id="loginMessage"]/a')
ele.click()


element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="submitButton"]')))

browser.find_element_by_name("Password").send_keys("lhy_71171111111")
browser.find_element_by_xpath('//*[@id="submitButton"]').click()
time.sleep(20)


#decoce experiment

element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tasklist"]/div[2]/table/tbody/tr')))

ExpName_Url = {}
experiments = browser.find_elements_by_xpath('//*[@id="tasklist"]/div[2]/table/tbody/tr')
for experiment in experiments:
    exp_link_node = experiment.find_element_by_xpath('./td/a[@data-bind="attr: {href: UrlToTask(DbID())}, text: TaskName"]')
    exp_link_url = exp_link_node.get_attribute("href")
    exp_name = exp_link_node.text
    ExpName_Url[exp_name] = exp_link_url
    exp_link_node.click()

    browser.switch_to.window(browser.window_handles[-1])
    queryView_button_node = browser.find_element_by_link_text('Query View')
    queryView_button_node.click()
    element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="hitList"]/div[2]/table/tbody/tr')))
    queries_judges_link_node = browser.find_elements_by_xpath('//*[@id="hitList"]/div[2]/table/tbody/tr')
    for query_node in queries_judges_link_node:
        query_info_node = query_node.find_element_by_xpath("./td/a")
        query = query_info_node.text
        query_link = query_info_node.get_attribute('href')
        print("query:{0}\t{1}".format(query, query_link))

    break

for name, url in ExpName_Url.items():
    print("{0}\t{1}".format(name, url))

"""
# print(page_info.text)
pages = int((page_info.text.split('，')[0]).split(' ')[1])
for page in range(pages):
    if page > 2:
        break
    url = 'http://www.17huo.com/?mod=search&sq=2&keyword=%E7%BE%8A%E6%AF%9B&page=' + str(page + 1)
    browser.get(url)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)   # 不然会load不完整
    goods = browser.find_element_by_css_selector('body > div.wrap > div:nth-child(2) > div.p_main > ul').find_elements_by_tag_name('li')
    print('%d页有%d件商品' % ((page + 1), len(goods)))
    for good in goods:
        try:
            title = good.find_element_by_css_selector('a:nth-child(1) > p:nth-child(2)').text
            price = good.find_element_by_css_selector('div > a > span').text
            print(title, price)
        except:
            print(good.text)
"""
