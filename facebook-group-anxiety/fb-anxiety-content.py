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

def getPostDetail(post_href):
    ## post_href: a facebook post url
    ## return: post details from the post page

    base_href = 'https://mobile.facebook.com'
    print('Scraping ',post_href,'...')
    driver.get(base_href+post_href)
    time.sleep(3)
    
    comments = list()
    timestamp = ''
    content = list()
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    content = soup.find_all('p')
    if not content:
        stories = soup.find_all('span',{'class' : '_1-sk'})
        for story in stories:
            content.append(story.text)
        #content = story.text
    content = list(dict.fromkeys(content))
    timestamps = soup.find_all('abbr')
    if timestamps:
        timestamp = timestamps[0].text
    
    comments_all = soup.find_all('div', {'data-sigil' : 'comment-body'})
    
    for comment in comments_all:
        comments.append(comment.text)
    
    
    return pd.Series({'content': content, 'timestamp' : timestamp, 'comments' : comments})

""" Login Facebook """
def getFacebook():
    ## return: a list of links

    base_url =  'https://web.facebook.com'
    # group_id = '1059135227812853'     # Stress Management
    group_id = '944893365848617'        # Anxiety Disorder
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

    filename = group_id+'csv'
    # Load csv & parse one by one
    df = pd.read_csv(filename)
    df[['content','timestamp','comments']] = df['post_links'].apply(lambda x: getPostDetail(x))
    df.to_csv(filename, index = False)

def main():

    getFacebook()

if __name__ == '__main__':
	main()
