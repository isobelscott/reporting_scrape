#!/usr/bin/env python3

from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import os
import sys


# get the number of days needed 
def get_days(start_date, end_date):
    start_d = datetime.strptime(start_date, '%m-%d-%Y')
    end_d = datetime.strptime(end_date, '%m-%d-%Y')
    time_d = end_d - start_d
    return time_d.days

# use an automated testing browser 
def make_profile():
    browser = webdriver.PhantomJS()
    return browser

# open the account
def open_sesame(browser, url, email, password):
    browser.get(url)
    account_email = browser.find_element_by_xpath('//*[@id="signin_email"]')
    password_field = browser.find_element_by_xpath('//*[@id="signin_password"]')
    account_email.send_keys(email)
    password_field.send_keys(password)
    signin = browser.find_element_by_xpath('//*[@id="loginform"]/button')
    signin.click()
    time.sleep(1)

# make a dataframe
def make_pandas(list1, list2, list3, list4, list5, list6, list7):
    df = pd.DataFrame(list(zip(list1, list2, list3, list4, list5, list6, list7)), 
        columns=['Day', 'Name', 'Impressions', 'Clicks', 'CTR', 'Avg CPC', 'Cost'])
    return df 

# output it to csv
def make_csv(df):
    new_csv = df.to_csv('daily.csv', index=False)
    return os.system("open daily.csv")

# scrape the info
def get_info(browser, days_needed):
    start_date  = datetime.today().date() - timedelta(days=1)
    date_urls = []
	
    for day in range(days_needed):
        start_date = start_date - timedelta(days=1)
        date_url = 'https://ads.indeed.com/job/ads?hd=0&startDate={0}&endDate={0}'.format(start_date) 
        date_urls.append(date_url)

    big_country_list, big_date_list, big_camp_list, big_impression_list, big_click_list, big_ctr_list, big_cpc_list, big_cost_list  = [], [], [], [], [], [], [], []

    for url in date_urls:
        browser.get(url)
        line_path = '//*[@id="sjc_table"]/tbody/tr'
        campaign_num1 = browser.find_elements_by_xpath(line_path)
        campaign_num = (len(campaign_num1) - 2)
        country_list, date_list, campaign_list, impression_list, click_list, ctr_list, cpc_list, cost_list = [], [], [], [], [], [], [], []
        base_num = 0 
        for campaign in range(campaign_num):
            base_num = base_num + 1
            
         
            impression_path = '//*[@id="sjc_table"]/tbody/tr[{0}]/td[4]'.format(base_num)
            impression_value = browser.find_element_by_xpath(impression_path).text
            
            if impression_value == '0':
            	pass
            	
            else:
            #get impressions
                impression_list.append(impression_value)
        
            #get clicks
                click_path = '//*[@id="sjc_table"]/tbody/tr[{0}]/td[5]'.format(base_num)
                click_title = browser.find_element_by_xpath(click_path).text
                click_list.append(click_title)
        
            #get CTR
                ctr_path = '//*[@id="sjc_table"]/tbody/tr[{0}]/td[7]'.format(base_num)
                ctr = browser.find_element_by_xpath(ctr_path).text
                ctr_list.append(ctr)

            #get avg cpc
                cpc_path = '//*[@id="sjc_table"]/tbody/tr[{0}]/td[10]/span'.format(base_num)
                cpc = browser.find_element_by_xpath(cpc_path).text
                cpc_list.append(cpc)

            #get cost
                cost_path = '//*[@id="sjc_table"]/tbody/tr[{0}]/td[9]/div[1]/span'.format(base_num)
                cost = browser.find_element_by_xpath(cost_path).text
                cost_list.append(cost)            
                   
            #get dates
                date_path = '//*[@id="sjc_table"]/thead/tr/th[2]/a'
                date_url = browser.find_element_by_xpath(date_path).get_attribute('href')  
                date = str(date_url).split('=')
                date_list.append(date[-1])
            
            #get campaign names
                campaign_path = '//*[@id="sjc_table"]/tbody/tr[{0}]/td[3]/span/span/a'.format(base_num)
                campaign_title = browser.find_element_by_xpath(campaign_path).text
                campaign_list.append(campaign_title)
	
			   
        #big_country_list.extend(country_list)
        big_date_list.extend(date_list)
        big_camp_list.extend(campaign_list)
        big_impression_list.extend(impression_list)
        big_click_list.extend(click_list)
        big_ctr_list.extend(ctr_list)
        big_cpc_list.extend(cpc_list)
        big_cost_list.extend(cost_list)
	
    return big_date_list, big_camp_list, big_impression_list, big_click_list, big_ctr_list, big_cpc_list, big_cost_list


def logout(browser):
    browser.get('https://ads.indeed.com/account/do-logout')
    time.sleep(1)


if __name__ == '__main__':
    print('\n')
    email1 = input('Please enter the account email address:  ')
    print('\n') 
    password1 = input('Enter the account password:   ')
    print('\n') 
    start_date = input('Enter start date in 01-02-2018 format:  ')
    print('\n') 
    end_date = input('Enter end date in 01-02-2018 format:  ')
    days_needed = get_days(start_date, end_date)
    print('\n')    
    print('Thank you! Processing now...')
    url = 'https://ads.indeed.com/job/ads'
    browser = make_profile()
    print('\n')
    open_sesame(browser, url, email1, password1)
    l1, l2, l3, l4, l5, l6, l7 = get_info(browser, days_needed)
    df1 = make_pandas(l1, l2, l3, l4, l5, l6, l7)
    make_csv(df1)
    browser.quit()