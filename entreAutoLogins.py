#!/usr/bin/env python

# waiting for login
# https://irwinkwan.com/2013/04/05/automating-the-web-with-selenium-complete-tasks-automatically-and-write-test-cases/
import os
import time

#Argparse
import argparse

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# Standard Libs
from random import *

browser = webdriver.Chrome()
# browser = webdriver.Firefox()
# browser = webdriver.Safari()

# Args
parser = argparse.ArgumentParser()
# parser.parse_args()

parser.add_argument("-v", "--verbose", help="increase output verbosity",action="store_true")
args = parser.parse_args()
if args.verbose:
    print("verbosity turned on")

#========================================== functions ===========================
def loginWeeklyReport(url, email, pwd):
	browser.get (url)

	browser.find_element_by_name("email").send_keys(email)
	browser.find_element_by_name("password").send_keys(pwd)
	browser.find_element_by_class_name("Button").click()
	browser.implicitly_wait(30)
	browser.find_element_by_name("high").send_keys("blah blah blah blah")

def loginEntre(url, email, pwd):
	# browser.implicitly_wait(30) # <- try for 30sec to do action 
	browser.get (url)
	# browser.find_element_by_id("chicago-button-no").click()
	browser.find_element_by_link_text("Log In").click()
	browser.find_element_by_name("email").send_keys(email)
	browser.find_element_by_name("password").send_keys(pwd)
	browser.find_element_by_name("commit").click()
	# browser.implicitly_wait(30)
	# browser.find_element_by_name("high").send_keys("blah blah blah blah")

# def randMailinatorAddress():
# 	randNum = randint(1, 10000)    # Pick a random number between 1 and 100.
# 	print(randNum)
# 	randEmail = "testUser ".replace(' ', str(randNum))
# 	print(randEmail)
# 	return randEmail

def becomeEntreMember(url):
	randUser = "testUser%s" % randint(1, 10000)
	print(randUser)
	randEmail = "%s@mailinator.com" % randUser
	print(randEmail)
	browser.get (url)
	browser.find_element_by_partial_link_text("Become").click()
	browser.find_element_by_partial_link_text("Become").click()
	browser.find_element_by_id("user_first_name").send_keys("testFirstName")
	browser.find_element_by_id("user_last_name").send_keys("testLastName")
	browser.find_element_by_id("user_email").send_keys(randEmail)
	browser.find_element_by_id("user_phone_number").send_keys("6155551234")
	browser.find_element_by_id("user_company_name").send_keys("La Hacienda")
	browser.find_element_by_name("password").send_keys("password")
	# browser.find_element_by_name("commit").click() # <- turn on when ready to create user

	# open new tab in Mailinator to watch emails
	browser.execute_script("window.open('https://www.mailinator.com/v2/inbox.jsp?zone=public&query=%s', 'new_window')" % randUser)
	browser.switch_to.window(browser.window_handles[0]) #<- switch tabs
	# browser.switch_to.window(browser.window_handles[1])
	# browser.switch_to.window(browser.window_handles[-1])

def getUsername(credFile):
	file = open(credFile,'r')#.readlines()
	for x, line in enumerate(file):
		if x == 0:
			username = line
	file.close()
	return(username)

def getPwd(credFile):
	file = open(credFile,'r')#.readlines()
	for x, line in enumerate(file):
		if x == 1:
			pwd = line
	file.close()
	return(pwd)

	# One Liner
	# for i in open(credFile,'r').readlines():
	# 	print(i)

def createNewUserQA(url):
	randUser = "testUser%s" % randint(1, 10000)
	print(randUser)
	randEmail = "%s@mailinator.com" % randUser
	print(randEmail)

	# root of domain
	browser.get (url)
	
	# go to allaccess
	browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)

	browser.find_element_by_partial_link_text("Become").click()
	
	# go to sign up page for allaccess
	browser.find_element_by_partial_link_text("Become").click()

	# fill out new All Access member form
	browser.find_element_by_id("user_first_name").send_keys("testFirstName")
	browser.find_element_by_id("user_last_name").send_keys("testLastName")
	browser.find_element_by_id("user_email").send_keys(randEmail)
	browser.find_element_by_id("user_phone_number").send_keys("6155551234")
	browser.find_element_by_id("user_company_name").send_keys("La Hacienda")
	browser.find_element_by_name("password").send_keys("password")
	browser.find_element_by_id("user_agreed_to_tos").click() # agree to terms checkbox
	browser.find_element_by_name("commit").click() # submit create new user

	# apply discount code before entering payment
	browser.find_element_by_id("coupon_code").send_keys("321") # enter discount code value
	browser.find_element_by_id("coupon_submit").click() # apply discount code
	# browser.implicitly_wait(5)
	# time.sleep(5)   # delays for 5 seconds. You can Also Use Float Value.
	browser.find_element_by_xpath("//input[@value='Next Page']").click() # submit
	
	# payment page
	iframe = browser.find_element_by_id("z_hppm_iframe")
	browser.switch_to.frame(iframe)
	print(browser.find_element_by_id("input-creditCardNumber").get_attribute("class"))
	browser.find_element_by_id("input-creditCardNumber").send_keys("5454545454545454")
	select_dropdown_value('input-creditCardExpirationMonth', '03')
	select_dropdown_value('input-creditCardExpirationYear', '2037')
	browser.find_element_by_id("input-cardSecurityCode").send_keys("989")
	select_dropdown_value('input-creditCardState', 'Tennessee')
	browser.find_element_by_id("input-creditCardAddress1").send_keys("123 Test Dr")
	browser.find_element_by_id("input-creditCardCity").send_keys("Nashville")
	browser.find_element_by_id("input-creditCardPostalCode").send_keys("37214")
	browser.find_element_by_id("submitButton").click()

	# initial login
	browser.implicitly_wait(40)
	browser.find_element_by_name("email").send_keys(randEmail)
	browser.find_element_by_name("password").send_keys("password")
	browser.find_element_by_name("commit").click()


def select_dropdown_value(id, value):

	selectOption = Select(browser.find_element_by_id(id))
	print("selectOption = %s" % selectOption)
	option_selected = selectOption.select_by_value(value)

def elementExists(url, locator_attr, locator_text):
	# Description: return true if element exists
	browser.get (url)
	try:
		browser.find_element(locator_attr, locator_text)
		print("true")
		return True
	except:
		print("false")
		return False


#========================================== main =================================

# loginWeeklyReport("https://weeklyreport.entreleadership.com", getUsername("./creds.py"), getPwd("./creds.py"))

# loginEntre("https://www.entreleadership.com", getUsername("./creds.py"), getPwd("./creds.py"))

# becomeEntreMember("https://www.entreleadership.com")



createNewUserQA("https://www.qa.entreleadership.com")



# loginEntre("https://www.test.entreleadership.com", getUsername("./creds.py"), getPwd("./creds.py"))

# elementExists("https://www.test.entreleadership.com", "by_css_selector", "HeroButter-heading")

# # Notes on tabs
# driver = webdriver.Chrome()

# # Open a new window
# # This does not change focus to the new window for the driver.
# driver.execute_script("window.open('');")

# # Switch to the new window
# driver.switch_to.window(driver.window_handles[1])
# driver.get("http://stackoverflow.com")

# # close the active tab
# driver.close()

# # Switch back to the first tab
# driver.switch_to.window(driver.window_handles[0])
# driver.get("http://google.se")

# # Close the only tab, will also close the browser.
# driver.close()
