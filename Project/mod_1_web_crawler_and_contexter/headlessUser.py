import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

'''
Searched "words" on google 
by simulating user behavior by 
headless selenium so that there is 
no limit on searches
'''
def performSearch(words):
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options, executable_path='./mod_1_web_crawler_and_contexter/geckodriver')
    browser.get('http://www.google.com')

    search = browser.find_element_by_name('q')
    search.send_keys(words)
    search.send_keys(Keys.RETURN)


    path1 = '/html/body/div[6]/div[3]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div/div[3]/div/div['
    path2 = ']/div/div/div[1]/a/div/cite'


    path11= '/html/body/div[6]/div[3]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div/div/div/div['
    path22= ']/div/div/div[1]/a/div/cite'
    
    urls = []

    for p in range(1, 10):
        try:
            time.sleep(3)
            for i in range(1, 5):
                try:
                    path = path1+str(i)+path2
                    url = browser.find_element_by_xpath(path)
                    urls.append(url.text)
                except:
                    try:
                        path = path11+str(i)+path22
                        url = browser.find_element_by_xpath(path)
                        urls.append(url.text)
                    except:
                        pass
            if(len(urls) > 15):
                break
            browser.find_element_by_xpath("//*[contains(local-name(), 'span') and contains(text(), 'Next')]").click()
        except:
            pass
    browser.quit()
    if len(urls):
        print('urls fetched')
    return urls
performSearch('python')