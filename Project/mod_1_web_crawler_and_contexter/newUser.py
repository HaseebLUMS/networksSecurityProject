import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


''' checks for url
    #The only problem here can be that 
    #the extracted text might have spaces
    #and be not a url
    #Also some url are not complete
    they end at ...
'''
def is_url(url):
    if " " in url: return False
    if "..." in url: return False
    return True


'''
Searched "words" on google 
by simulating user behavior by 
headless selenium so that there is 
no limit on searches
'''

def perform_search(words):
    print('Headless browser active.')
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options, executable_path='./mod_1_web_crawler_and_contexter/geckodriver')
    browser.get('http://www.google.com')

    search = browser.find_element_by_name('q')
    search.send_keys(words)
    search.send_keys(Keys.RETURN)

    urls = []

    for p in range(1, 5):
        try:
            time.sleep(1)
            if(len(urls) > 20):
                break
            res = browser.find_elements_by_xpath("//*[@href]")
            for r in res:
                link = r.get_attribute('href')
                if 'https://www.google.com/search?' in link:
                    continue
                if 'google.com' in link:
                    continue
                if not is_url(link):
                    continue
                urls.append(link)
        except info:
            print('ERROR: ', info)

        try: #if no next then return
            browser.find_element_by_xpath("//*[contains(local-name(), 'span') and contains(text(), 'Next')]").click()
        except:
            browser.quit()
            print('=>', urls)
            return urls
    browser.quit()
    print('=>', urls)
    return urls


perform_search('ASUS RT-AC58U router')