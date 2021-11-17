# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 09:10:47 2021

Job Hunter:
    this definitely already exists but
    given a job description and a city 
    search on google the job and city
    stage one-grab the first few links
    stage two-search for exact matches between sites
    stage three-scrape out the company, some links, closing date...
    
    first session thoughts
    each recuiting site is a bit different 
    there is a lot of navigating
    its easy to get the wrong jobs 

@author: Patty Whack
"""

from selenium import webdriver as wd
from selenium.webdriver.common.by import By

url = "https://www.google.com" 
browser = wd.Chrome(executable_path='./chromedriver')
browser.get(url)

# wait until ready

# find the input by xpath
search_field = browser.find_element(By.XPATH, "//input")
# enter keys for your search
search_field.send_keys("QA Jobs Calgary \ue007'")
# hit search button 
#search_button = browser.find_element(by=XPATH, '//*submit')
#search_buttom = browser.find_element(by.link_text, "Google Search")
#search_button = browser.find_element_by_link_text("Google Search")
#search_button.click()

# wait until ready

# could either click 'explore jobs' or just pull all the links from below

# master list [] for all direct job links and decriptions

# list all the links we have the page with class g
all_links = browser.find_elements(By.PARTIAL_LINK_TEXT, 'Jobs')

all_links[4].click()

# on linkedin id="resultsCol" with class="slider_container"
# inside there is a class="jobCard_mainContent" and class="jobCardShelfContainer"

#page_body = browser.find_element(By.CSS_SELECTOR, 'jobDescriptionContent')
#print(page_body.get_attribute("text"))
'''
for link in all_links:
    #print(str(link.get_attribute("text")))
    link.click()
    page_body = browser.find_element(By.CLASS_NAME, "//body")
    print(page_body)
    # go to link (which will prob be another list of jobs)
    # get those links and click each one
    # get the text from those pages
    # if apply on company website is available click that
    # <section class="top-card-layout">
    # <div class="description__text description__text--rich"> 
    # add to master list of link and description
'''
# go through master list and
# check for duplicates -> list all unique?
# see if apply on their site is available?

#print(all_links)

