import pandas as pd
import requests # For downloading the website
from bs4 import BeautifulSoup # For parsing the website
import time # To put the system to sleep
import random # for random numbers


# %% -----------------------------------------

url = "https://www.bbc.com/news/world-us-canada-54238936"
page = requests.get(url)
page.status_code # 200 == Connection



# We've downloaded the entire website
page.content


soup = BeautifulSoup(page.content, 'html.parser')

# Let's look at the raw code of the downloaded website
print(soup.prettify())


# With the above in hand, we can find all instances of a tag at once.
soup.find_all('p') # Here I'm locating all the paragraph tags


# We can then convert the tag to text
soup.find_all('p')[15].get_text()

# Using a list comprehension we can do this for each paragraph tag
content1 = [i.get_text() for i in soup.find_all('p')]
content1


# As we can see, we get things that we want and some things that we don't want.
# So let's be more specific in targeting specific content.

# Can use a css selector to target specific content

# page > div:nth-child(1) > div.container > div > div.column--primary > div.story-body > div.story-body__inner > p.story-body__introduction
story_content = [i.get_text() for i in soup.select("div.story-body__inner p")]



# Join together as a single string
story_text = "\n".join(story_content)
print(story_text)


# Great! Now let's target different information like the headline and the date.


# Date CSS
#page > div:nth-child(1) > div.container > div > div.column--primary > div.story-body > div.with-extracted-share-icons > div > div.story-body__mini-info-list-and-share-row > div.mini-info-list-wrap > ul > li > div
css_loc = "div.mini-info-list-wrap > ul > li > div"
story_date = soup.select(css_loc)[0].get_text()


# Get story head line
story_headline = soup.find_all("h1")[0].get_text()



# Gather together
entry = [story_headline,story_date,story_text]
entry



# %% -----------------------------------------

# Building a scraper

# The idea here is to just wrap the above in a function.
# Input: url
# Output: relevant content


def bbc_scraper(url=None):

    # Download the webpage
    page = requests.get(url)

    # If a connection was reached
    if page.status_code == 200:

        # Parse
        soup = BeautifulSoup(page.content, 'html.parser')

        # Pull Headline
        story_headline = soup.find_all("h1")[0].get_text()

        # Pull Date
        story_date = soup.select("div.mini-info-list-wrap > ul > li > div")[0].get_text()

        # Pull story content
        story_content = [i.get_text() for i in soup.select("div.story-body__inner p")]
        story_text = " ".join(story_content)

        # Return data
        return [story_headline,story_date,story_text]

# Extract one webpage
bbc_scraper("https://www.bbc.com/news/world-us-canada-54238936")



# Now loop through urls of relevant stories
# Let's collect urls on all the relevant news stories of the day.

urls = ["https://www.bbc.com/news/world-us-canada-54238936",
        "https://www.bbc.com/news/world-us-canada-54254141",
        "https://www.bbc.com/news/world-us-canada-54229799",
        "https://www.bbc.com/news/world-us-canada-54244515"]


#Then just loop through and collect
scraped_data = []
for url in urls:

    # Scrape the content
    scraped_data.append(bbc_scraper(url))

    # Put the system to sleep for a random draw of time (be kind)
    time.sleep(random.uniform(.5,3))


# Look at the data object
scraped_data


# Organize as a pandas data frame
dat = pd.DataFrame(scraped_data,columns=["headline","date","content"])
dat.to_csv("scraped_web_data.csv",index=False)




# %% -----------------------------------------

# How to locate URLS?

main_bbc_page_url = "https://www.bbc.com/news"
main_page = requests.get(main_bbc_page_url)
main_page.status_code
main_soup = BeautifulSoup(main_page.content,'html.parser')


tag = main_soup.find_all("a")[10]
tag.attrs.get("href")


# Extract relevant links
links = set()
for tag in main_soup.find_all("a"):
    href = tag.attrs.get("href")
    if "world-us-canada" in href and "https:" not in href:
        links.update(["https://www.bbc.com" + href])
links


# %% -----------------------------------------

# Let's write the above as a single function
def link_scrape(urls=None,sleep=3):
    """Scrape multiple BBC URLS.

    Args:
        urls (list): list of valid BBC news urls.
        sleep (int): Integer value specifying how long the machine should be
                    put to sleep (random uniform). Defaults to 3.

    Returns:
        DataFrame: frame containing headline, date, and content fields
    """
    scraped_data = []
    for url in urls:

        print(url) # Keep track of where we are at.

        # Scrape the content
        scraped_data.append(bbc_scraper(url))

        # Put the system to sleep for a random draw of time (be kind)
        time.sleep(random.uniform(0,sleep))

    dat = pd.DataFrame(scraped_data,columns=["headline","date","content"])
    return dat


# This breaks. Why?
dat_content = link_scrape(urls=links)


# Code only works to scrape a very specific structure of the website.
links2 = list(links)
links2.pop(links2.index('https://www.bbc.com/news/world-us-canada-54242205'))
links2.pop(links2.index('https://www.bbc.com/news/world-us-canada-52497111'))
links2.pop(links2.index('https://www.bbc.com/news/world-us-canada-54244012'))

dat_content = link_scrape(urls=links2)



dat_content



# More advanced approaches to scraping the web.
# https://scrapy.org/
