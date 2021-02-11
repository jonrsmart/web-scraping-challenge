from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import pandas as pd 
import requests

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    #Featured Article Scrape
    url1 = 'https://mars.nasa.gov/news/'
    browser.visit(url1)
    html1 = browser.html
    soup1 = BeautifulSoup(html1, "html.parser")
    results = soup1.find_all('div', class_='slide')
    featured = []
    for result in results:
        title = result.find('div', class_='content_title').find('a').text
        paragraph = result.find('div', class_='rollover_description_inner').text
        featured.append({'title': title, 'paragraph': paragraph})

    #Mars Facts Table
    url2 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url2)
    mars_data = tables[0]
    mars_data.columns = ['Data', 'Value']
    mars_data.set_index('Data', inplace=True)
    mars_html = mars_data.to_html()
    mars_html2 = mars_html.replace('\n', '')

    #Mars Images Scrape
    
    url3 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    html2 = browser.html
    soup = BeautifulSoup(html2, 'html.parser')
    browser.visit(url3)
    image_info = []
    titles = []
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find_all('div', class_='item')
    for image in images:
        title = image.find('h3').text
        titles.append(title)
    for title in titles:
        browser.links.find_by_partial_text(title).click()
        html2 = browser.html
        soup = BeautifulSoup(html2, 'html.parser')
        bigpic = soup.find_all('div', class_='downloads')[0].li.a['href']
        hemi = soup.find('h2', class_='title').text
        image_info.append({'title':hemi, 'img_url':bigpic})
        browser.visit(url3)
    mars_dictionary = {'featured': featured,'mars_facts':mars_html2, 'mars_images':image_info}
    return mars_dictionary