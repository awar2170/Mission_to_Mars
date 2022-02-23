#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import numpy as np
from webdriver_manager.chrome import ChromeDriverManager
import requests


# In[2]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[11]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[14]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[15]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[16]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[17]:


# 2. Create a list to hold the images and titles.
hemisphere_image = []
hemisphere_titles = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# Make a for loop 
    # So beautiful soup <- find the div and class item 
    # Grasp the images 
    # Grasp the titles

html = browser.html
img_soup = soup(html, 'html.parser')


# In[18]:


#### First Link Image URL: Cerberus ####

apple = img_soup.find('a', class_='itemLink product-item').get("href")
new_url = url + apple

browser.visit(new_url)
html = browser.html
img_soup_new = soup(html, 'html.parser')

banana = img_soup_new.find('div', class_="downloads").find("li").find("a").get('href')
image_url = new_url + banana
image_url

#### ---- #####


# In[19]:


#### Second Link Image URL: Schiaparelli #####
schiaparelli = img_soup.find_all('div', class_='item')[1].find('a', class_="itemLink product-item").get("href")
new_url_schia = url + schiaparelli 

browser.visit(new_url_schia)
html = browser.html 
img_soup_schia = soup(html, 'html.parser')

banana = img_soup_new.find('div', class_="downloads").find("li").find("a").get('href')
image_url = new_url + banana
image_url

#### ----- #####


# In[20]:


#### Third Link Image URL: Sytris #####
apple = img_soup.find_all('div', class_='item')[2].find('a', class_="itemLink product-item").get("href")
new_url = url + apple 

browser.visit(new_url)
html = browser.html 
img_soup_new = soup(html, 'html.parser')

banana = img_soup_new.find('div', class_="downloads").find("li").find("a").get('href')
image_url = new_url + banana
image_url

#### ----- #####


# In[21]:


#### Fourth Link Image URL: Valles #####
apple = img_soup.find_all('div', class_='item')[3].find('a', class_="itemLink product-item").get("href")
new_url = url + apple 

browser.visit(new_url)
html = browser.html 
img_soup_new = soup(html, 'html.parser')

banana = img_soup_new.find('div', class_="downloads").find("li").find("a").get('href')
image_url = new_url + banana
image_url

#### ----- #####


# In[22]:


content = []

for x in np.arange(0,4,1):
    apple = img_soup.find_all('div', class_='item')[x].find('a', class_="itemLink product-item").get("href")
    new_url = url + apple 

    browser.visit(new_url)
    html = browser.html 
    img_soup_new = soup(html, 'html.parser')

    banana = img_soup_new.find('div', class_="downloads").find("li").find("a").get('href')
    image_url = new_url + banana
    image_url
    
    info = {
        "image_url": image_url,
        "title": img_soup_new.find('h2', class_="title").text
    }
    content.append(info)


# In[23]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls = content
hemisphere_image_urls


# In[24]:


# 5. Quit the browser
browser.quit()


# In[ ]:




