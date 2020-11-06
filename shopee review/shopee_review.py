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

def getReview(list_res):

    users = list()
    ids = list()
    rating_overview = list()
    rating = list()
    reviews = list()
    variations = list()
    timestamps = list()

    for item in list_res:
        base_url = item[0]
        print('Loading product {} ...'.format(base_url))
        
        driver.get(base_url)
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 1500);")
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        pages = int(item[2]/6)
        
        product_rating_overview = soup.find_all('span',{'class':'product-rating-overview__rating-score'})
        if len(product_rating_overview)>0:
            rating_ov = float(product_rating_overview[0].text)
            for i in range(pages):
                print("scraping page",i,"of",pages)
                product_main = soup.find_all('div',{'class': 'shopee-product-rating__main'})
            
                for main in product_main:
                    ids.append(item[1])
                    rating_overview.append(rating_ov)
                    author_name = main.find_all('div',{'class':'shopee-product-rating__author-name'})
                    if len(author_name) > 0:
                        users.append(author_name[0].text)
                    else:
                        users.append(main.find_all('a',{'class':'shopee-product-rating__author-name'})[0].text)
                    review = main.find_all('div', {'class':'shopee-product-rating__content'})
                    if len(review) > 0:
                        reviews.append(review[0].text)
                    else:
                        reviews.append(np.nan)
                    variation = main.find_all('span',{'class': 'shopee-product-rating__variation'})[0].text
                    variations.append(variation)
                    stars = main.find_all('polygon',{'fill':'none'})
                    if len(stars) > 0:
                        rating.append(5-len(stars))
                    else: rating.append(5)
                    timestamps.append(main.find_all('div',{'class':'shopee-product-rating__time'})[0].text)
                driver.find_element_by_css_selector("button[class='shopee-icon-button shopee-icon-button--right ']").click();
                time.sleep(3)

    return pd.DataFrame({'id': ids, 'user': users,'rating_overview':rating_overview,'rating':rating,'review':reviews,'timestamp':timestamps})

def main():

    df = pd.read_csv('zanzea_products.csv')
    list_res = []
    for a, b, c in zip(df['links'], df['product_ids'], df['ratingCount']):
        list_res.append([a, b, c])
    reviews_df = getReview(list_res)
    reviews_df.to_csv('zanzea_reviews.csv')
if __name__ == '__main__':
	main()
