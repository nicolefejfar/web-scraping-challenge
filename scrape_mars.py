import pandas as pd
import time
from splinter import Browser
from bs4 import BeautifulSoup

def init_browser():
    executable_path = {"executable_path": "c:/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
    browser = init_browser()

def scrape():
    browser = init_browser()
    
    # NASA News
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    time.sleep(2)
    soup = BeautifulSoup(browser.html, 'html.parser')
    result = soup.find_all('div', class_='list_text')[0]
    news_title = result.find('div', class_='content_title').text
    news_para = result.find('div', class_='article_teaser_body').text

    # JPL
    jpl_url = 'https://www.jpl.nasa.gov/'
    jpl_img_page = 'spaceimages/?search=&category=Mars'
    browser.visit(jpl_url + jpl_img_page)
    soup = BeautifulSoup(browser.html, 'html.parser')
    img_url = soup.find('article')['style']
    img_url = img_url.replace('background-image: url(',"").replace(');',"")[2:-1]
    featured_img_url = jpl_url + img_url

    # Facts Table? HTML?
    facts_url = 'https://space-facts.com/mars/'
    table = pd.read_html(facts_url)
    facts_df = table[0]
    html_table = facts_df.to_html(header=False, index=False, classes="table table-striped table-bordered table-sm")

    # USGS
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)
    soup = BeautifulSoup(browser.html, 'html.parser')
    items = soup.find('div', class_='result-list').find_all('div', class_='item')

    hem_data = []
    for item in items:
        hem_url = 'https://astrogeology.usgs.gov' + item.find('a')['href']
        hem_title = item.find('div',class_='description').find('a').find('h3').text
        hem_title = hem_title.replace(' Enhanced','')
        browser.visit(hem_url)
        time.sleep(1)
        hem_soup = BeautifulSoup(browser.html, 'html.parser')
        hem_info = hem_soup.find('div', class_='downloads')
        hem_dict = {
            'title':hem_title,
            'img_url': hem_info.find('li').find('a')['href']}
        hem_data.append(hem_dict)
    browser.quit()

    # Dictionary to hold all scraped data
    mars_data = {'news_title': news_title,
                'news_para': news_para,
                'featured_img_url': featured_img_url,
                'html_table': html_table,
                'hem_data': hem_data}

    return mars_data
    