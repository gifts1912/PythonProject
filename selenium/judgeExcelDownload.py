from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


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
main_window = browser.current_window_handle #window handle that display experiments list
i = 0
for experiment in experiments:
    exp_link_node = experiment.find_element_by_xpath('./td/a[@data-bind="attr: {href: UrlToTask(DbID())}, text: TaskName"]')
    exp_link_url = exp_link_node.get_attribute("href")
    exp_name = exp_link_node.text
    ExpName_Url[exp_name] = exp_link_url
    exp_link_node.click()

    #browser.find_element_by_tag_name("body").send_keys(Keys.CONTROL + Keys.TAB)
    browser.switch_to.window(browser.window_handles[-1])
    exp_window_handle = browser.window_handles[-1] #window that display judged queries list
    link_toExcelPage_node = WebDriverWait(browser, 10).until(lambda browser: browser.find_element_by_xpath('//*[@id="task_268843"]/td[7]/a'))
    link_toExcelPage_node.click()
    browser.close()
    browser.switch_to.window(browser.window_handles[-1])

    link_toExcel_node = WebDriverWait(browser, 10).until(lambda browser: browser.find_element_by_xpath('//*[@id="infoTable"]/tbody/tr[11]/td[2]/span[3]/a[text()="Export All Judgments including URLs To Excel"]'))
    link_toExcel_node.click()
    browser.close()
    browser.switch_to.window(main_window)