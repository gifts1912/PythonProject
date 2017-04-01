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
fw = open("C:/Code/data/judgmentsQueryInfo.tsv", 'w', encoding='utf-8')
fw.write("TaskId\tQuery\tJudgeInfo\n")

element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tasklist"]/div[2]/table/tbody/tr')))
ExpName_Url = {}
experiments = browser.find_elements_by_xpath('//*[@id="tasklist"]/div[2]/table/tbody/tr')
main_window = browser.current_window_handle #window handle that display experiments list
exp_num = 0
for experiment in experiments:
    exp_num += 1
    exp_score_node = experiment.find_element_by_xpath('./td[@data-bind="text: UnweightedTotalScore, attr: {class:  getWinLossClass(IsStatSig(), UnweightedTotalScore())}"]')
    if exp_score_node.text == "NaN":
        continue
    exp_link_node = experiment.find_element_by_xpath('./td/a[@data-bind="attr: {href: UrlToTask(DbID())}, text: TaskName"]')
    exp_link_url = exp_link_node.get_attribute("href")
    exp_name = exp_link_node.text
    ExpName_Url[exp_name] = exp_link_url
    exp_link_node.send_keys(Keys.CONTROL + Keys.RETURN)

    #browser.find_element_by_tag_name("body").send_keys(Keys.CONTROL + Keys.TAB)
    browser.switch_to.window(browser.window_handles[-1])
    exp_window_handle = browser.window_handles[-1] #window that display judged queries list
    #extract experiment id
    link_toTaskIdPage_node = WebDriverWait(browser, 10).until(lambda browser: browser.find_element_by_xpath('//tbody/tr/td[@style="max-width:400px;"]/a[@href]'))
    link_toTaskIdPage_node.click()
    browser.switch_to.window(browser.window_handles[-1])
    taskId_node = WebDriverWait(browser, 10).until(lambda browser : browser.find_element_by_xpath('//div[@class="page-header-shortcuts"]/div[@class="tertiary-text"]'))
    taskId = taskId_node.text
    browser.close()
    browser.switch_to.window(exp_window_handle)

    #extract query information
    queryView_button_node = browser.find_element_by_link_text('Query View')
    queryView_button_node.click()
    element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="hitList"]/div[2]/table/tbody/tr')))
    queries_judges_link_node = browser.find_elements_by_xpath('//*[@id="hitList"]/div[2]/table/tbody/tr')
    for query_node in queries_judges_link_node:
        query_info_node = query_node.find_element_by_xpath("./td/a")
        query = query_info_node.text
        query_info_node.click()
        browser.switch_to.window(browser.window_handles[-1])
        google_bing_label_nodes = WebDriverWait(browser, 10).until( lambda webdriver:webdriver.find_elements_by_xpath('//*[@id="RightPane"]/table/tbody/tr/td/span[@style="color: red; font-weight: 700; font-size: x-large;"]'))
        left_node_label = google_bing_label_nodes[0].text
        right_node_lable = google_bing_label_nodes[-1].text
        """
        if left_node_label.lower().find("google") != -1:
            res = "{left:google, right:bing}"
        elif left_node_label.lower().find("bing") != -1:
            res = "{left:bing, right:google}"
        """
        res = "left:" + left_node_label.lower() + ", " + "right:" + right_node_lable.lower()
        print("{2}\t{0}\t{1}".format(query, res, taskId))
        fw.write("{2}\t{0}\t{1}\n".format(query, res, taskId))
        browser.close()
        browser.switch_to.window(exp_window_handle)
    print("\n\nExp finished {0}\n\n".format(exp_num))
    browser.close()
    browser.switch_to.window(main_window)


#Next page extract as above
nextPage_node = browser.find_element_by_xpath('//*[@id="tasklist"]/div[3]/div/span[4]/button')
nextPage_node.click()

experiments = browser.find_elements_by_xpath('//*[@id="tasklist"]/div[2]/table/tbody/tr')
for experiment in experiments:
    exp_num += 1
    exp_score_node = experiment.find_element_by_xpath('./td[@data-bind="text: UnweightedTotalScore, attr: {class:  getWinLossClass(IsStatSig(), UnweightedTotalScore())}"]')
    if exp_score_node.text == "NaN":
        continue
    exp_link_node = experiment.find_element_by_xpath('./td/a[@data-bind="attr: {href: UrlToTask(DbID())}, text: TaskName"]')
    exp_link_url = exp_link_node.get_attribute("href")
    exp_name = exp_link_node.text
    ExpName_Url[exp_name] = exp_link_url
    exp_link_node.send_keys(Keys.CONTROL + Keys.RETURN)

    #browser.find_element_by_tag_name("body").send_keys(Keys.CONTROL + Keys.TAB)
    browser.switch_to.window(browser.window_handles[-1])
    exp_window_handle = browser.window_handles[-1] #window that display judged queries list
    #extract experiment id
    link_toTaskIdPage_node = WebDriverWait(browser, 10).until(lambda browser: browser.find_element_by_xpath('//tbody/tr/td[@style="max-width:400px;"]/a[@href]'))
    link_toTaskIdPage_node.click()
    browser.switch_to.window(browser.window_handles[-1])
    taskId_node = WebDriverWait(browser, 10).until(lambda browser : browser.find_element_by_xpath('//div[@class="page-header-shortcuts"]/div[@class="tertiary-text"]'))
    taskId = taskId_node.text
    browser.close()
    browser.switch_to.window(exp_window_handle)

    #extract query information
    queryView_button_node = browser.find_element_by_link_text('Query View')
    queryView_button_node.click()
    element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="hitList"]/div[2]/table/tbody/tr')))
    queries_judges_link_node = browser.find_elements_by_xpath('//*[@id="hitList"]/div[2]/table/tbody/tr')
    for query_node in queries_judges_link_node:
        query_info_node = query_node.find_element_by_xpath("./td/a")
        query = query_info_node.text
        query_info_node.click()
        browser.switch_to.window(browser.window_handles[-1])
        google_bing_label_nodes = WebDriverWait(browser, 10).until( lambda webdriver:webdriver.find_elements_by_xpath('//*[@id="RightPane"]/table/tbody/tr/td/span[@style="color: red; font-weight: 700; font-size: x-large;"]'))
        left_node_label = google_bing_label_nodes[0].text
        right_node_lable = google_bing_label_nodes[-1].text
        """
        if left_node_label.lower().find("google") != -1:
            res = "{left:google, right:bing}"
        elif left_node_label.lower().find("bing") != -1:
            res = "{left:bing, right:google}"
        """
        res = "left:" + left_node_label.lower() + ", " + "right:" + right_node_lable.lower()
        print("{2}\t{0}\t{1}".format(query, res, taskId))
        fw.write("{2}\t{0}\t{1}\n".format(query, res, taskId))
        browser.close()
        browser.switch_to.window(exp_window_handle)
    print("\n\nExp finished {0}\n\n".format(exp_num))
    browser.close()
    browser.switch_to.window(main_window)

fw.close()
