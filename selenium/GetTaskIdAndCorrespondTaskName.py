from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

browser = webdriver.Chrome("C:/Code/Tools/chromedriver.exe")
browser.get('https://sbswebapp.azurewebsites.net/TasksV2?filterId=124950')

#----------------------LogIn part -Begin- -------------
element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'passwd')))
element = browser.find_element_by_name("login")
element.clear()
element.send_keys("hengyliu@microsoft.com")
element = browser.find_element_by_name("passwd")
element.clear()
element.send_keys("lhy_71171111111")

element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginMessage"]/a')))
element.click()

element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="submitButton"]')))
browser.find_element_by_name("Password").send_keys("lhy_71171111111")
browser.find_element_by_xpath('//*[@id="submitButton"]').click()
time.sleep(20)
#--------------------LogIn part -End--------------------

#--------------------Decode query engine info -Begin--------------------
i = 0
while i < 2:
    if i == 1:
        nextPage_node = WebDriverWait(browser, 50).until(lambda browser : browser.find_element_by_xpath('//*[@id="tasklist"]/div[3]/div/span[4]/button'))
        nextPage_node.click() #not need to switch to latest window handle as no new window handle opened

    experiments = WebDriverWait(browser, 50).until(lambda browser: browser.find_elements_by_xpath('//div/table/tbody[@data-bind="foreach: PagedQuery"]/tr'))
    main_window = browser.current_window_handle #window handle that display experiments list
    exp_num = 0
    #---loop between submitted experiments----
    for experiment in experiments:
        exp_num += 1
        exp_score_node = experiment.find_element_by_xpath('./td[@data-bind="text: UnweightedTotalScore, attr: {class:  getWinLossClass(IsStatSig(), UnweightedTotalScore())}"]') #find specified experiment score to filter NAN job
        experiment_score = exp_score_node.text
        if experiment_score == "NaN":
            continue
        exp_link_node = experiment.find_element_by_xpath('./td/a[@data-bind="attr: {href: UrlToTask(DbID())}, text: TaskName"]') #find the link node to detail information about this experiment
        experiment_name = exp_link_node.text
        exp_link_node.click()

        browser.switch_to.window(browser.window_handles[-1]) #new tab window opened
        exp_window_handle = browser.window_handles[-1] #switch to latest opened tab window

        #extract group and task id
        link_toTaskIdPage_node = WebDriverWait(browser, 10).until(lambda browser: browser.find_element_by_xpath('//tbody/tr/td[@style="max-width:400px;"]/a[@href]'))
        link_toTaskIdPage_node.click() #stay the window handler to extract QueryView information

        browser.switch_to.window(browser.window_handles[-1])
        taskId_node = WebDriverWait(browser, 10).until(lambda browser : browser.find_element_by_xpath('//div[@class="page-header-shortcuts"]/div[@class="tertiary-text"]'))
        taskId = taskId_node.text
        print("{0}\t{1}\t{2}".format(experiment_name, experiment_score, taskId))
        browser.close()
        browser.switch_to.window(exp_window_handle) #switch to QueryView webpage
    i += 1