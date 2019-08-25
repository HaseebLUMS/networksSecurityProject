import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

lim = 20
lim_page = 5
trash = ['youtube.com', 'facebook.com', 'linkedin.com', 'twitter.com', 'quora.com', 'glassdoor.com', 'reddit.com', '.pdf', '.doc', '.docx']

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
    # cap = DesiredCapabilities().FIREFOX
    # cap["marionette"] = False
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options, executable_path='./geckodriver')
    browser.get('http://www.google.com')

    search = browser.find_element_by_name('q')
    search.send_keys(words)
    search.send_keys(Keys.RETURN)

    urls = []

    for p in range(1, lim_page):
        # print(".")
        try:
            time.sleep(1)
            if(len(urls) > lim):
                urls = urls[0:20]
                break
            res = browser.find_elements_by_xpath("//*[@href]")
            for r in res:
                # print(".")
                link = r.get_attribute('href')
                if 'https://www.google.com/search?' in link:
                    continue
                if 'google.com' in link:
                    continue
                if 'webcache.googleusercontent' in link:
                    continue
                if not is_url(link):
                    continue

                isTrash = False
                for tr in trash:
                    if tr in link:
                        isTrash = True
                if isTrash is True: continue
                urls.append(link)
        except Exception as info:
            print('ERROR: ', info)

        try: #if no next then return
            browser.find_element_by_xpath("//*[contains(local-name(), 'span') and contains(text(), 'Next')]").click()
        except:
            browser.quit()
            # print('=>', urls)
            return urls
    browser.quit()
    # print('=>', urls)
    return urls
