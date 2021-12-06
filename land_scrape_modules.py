# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 09:00:10 2021

@author: Patty Whack
"""
from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

class Browser_Super:
    '''' a somewhat java esque constructor
    containing the browser access and waiter functions
    '''
    def __init__(self, a_browser, a_waiter):
        self.browser = a_browser
        self.waiter = a_waiter
        return self

def launch_browser(url):
    chromedriver_service = Service('./chromedriver.exe')
    new_browser = wd.Chrome(service=chromedriver_service)
    new_browser.get(url)
    return new_browser

def wait_for_browser_ready(browser, condition):
    ''' called from within functions outside of main '''
    # wait until the page is loaded
    waiter = WebDriverWait(browser, 10)
    ready = waiter.until(EC.element_to_be_clickable((By.ID, condition)))
    return ready

def login(browser, username, password):
    ''' '''    
    wait_for_browser_ready(browser, 'btnLogin')
    # <input type="text" id="txtUserName" name="UserName" maxlength="50">
    user_name_field = browser.find_element(By.ID, "txtUserName")
    user_name_field.send_keys(username)
    
    # <input type="password" id="txtPassword" name="Password" maxlength="50">
    user_password_field = browser.find_element(By.ID, "txtPassword")
    user_password_field.send_keys("")
    
    # <input name="btnLogin" type="submit" id="btnLogin" class="green" value="Login">
    login_button = browser.find_element(By.ID, "btnLogin")
    login_button.click()
    
def list_events(browser):
    wait_for_browser_ready(browser, 'lnkUpcomingEvents')
    # ensure we are on the lnkUpcomingEvents page Upcoming Events
    upcoming_events_link = browser.find_element(By.ID, 'lnkUpcomingEvents')
    upcoming_events_link.click()
    
    # wait for rptUpcomingEvents_ctl00_divItemRow to all be ready
    upcoming_events_page_ready = waiter.until(EC.element_to_be_clickable((By.ID, 'rptUpcomingEvents_ctl00_btnRSVP')))
    
    page_soup = BeautifulSoup(browser.page_source, 'html.parser')
    evnt_title_links = page_soup.find_all("a", {"id" : re.compile('rptUpcomingEvents_ctl.*_hlkTitleUpcoming')})
    #print(event_title_links)
    
    return evnt_title_links

def get_related_events(browser, evnt_title_links):
    # slap all required sessions into one string for easy compare
    required_sessions_file = open(r"H:\2021-11-03-HIGHER-LANDING\schedule.txt", "r")
    required_sessions_string = required_sessions_file.read()
    
    ''' still need to do the date compare as well '''
     
    # check which ones are the right dates for my enrollment
    for link in evnt_title_links:
        if(link.text in required_sessions_string):
            '''link.text, event_time, zoom_link, description  '''
            #print(link['id'])
            print(link.text)
            click_me = browser.find_element(By.ID, link['id'])
            click_me.click()
            rsvp_page_ready = waiter.until(EC.element_to_be_clickable((By.ID, 'btnRSVP')))
            
            tmp_event_soup = BeautifulSoup(browser.page_source, 'html.parser')        
            zoom_link = tmp_event_soup.find('p', text=re.compile('^https:.*zoom'))        
            # get the parent/containing element
            description_container_element = zoom_link.parent        
            
            event_start_datetime = description_container_element.find(id='lblDatetime')
            #print(event_start_datetime.text.replace('/','-'))
            event_start_datetime_formatted = event_start_datetime.text.replace('/','-')
                    
            # find the start point that we are interested in
            text_start_point = description_container_element.find(id='lblDescription')        
            text_end_point = description_container_element.find(text=re.compile(".*Passcode:"))        
            
            actual_description_text = description_container_element.get_text(
                ).split("Send calendar to email")[1].strip('\n')
                    
            #print(actual_description_text)
            #zoom_link_text = zoom_link.text
            #print(zoom_link_text)        
            
            tmp_tuple = (link.text, event_start_datetime_formatted,
                         zoom_link.text, actual_description_text)
            events_to_attend_list.append(tmp_tuple)
        
            
        else:
            print("skipped")

def return_to_upcoming_events(browser):
    back_to_calendar_link = browser.find_element(By.ID, "hlkBackToCalendar")
    back_to_calendar_link.click()
    tmp_calendar_ready = waiter.until(EC.element_to_be_clickable((By.ID, 'lnkUpcomingEvents')))
    tmp_upcoming_events_link = browser.find_element(By.ID, 'lnkUpcomingEvents')
    tmp_upcoming_events_link.click()
    tmp_upcoming_events_page_ready = waiter.until(EC.element_to_be_clickable((By.ID, 'rptUpcomingEvents_ctl00_btnRSVP')))

def main():
    # url of where we are going   
    events_url = "https://suite.insala.com/ICM/Calendar/EventadminV5.aspx"
    
    # this will take us to the log in page
    browser = launch_browser(events_url)
    # we can use this waiter to halt execution
    waiter = WebDriverWait(browser, 10)
    
    user_name = "patrick.crosman@gmail.com"
    pass_word = "" # switch this to a simple load from a file
    
    # a java esque creation of a super browser
    brower_super = Browser_Super(browser, waiter)

    # log in using credentials
    login(browser, user_name, pass_word)
    event_title_links = list_events(browser)    
    get_related_events(browser, event_title_links)
    
    
    for event_title_link in event_title_links:
        event_details = get_event_details()
        events_to_attend_list.append(event_details)
        return_to_upcoming_events
    
    pass

if __name__ == '__main__':
    main()
    
# wait until the page is loaded
#waiter = WebDriverWait(browser, 10)
#ready_for_input = waiter.until(EC.element_to_be_clickable((By.ID, 'btnLogin')))

 
#waiter.until(EC.element_to_be_clickable((By.ID, 'lnkUpcomingEvents')))
waiter.until(EC.element_to_be_clickable((By.ID, 'lnkUpcomingEvents')))
# wait until events is loaded
#<div class="divTable" id="common-container" data-abobora="" style="width:100%">
#calendar_ready = waiter.until(EC.element_to_be_clickable((By.ID, 'lnkUpcomingEvents')))

# ensure we are on the lnkUpcomingEvents page Upcoming Events
#upcoming_events_link = browser.find_element(By.ID, 'lnkUpcomingEvents')
#upcoming_events_link.click()

# wait for rptUpcomingEvents_ctl00_divItemRow to all be ready
#upcoming_events_page_ready = waiter.until(EC.element_to_be_clickable((By.ID, 'rptUpcomingEvents_ctl00_btnRSVP')))

#page_soup = BeautifulSoup(browser.page_source, 'html.parser')
#event_title_links = page_soup.find_all("a", {"id" : re.compile('rptUpcomingEvents_ctl.*_hlkTitleUpcoming')})
#print(event_title_links)

# slap all required sessions into one string for easy compare
required_sessions_file = open(r"H:\2021-11-03-HIGHER-LANDING\schedule.txt", "r")
required_sessions_string = required_sessions_file.read()
 
# check which ones are the right dates for my enrollment
for link in event_title_links:
    if(link.text in required_sessions_string):
        #print(link['id'])
        click_me = browser.find_element(By.ID, link['id'])
        click_me.click()
        rsvp_page_ready = waiter.until(EC.element_to_be_clickable((By.ID, 'btnRSVP')))
        
        tmp_event_soup = BeautifulSoup(browser.page_source, 'html.parser')
        # give all text in div class events-calendar 
        # or all text in div class column wpc65 left
        tmp_event_column = tmp_event_soup.find(class_='column wpc65 left')
        p_tags = tmp_event_column.find_all("p") # [,"span"]
        # start of the description
        # <span id="lblDescription"></span>, 
        #text_i_want = explicit_for(list_of_things, conditions("lblDescription", "web.zoom.us"))
        #text_i_want = 
        
        print(p_span_tags)
        
        # , <span id="lblDescription"></span>,  everything after that
        # get next sibling until Passcode: or zoom
        
        # this is the zoom meeting link web.zoom.us
        #>Meeting ID: 816 4508 9906</p>,   can stop after this 
        #</span></p>, <span>Passcode: 
        
        
        back_to_calendar_link = browser.find_element(By.ID, "hlkBackToCalendar")
        back_to_calendar_link.click()
        tmp_calendar_ready = waiter.until(EC.element_to_be_clickable((By.ID, 'lnkUpcomingEvents')))
        tmp_upcoming_events_link = browser.find_element(By.ID, 'lnkUpcomingEvents')
        tmp_upcoming_events_link.click()
        tmp_upcoming_events_page_ready = waiter.until(EC.element_to_be_clickable((By.ID, 'rptUpcomingEvents_ctl00_btnRSVP')))
    else:
        print("skipped")

'''
these are in class="row pdb20"
<span id="lblTitle">Knowing Your Brand Part I</span>
<span id="lblStartDate">12/2/2021</span>
<span id="lblDatetime">12/2/2021 09:30 AM to 03:00 PM</span>

give me all p that are siblings of class="column wpc65 left"

'''

#for link in enumerate(filtered_links)
#tmp_url = filtered_links[0].href
#result = requests.get(tmp_url)
#print(result.text)
    
# for link in links - click or soup list, list <p> into a new text file

# class="column wpc65 left"   contains all event info
# class="row pdb20" contains the main stuff
# span id="lblTitle" Knowing Your Brand Part I
# span id="lblDatetime"

# div class="events-calendar" has everything so could just pull from there
# find partial link test  zoom.us
# zoom.us  https://us02web.zoom.us/j/83159945608?pwd=MUkrd0FObWsrWm9Yd1ZRcWlHeFgwUT09

# for file in files 

# create a calendar event for each file listed event

# now load up each one and 
# https://suite.insala.com/ICM/Calendar/EventDetails.aspx?EventID=344044&date=637743816000000000&dateDB=637743816000000000



#id="rptUpcomingEvents_ctl00_hlkTitleUpcoming"
#print(event_titles)

#ocating Elements by Tag Name

# text_to_be_present_in_element_value

#event_list = wd.findAll(By.XPATH("//*[@id='rptUpcomingEvents_ct*_divItemRow']" ))

# right need to log in here
#print(event_list)


#<input type="submit" name="rptUpcomingEvents$ctl00$btnRSVP" value="RSVP" onclick="fw.GetRSVP(this, 343247,637739442000000000,0); return false;" id="rptUpcomingEvents_ctl00_btnRSVP" class="green-action edit">

# find all links with id="rptUpcomingEvents_ct*_hlkTitleUpcoming"
#//*[@id="rptUpcomingEvents_ctl00_hlkTitleUpcoming"]
#all_event_titles = browser.find_elements(   By.ID, 'rptUpcomingEvents_ctl*_hlkTitleUpcoming')