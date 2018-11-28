
# coding: utf-8
# Import BeautifulSoup for parsing and splinter for site navigation
from bs4 import BeautifulSoup
from splinter import Browser

def scrape_all():
    executable_path = {"executable_path": 'C:/Users/danny/Downloads/chromedriver_win32/chromedriver'}
    browser = Browser("chrome", **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # In[2]:

    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # In[4]:

    slide_elem = news_soup.select_one('ul.item_list li.slide')
    #slide_elem

    # In[5]:

    news_title = slide_elem.find("div", class_='content_title').get_text()
    #news_title

    # In[6]:

    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    #news_p



    # # JPL Space Images Featured Image

    # In[12]:

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&catergory=Mars'
    browser.visit(url)

    # In[13]:

    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # In[14]:

    browser.is_element_present_by_text('more_info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # In[15]:

    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    # In[16]:

    img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    #img_url_rel

    # In[17]:

    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    #img_url



    # # Mars Weather

    # In[18]:

    url = 'https://twitter.com/marswxreport?lan=en'
    browser.visit(url)

    # In[19]:

    html = browser.html
    weather_soup = BeautifulSoup(html, 'html.parser')

    # In[20]:

    mars_weather_tweet = weather_soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})

    # In[21]:

    mars_weather = mars_weather_tweet.find('p', 'tweet-text').get_text()
    #mars_weather

    # In[22]:

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1rget&v1=Mars'
    browser.visit(url)

    # In[23]:

    hemisphere_image_urls = []

    links = browser.find_by_css("a.product-item h3")

    for i in range(len(links)):
        hemisphere = {}
        
        browser.find_by_css("a.product-item h3")[i].click()
        
        sample_elem = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        
        hemisphere['title'] = browser.find_by_css("h2.title").text
        
        hemisphere_image_urls.append(hemisphere)
        
        browser.back()

    # In[24]:

    #hemisphere_image_urls



    # # Mars Facts

    # In[26]:


    import pandas as pd
    df = pd.read_html('http://space-facts.com/mars/')[0]
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    #df


    # In[28]:


    #df.to_html()


    # In[29]:


    browser.quit()

    return_data = {
        "news_title": news_title,
        "news_parapgraph": news_p,
        "featured_imagine": img_url,
        "hemispheres": hemisphere_image_urls,
        "weather": mars_weather,
        "facts": df
    }

    return return_data



