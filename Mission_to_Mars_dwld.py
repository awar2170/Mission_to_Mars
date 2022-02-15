#!/usr/bin/env python
# coding: utf-8

# # Scape Mars Data: The News

# In[14]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[4]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Note: The browser.is_element_present_by_css('div.list_text', wait_time=1) line does 2 things 
    # search elements with a speciif combo tag div and list_text 
    # tells the browser to wait a section before looking at the page; 
        # This allow the page to laod fully before the program looks for things 


# In[5]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# Notice how we've assigned slide_elem as the variable to look for the <div /> tag and its descendent (the other tags within the <div /> element)? This is our parent element. This means that this element holds all of the other elements within it, and we'll reference it when we want to filter search results even further. The . is used for selecting classes, such as list_text, so the code 'div.list_text' pinpoints the <div /> tag with the class of list_text. CSS works from right to left, such as returning the last item on the list instead of the first. Because of this, when using select_one, the first matching element returned will be a <li /> element with a class of slide and all nested elements within it.
# 
# The data Robin wants to collect from this particular website is the most recent news article along with its summary. Remember, the code for this will eventually be used in an application that will scrape live data with the click of a button—this site is dynamic and the articles will change frequently, which is why Robin is removing the manual task of retrieving each new article.

# In[6]:


slide_elem.find('div', class_='content_title')

# above, we use .find to find the sepcifric information we are looking for 


# In[7]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# important
# 
# There are two methods used to find tags and attributes with BeautifulSoup:
# 
#     .find() is used when we want only the first class and attribute we've specified.
#     .find_all() is used when we want to retrieve all of the tags and attributes.
# 
# For example, if we were to use .find_all() instead of .find() when pulling the summary, we would retrieve all of the summaries on the page instead of just the first one.
# 

# In[8]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# # Scrape Mars Data: Features Image

# ### Featured Images 
# 
# https://spaceimages-mars.com/

# In[9]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[10]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[11]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[12]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# It's important to note that the value of the src will be different every time the page is updated, so we can't simply record the current value—we would only pull that image each time the code is executed, instead of the most recent one.
# 
# Above: 
# Let's break it down:
# 
#     An img tag is nested within this HTML, so we've included it.
#     .get('src') pulls the link to the image.
# 
# What we've done here is tell BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image. Basically we're saying, "This is where the image we want lives—use the link that's inside these tags."

# In[13]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# # Scrape Mars Data: Mars Facts
# 
# https://galaxyfacts-mars.com/
# 
# Instead of scraping each row, or the data in each <td />, we're going to scrape the entire table with Pandas' .read_html() function.

# In[15]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# Above Code: 
# Now let's break it down:
# 
#     df = pd.read_htmldf = pd.read_html('https://galaxyfacts-mars.com')[0] With this line, we're creating a new DataFrame from the HTML table. The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML. By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. Then, it turns the table into a DataFrame.
#     df.columns=['description', 'Mars', 'Earth'] Here, we assign columns to the new DataFrame for additional clarity.
#     df.set_index('description', inplace=True) By using the .set_index() function, we're turning the Description column into the DataFrame's index. inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.
# 
# Now, when we call the DataFrame, we're presented with a tidy, Pandas-friendly representation of the HTML table we were just viewing on the website.

# In[17]:


df.to_html() # converts the table into html


# In[18]:


# End session 
browser.quit()


# In[ ]:




