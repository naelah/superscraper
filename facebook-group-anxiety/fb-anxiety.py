import requests # for web requests
from bs4 import BeautifulSoup # a powerful HTML parser
from selenium.webdriver import Chrome
import pandas as pd # for .csv file read and write
import re # for regular regression handling
import time

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
path = "/usr/local/Caskroom/chromedriver/86.0.4240.22/chromedriver"
driver = Chrome(executable_path=path)
time.sleep(2)
num_of_scroll = 20

def scroll_to_the_bottom():
    retry = 0

    while retry < num_of_scroll:
        print('Scrolling..', retry)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        retry = retry + 1
        time.sleep(3)

""" scroll n times in fb page group  """
def getFacebook():
    ## return: a list of links

    base_url =  'https://web.facebook.com'
    group_id = '944893365848617'
    email = "arefieqa.1996@gmail.com"
    password = "Fiqa1996"
    print('Go to Facebook')
    driver.get(base_url)

    # Login
    print('Log in to Facebook')
    login_container = driver.find_element_by_xpath("//form[@class='_featuredLogin__formContainer']")
    email_input = login_container.find_element_by_xpath("//input[@id='email']")
    email_input.send_keys(email)
    password_input = login_container.find_element_by_xpath("//input[@id='pass']")
    password_input.send_keys(password)
    login_button = login_container.find_element_by_xpath("//button[@type='submit']")
    login_button.click()
    time.sleep(5)

    getLinks(group_id)


""" parse HTML strings for the list of posts"""
def getLinks(group_id):
    ## group_id: id of the fb group
    ## return: print parsed results to .csv file

    mobile_url = 'https://mobile.facebook.com/groups/'
    print('Go to the group')
    driver.get(mobile_url+group_id)
    time.sleep(3)


    # Scroll
    scroll_to_the_bottom()
    driver.implicitly_wait(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
   
    # Parse links
    urls = list()
    urls_clean = list()
    for a in soup.find_all('a', {'class': '_5msj'}):
        urls.append(a['href'])

    for url in urls:
        m = re.search('.*&refid', url)
        if m:
            text = m.group(0)
            urls_clean.append(text[:-6])
    urls_clean

    print("Successfully scraped",len(urls_clean),"post links")
    # transfrom the result to a pandas.DataFrame
    result = pd.DataFrame(urls_clean,columns=['post_links'])

    # save result,
    file_name = group_id+'.csv'
    result.to_csv(file_name,index=False)


def main():

    getFacebook()

if __name__ == '__main__':
	main()
