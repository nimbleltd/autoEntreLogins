#!/usr/bin/env python

import os
import sys
import time
import datetime
from numpy import base_repr

#Argparse
import argparse

# beautiful soup
import bs4 as bs

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# Standard Libs
from random import *
import random
import subprocess # <-- to get clipboarData

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
	# browser.implicitly_wait(30)
	# browser.find_element_by_name("high").send_keys("blah blah blah blah")

def loginEntre(url, email, pwd):

	browser.get (url)
	browser.find_element_by_link_text("Log In").click()
	browser.find_element_by_name("email").send_keys(email)
	browser.find_element_by_name("password").send_keys(pwd)
	browser.find_element_by_name("commit").click()

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


	# One Liner
	# for i in open(credFile,'r').readlines():
	# 	print(i)

def createNewUserAA(url, randUser, randEmail):
	whichEnv = url.split('.')[1]

	# root of domain
	browser.get (url)
	
	# go to allaccess
	browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)

	browser.find_element_by_partial_link_text("Become").click()
	
	# go to sign up page for allaccess
	browser.find_element_by_partial_link_text("Become").click()

	# fill out new All Access member form
	browser.find_element_by_id("user_first_name").send_keys("testFirstName")
	browser.find_element_by_id("user_last_name").send_keys("%s" % randUser)
	browser.find_element_by_id("user_email").send_keys(randEmail)
	browser.find_element_by_id("user_phone_number").send_keys("6155551234")
	browser.find_element_by_id("user_company_name").send_keys("Fluke Lasers")
	browser.find_element_by_name("password").send_keys("password")
	browser.find_element_by_id("user_agreed_to_tos").click() # agree to terms checkbox
	# browser.implicitly_wait(30)
	# time.sleep(3)
	browser.find_element_by_name("commit").click() # submit create new user

	if whichEnv == 'qa':
		print("TestEnv = %s" % whichEnv)
		# apply discount code before entering payment https://www.qa.entreleadership.com/pay
		browser.find_element_by_id("coupon_code").send_keys("321") # enter discount code value
		browser.find_element_by_id("coupon_submit").click() # apply discount code
		browser.find_element_by_xpath("//input[@value='Next Page']").click() # submit
	else:
		print("TestEnv = %s \nskipping discount code test" % whichEnv)
		browser.implicitly_wait(5)
		time.sleep(5)   # delays for 5 seconds. You can Also Use Float Value.
		browser.find_element_by_xpath("//input[@value='Next Page']").click() # submit
	

	
	# payment page
	iframe = browser.find_element_by_id("z_hppm_iframe")
	browser.switch_to.frame(iframe)
	browser.find_element_by_id("input-creditCardNumber").send_keys("5454545454545454")
	select_dropdown_value('input-creditCardExpirationMonth', '03')
	select_dropdown_value('input-creditCardExpirationYear', '2037')
	browser.find_element_by_id("input-cardSecurityCode").send_keys("989")
	select_dropdown_value('input-creditCardState', 'Tennessee')
	browser.find_element_by_id("input-creditCardAddress1").send_keys("123 Test Dr")
	browser.find_element_by_id("input-creditCardCity").send_keys("Nashville")
	browser.find_element_by_id("input-creditCardPostalCode").send_keys("37214")
	browser.find_element_by_id("submitButton").click()

	# initial user login
	browser.implicitly_wait(35)
	browser.find_element_by_name("email").send_keys(randEmail)
	browser.find_element_by_name("password").send_keys("password")
	browser.find_element_by_name("commit").click()

	# # all acces on boarding, watch intro video, click next
	# print("before waiting")
	# browser.implicitly_wait(30)
	# time.sleep(15)
	# browser.find_element_by_xpath("//button[@name='button']").click()
	# print("should have clicked Next now...")

	# Get-Started
	browser.find_element_by_link_text("Get Started Now").click()

	# Onboarding Steps
	# ==========================================================
	# Join Mastermind
	# ================
	browser.find_element_by_xpath("//span[@class='GetStarted-title']").click()
	print("click mm button")
	time.sleep(1)
	print("sleep before clicking 'join MM bullet link'")
	browser.find_element_by_xpath("//span[@class='GetStarted-title']").click()
	print("before clicking join MM link to next page")
	browser.find_element_by_xpath("//a[contains(text(), 'Join a Mastermind Group')]").click()
	# browser.find_element_by_partial_link_text("Join a Mastermind Group").click()
	print("after clicking joining MM group link to new page")
	# browser.find_element_by_link_text("Join a Mastermind Group").click()

	# Edit profile page https://www.qa.entreleadership.com/mastermind 
	browser.find_element_by_link_text("Edit My Profile").click()

	# Completed your profile
	#Industry
	browser.implicitly_wait(30)
	wait = WebDriverWait(browser, 5)
	# element = wait.until(EC.element_to_be_clickable((By.ID, 'profile-card-field-industry')))
	# print("begun profile")

	# # select industry info
	# browser.find_element_by_xpath("//div[@id='profile-card-field-industry']//i[@class='fa fa-plus profile-card-field-icon plus']").click()
	# select_dropdown_value('user_industry', 'Financial Services')
	
	# # save Industry changes
	# wait.until(EC.element_to_be_clickable((By.ID, 'profile-card-field-form-industry')))
	# time.sleep(5)
	# timeout = 5
	# try:
	# 	element_present = EC.presence_of_element_located((By.ID, 'profile-card-field-form-industry'))
	# 	WebDriverWait(browser, timeout).until(element_present)
	# 	browser.implicitly_wait(5)
	# 	time.sleep(5)
	# 	browser.find_element_by_xpath("//div[@id='profile-card-field-form-industry']//button[@type='submit']").click()
	# except:
	# 	print("busted, didn't find %s" % element_present)

	# Team Size 
	browser.find_element_by_xpath("//div[@id='profile-card-field-num_of_employees']//i[@class='fa fa-plus profile-card-field-icon plus']").click()	
	select_dropdown_value('user_num_of_employees', '2-10')
	browser.implicitly_wait(5)
	time.sleep(5)
	browser.find_element_by_xpath("//div[@id='profile-card-field-form-num_of_employees']//button[@type='submit']").click()
	# Gross Revenue 
	browser.find_element_by_xpath("//div[@id='profile-card-field-gross_revenues']//i[@class='fa fa-plus profile-card-field-icon plus']").click()	
	select_dropdown_value('user_gross_revenues', '$500,000-$999,999')
	browser.find_element_by_xpath("//div[@id='profile-card-field-form-gross_revenues']//button[@type='submit']").click()
	
	# # Go to the Next Page
	# browser.implicitly_wait(5)
	# time.sleep(9)
	# browser.find_element_by_xpath("//button[@data-event='completed_profile_setup']").click()

	# Choose Friday 10am MM Group
	browser.implicitly_wait(5)
	time.sleep(5)
	if whichEnv == "qa":
		browser.find_element_by_id("mastermind-group-92").click() # qa
	else:
		browser.find_element_by_id("mastermind-group-133").click() # test
	browser.find_element_by_xpath("//button[@data-target='3']").click()

	# Get Started: https://www.qa.entreleadership.com/get-started?step=validate_sync_ecoaching
	browser.implicitly_wait(5)
	time.sleep(8)
	# browser.find_element_by_link_text("Get Started").click()
	browser.find_element_by_xpath("//a[@data-event='completed_ecoaching_sync']").click()

	
	# Open Mailinator to see
	browser.execute_script("window.open('https://www.mailinator.com/v2/inbox.jsp?zone=public&query=%s', 'new_window')" % randUser)


	# close driver
	# browser.close()

def select_dropdown_value(id, value):
	selectOption = Select(browser.find_element_by_id(id))
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


def getClipboardData():
 p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
 retcode = p.wait()
 data = p.stdout.read()
 return data

def setClipboardData(data):
 p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
 p.stdin.write(data)
 p.stdin.close()
 retcode = p.wait()



def signUpAAuserForWRT(url, email, password, firstLogin, am_i_signed_in, num_users_to_create):
	browser.get (url)

	if am_i_signed_in == True:
		pass
	else:
		# WRT Sign In
		browser.find_element_by_name("email").send_keys(email)
		browser.find_element_by_name("password").send_keys(password)
		browser.find_element_by_class_name("Button").click()

	# # Get started
	if firstLogin == True:
		try:
			browser.implicitly_wait(10)
			browser.find_element_by_xpath("//a[contains(text(), 'Get Started')]").click()

			# Continue Sign-up
			browser.find_element_by_name("title").send_keys("Nerf Herder")
			browser.implicitly_wait(10)
			time.sleep(5)
			browser.find_element_by_xpath("//button[contains(text(), 'Continue')]").click()
		except Exception:
			print("Not my first login")
			pass

	# Invite Team
	# copy link
	browser.implicitly_wait(10)
	time.sleep(10)
	browser.find_element_by_xpath("//button[contains(text(), 'Copy Link')]").click()
	comapnyLink = str(getClipboardData())
	# drop un-needed chars on clipboard content
	comapnyLink = comapnyLink[2:-1]
	randUser = email.split('@')[0]
	# Add n number users to the Company WRT
	for n in range(0, num_users_to_create):
		print("n = %s" % n)
		time.sleep(1)
		# browser.switch_to.window(browser.window_handles[(n-1)])
		browser.execute_script("window.open('%s', 'tab%s')" % (comapnyLink, (n)))
		browser.switch_to.window('tab%s' % (n))
		time.sleep(2)
		try:
			browser.find_element_by_xpath("//input[@class='SelectBox PersistEmail-field']").send_keys("%s-%s@mailinator.com" % (randUser, n))
			browser.find_element_by_xpath("//button[contains(text(), 'Sign Up')]").click()
			browser.find_element_by_xpath("//input[@name='firstName']").send_keys("fName")
			browser.find_element_by_xpath("//input[@name='lastName']").send_keys("%s-%s" % (randUser, n))
			browser.find_element_by_xpath("//input[@name='title']").send_keys("Nerf Herder")
			browser.find_element_by_xpath("//input[@name='password']").send_keys("password")
			browser.find_element_by_xpath("//button[contains(text(), 'Continue')]").click()
			browser.implicitly_wait(20)
			time.sleep(10)
			browser.find_element_by_xpath("//div[@id='addeventatc1']").click()
			browser.find_element_by_xpath("//div[@id='addeventatc1']").click()
		except:
			pass
	browser.switch_to.window(browser.window_handles[0])

	# Go to "Edit Team" page
	print("before sleep before clicking weekly report tool")
	time.sleep(1)
	print("before clicking weekly report tool")
	print("about to exit program")
	sys.exit()
	sys.exit(0)
	print("exited")
	# os.system("pause")
	# time.sleep(45)
	browser.find_element_by_xpath("//a[contains(text(), 'Weekly Report Tool')]").click()
	time.sleep(2)
	browser.refresh()
	browser.refresh()
	time.sleep(2)
	browser.refresh()
	print("after clicking weekly report tool")
	time.sleep(1)
	print("after sleep after clicking weekly report tool")
	browser.find_element_by_xpath("//a[contains(text(), 'Edit Team')]").click()
	print("after clicking Edit Team")
	time.sleep(3)
	print("after waiting 3 sec after clicking Edit Team")
	# CRUD members of team
	browser.find_element_by_xpath("//div[@class='TeamMemberPanel TeamMemberPanel--admin']").click()
	print("after clicking team meber")
	browser.find_element_by_xpath("//button[contains(text(), 'Edit')]").click()
	# edit team member first name
	browser.find_element_by_name("firstName").click()
	time.sleep(1)
	browser.find_element_by_name("firstName").clear()
	time.sleep(1)
	timestamp = datetime.datetime.now().strftime('%b-%d_%I:%M:%S')
	time.sleep(1)
	browser.find_element_by_name("firstName").send_keys("botWroteThis-%s" % timestamp)
	time.sleep(2)
	# same user new name
	browser.find_element_by_class_name("Button").click()

	# delete team member from team
	findTeamMemeberToBeDeleted = browser.find_elements_by_xpath("//div[@class='TeamMemberPanel TeamMemberPanel--admin']") #clickable by selenium
	findTeamMemeberNameToBeDeleted = browser.find_elements_by_xpath("//div[@class='TeamMemberPanel-label']") # list of names of users on the page
	print("findTeamMemeberToBeDeleted = %s" % len(findTeamMemeberToBeDeleted))
	time.sleep(2)
	teamMemberThreeToBeDeleted = findTeamMemeberToBeDeleted[2]
	teamMemberThreeToBeDeleted.click()
	print("after clicking 3rd member")
	browser.find_element_by_xpath("//button[contains(text(), 'Delete')]").click()
	browser.find_element_by_xpath("//button[contains(text(), 'Delete')]").click()
	print("User %s has been deleted, attempted" % findTeamMemeberNameToBeDeleted[2].text)

	findTeamMemeberNameAfterDeletion = browser.find_elements_by_xpath("//div[@class='TeamMemberPanel-label']") # list of names of users on the page
	# time.sleep(2)
	# print("teamMemberThreeToBeDeleted = %s" % findTeamMemeberNameToBeDeleted[2].text)
	# print("findTeamMemeberNameAfterDeletion[2].text = %s" % findTeamMemeberNameAfterDeletion[2].text)

	if findTeamMemeberNameToBeDeleted[2].text == findTeamMemeberNameAfterDeletion[2].text:
		print("User %s has been deleted" % findTeamMemeberNameToBeDeleted[2].text)
	else:
		print("problem occured user: %s was not deleted" % findTeamMemeberNameToBeDeleted[2].text)


def createNewAAonly():
	env = "test"
	randUser = "genUserBilly%s" % randint(1, 10000)
	# randUser = "kylecentervillepediatricdentistry"
	print(randUser)
	randEmail = "%s@mailinator.com" % randUser
	print(randEmail)

	createNewUserAA("https://www.%s.entreleadership.com" % (env), randUser, randEmail)

def loginWRT(email, password, env):
	browser.get ("https://weeklyreport.%s.entreleadership.com/get-started" % (env))
	browser.implicitly_wait(30)
	time.sleep(3)
	browser.find_element_by_name("email").send_keys(email)
	browser.find_element_by_name("password").send_keys(password)
	browser.find_element_by_class_name("Button").click()
	time.sleep(2)

# workflows
# =====================================================================

# ===================================================
# Create many team members using company sign up link
# ===================================================
def createUserByCompanyLink(companyURL, num_users_to_create):
	comapnyLink = companyURL
	email = "makeManyUsers9998@mailinator.com"
	randUser = email.split('@')[0]
	# Add n number users to the Company WRT
	for n in range(0, num_users_to_create):
		print("n = %s" % n)
		time.sleep(1)
		# browser.switch_to.window(browser.window_handles[(n-1)])
		browser.execute_script("window.open('%s', 'tab%s')" % (comapnyLink, (n)))
		browser.switch_to.window('tab%s' % (n))
		time.sleep(2)
		try:
			browser.find_element_by_xpath("//input[@class='SelectBox PersistEmail-field']").send_keys("%s-%s@mailinator.com" % (randUser, n))
			browser.find_element_by_xpath("//button[contains(text(), 'Sign Up')]").click()
			browser.find_element_by_xpath("//input[@name='firstName']").send_keys("fName")
			browser.find_element_by_xpath("//input[@name='lastName']").send_keys(randUser)
			browser.find_element_by_xpath("//input[@name='title']").send_keys("Nerf Herder")
			browser.find_element_by_xpath("//input[@name='password']").send_keys("password")
			browser.find_element_by_xpath("//button[contains(text(), 'Continue')]").click()
			browser.implicitly_wait(20)
			time.sleep(10)
			browser.find_element_by_xpath("//div[@id='addeventatc1']").click()
			browser.find_element_by_xpath("//div[@id='addeventatc1']").click()
		except:
			pass
	browser.switch_to.window(browser.window_handles[0])

# ===================================================

# =================
#  Forgot Password
# =================
# loginWRT("genUser2317@mailinator.com", "password", "qa")

def createNewAAandWRTuser():
	env = "qa"
	randUser = "testUser%s" % base_repr(int(time.time()), 36)
	# randUser = "kylecentervillepediatricdentistry"
	print(randUser)
	randEmail = "%s@mailinator.com" % randUser
	print(randEmail)
	# return randEmail

	createNewUserAA("https://www.%s.entreleadership.com" % (env), randUser, randEmail)
	signUpAAuserForWRT("https://weeklyreport.%s.entreleadership.com/get-started" % (env), randEmail, "password" , True, True, 2)

def newDashBoardOnboardingSteps(whichEnv):
	print("sleep before clicking 'join MM bullet link'")
	# browser.find_element_by_xpath("//span[@class='GetStarted-title']").click()
	print("before clicking join MM link to next page")
	browser.find_element_by_xpath("//a[contains(text(), 'Join a Mastermind Group')]").click()
	# browser.find_element_by_partial_link_text("Join a Mastermind Group").click()
	print("after clicking joining MM group link to new page")
	# browser.find_element_by_link_text("Join a Mastermind Group").click()

	# Edit profile page https://www.qa.entreleadership.com/mastermind 
	browser.find_element_by_link_text("Edit My Profile").click()
	
	# Edit User profile so we can pass MM min signup requirments
	browser.find_element_by_xpath("//div[@id='profile-card-field-num_of_employees']//i[@class='fa fa-plus profile-card-field-icon plus']").click()	
	select_dropdown_value('user_num_of_employees', '2-10')
	browser.implicitly_wait(5)
	time.sleep(1)
	browser.find_element_by_xpath("//div[@id='profile-card-field-form-num_of_employees']//button[@type='submit']").click()
	# Gross Revenue 
	browser.find_element_by_xpath("//div[@id='profile-card-field-gross_revenues']//i[@class='fa fa-plus profile-card-field-icon plus']").click()	
	select_dropdown_value('user_gross_revenues', '$500,000-$999,999')
	browser.find_element_by_xpath("//div[@id='profile-card-field-form-gross_revenues']//button[@type='submit']").click()

	#  Go to MM
	time.sleep(5)
	browser.find_element_by_xpath("//a[contains(text(), 'Mastermind')]").click()

	#  Sign me up for an MM Group
	time.sleep(5)
	browser.refresh()
	# time.sleep(3)
	# browser.refresh()
	browser.find_element_by_xpath("//a[contains(text(), 'Sign Me Up for a Group!')]").click()
	browser.implicitly_wait(5)
	time.sleep(5)
	if whichEnv == "qa":
		browser.find_element_by_id("mastermind-group-92").click() # qa
	else:
		browser.find_element_by_id("mastermind-group-133").click() # test
	browser.find_element_by_xpath("//input[@value='Sign Me Up!']").click()
	time.sleep(5)

	#  Go back to dashboard
	browser.find_element_by_xpath("//a[contains(text(), 'Dashboard')]").click()

	# Set Up Weekly Report Tool
	# browser.find_element_by_xpath("//a[contains(text(), 'Set Up Weekly Report Tool')]").click()
	browser.find_element_by_link_text("Set Up Weekly Report Tool").click()
	browser.find_element_by_link_text("Set up the Weekly Report Tool").click()

	# WRT get started
	browser.find_element_by_link_text("Get Started").click()
	time.sleep(2)
	#  Enter job title
	browser.find_element_by_name("title").send_keys("Nerf Herder")
	browser.implicitly_wait(10)
	time.sleep(5)
	browser.find_element_by_xpath("//button[contains(text(), 'Continue')]").click()

	


def onbpardFB():
	# # signup for Facebook
	browser.switch_to.window(browser.window_handles[0])
	browser.find_element_by_xpath("//a[contains(text(), 'Dashboard')]").click()
	browser.find_element_by_link_text("Join our Facebook Commmunity").click()
	browser.find_element_by_xpath("//a[contains(text(), 'Join our Facebook Community')]").click()


def inviteWrtTeamMembers(email, start_num, end_num):
	# Invite Team by copying link
	time.sleep(3)
	browser.find_element_by_xpath("//button[contains(text(), 'Copy Link')]").click()
	comapnyLink = str(getClipboardData())
	# drop un-needed chars on clipboard content
	comapnyLink = comapnyLink[2:-1]
	randUser = email.split('@')[0]
	# Add n number users to the Company WRT
	for n in range(start_num, end_num):
		print("n = %s" % n)
		time.sleep(1)
		# browser.switch_to.window(browser.window_handles[(n-1)])
		browser.execute_script("window.open('%s', 'tab%s')" % (comapnyLink, (n)))
		browser.switch_to.window('tab%s' % (n))
		time.sleep(2)
		try:
			browser.find_element_by_xpath("//input[@class='SelectBox PersistEmail-field']").send_keys("%s-%s@mailinator.com" % (randUser, n))
			browser.find_element_by_xpath("//button[contains(text(), 'Sign Up')]").click()
			browser.find_element_by_xpath("//input[@name='firstName']").send_keys("fName")
			browser.find_element_by_xpath("//input[@name='lastName']").send_keys("%s-%s" % (randUser, n))
			browser.find_element_by_xpath("//input[@name='title']").send_keys("Nerf Herder")
			browser.find_element_by_xpath("//input[@name='password']").send_keys("password")
			browser.find_element_by_xpath("//button[contains(text(), 'Continue')]").click()
			browser.implicitly_wait(20)
			time.sleep(10)
			browser.find_element_by_xpath("//div[@id='addeventatc1']").click()
			browser.find_element_by_xpath("//div[@id='addeventatc1']").click()
		except:
			pass
	browser.switch_to.window(browser.window_handles[0])

def teamMemberLoginSelectLeader(email, num_start, num_end, password):
	# open new browser and login via 
	# browser = webdriver.Chrome()
	for memberNum in range(num_start, num_end):
		# browser = webdriver.Chrome()
		print(email,", team number = %s" % memberNum)
		randUser = email.split('@')[0]
		teamMemberEmail = "%s-%s@mailinator.com" % (randUser, memberNum)
		# browser.get("https://weeklyreport.qa.entreleadership.com/sign-in")
		time.sleep(0.5)
		# Sign out of Owner Account
		browser.get("https://weeklyreport.qa.entreleadership.com/sign-out")
		#  sign in to WRT 
		loginWeeklyReport('https://weeklyreport.qa.entreleadership.com', teamMemberEmail, 'password')
		browser.implicitly_wait(15)
		time.sleep(8)

		# Select a leader
		browser.find_element_by_xpath("//div[@style='cursor: pointer; height: 100%; position: relative; width: 100%;']").click()
		time.sleep(1)
		if memberNum == 0:
			browser.find_element_by_xpath("//span[@name='testFirstName %s']" % randUser).click()
		elif memberNum == 1:
			browser.find_element_by_xpath("//span[@name='fName %s-0']" % randUser).click()
		elif memberNum == 2:
			browser.find_element_by_xpath("//span[@name='fName %s-1']" % randUser).click()
		elif memberNum == 3:
			browser.find_element_by_xpath("//span[@name='fName %s-1']" % randUser).click()
			time.sleep(0.5 )
			browser.find_element_by_xpath("//span[@name='fName %s-0']" % randUser).click()
		elif memberNum > 3:
			browser.find_element_by_xpath("//span[@name='fName %s-1']" % randUser).click()
		
		browser.find_element_by_xpath("//div[@style='position: fixed; top: 0px; bottom: 0px; left: 0px; right: 0px; z-index: 2000;']").click()
		time.sleep(2)
		browser.find_element_by_xpath("//button[contains(text(), 'Continue')]").click()
		browser.implicitly_wait(15)
		time.sleep(9)
		# fill out WRT weekly form Previous Week
		print("signing out")
		browser.find_element_by_xpath("//a[contains(text(), 'sign out')]").click()
		# browser.implicitly_wait(15)
		time.sleep(5)
		print("loggin back in")
		loginWeeklyReport('https://weeklyreport.qa.entreleadership.com', teamMemberEmail, 'password')
		time.sleep(5)
		completeWRTform('previousWeek', memberNum, teamMemberEmail)
		# browser.get("https://weeklyreport.qa.entreleadership.com")
		completeWRTform('currentWeek', memberNum, teamMemberEmail)

def completeWRTform(whichWeek, memberNum, teamMemberEmail):
	# browser = webdriver.Chrome()
	# html = browser.execute_script('return document.documentElement.outerHTML')
	# print("==================================================")
	# html = browser.execute_script('return document.documentElement.outerHTML')
	# soup = bs.BeautifulSoup(html, 'html.parser')
	# print(soup.prettify)
	# print("==================================================")
	# browser.implicitly_wait(15)
	# print("refreshing")
	# loginWeeklyReport('https://weeklyreport.qa.entreleadership.com', teamMemberEmail, 'password')
	# browser.get("https://weeklyreport.qa.entreleadership.com")

	# print("after refreshing")
	browser.implicitly_wait(3)
	time.sleep(1)
	print("browser refresh y'all")
	score = [20,40,60,80,100]
	randScore = random.choice(score)
	if whichWeek == 'previousWeek':
		week = 'previous -%s' % memberNum
		additional = 'nope'
		dateRange = 'previous'
	elif whichWeek == "currentWeek":
		week = 'current -%s' % memberNum
		additional = 'nada'
		dateRange = 'current'

	# print variabels
	print("randScore = %s" % randScore)
	print("whichWeek = %s" % whichWeek)
	# fill out your high for the week
	# time.sleep(3)
	print("go to wrt form page")
	browser.get ("https://weeklyreport.qa.entreleadership.com")
	# browser.find_element_by_name("high").click()
	# browser.find_element_by_name("high").send_keys(week)
	browser.find_element_by_xpath("//textarea[@name='high']").send_keys(week)
	
	# low for the week
	browser.find_element_by_xpath("//textarea[@name='low']").send_keys(week)

	# stress level
	stressElement = browser.find_element_by_xpath("//input[@name='stress'][@value='%s']" % randScore)
	browser.execute_script("arguments[0].click();",stressElement)

	# morale level
	moraleElement = browser.find_element_by_xpath("//input[@name='morale'][@value='%s']" % randScore)
	browser.execute_script("arguments[0].click();",moraleElement)

	# workload level
	workloadElement = browser.find_element_by_xpath("//input[@name='workload'][@value='%s']" % randScore)
	browser.execute_script("arguments[0].click();",workloadElement)

	# Anything Else
	browser.find_element_by_xpath("//textarea[@name='extra']").send_keys(week)

	# select which date range to submit
	browser.find_element_by_xpath("//div[@value='%s']" % dateRange).click()

	# Submit Report
	time.sleep(1)
	browser.find_element_by_xpath("//button[contains(text(), 'Submit Report')]").click()

	

# def submitPreviousWrtReport():
# 	# Do things

# def submitCurrentWrtReport():
# 	# Do things

def randEmailUser():
	env = "qa"
	randUser = "testUser%s" % base_repr(int(time.time()), 36)
	print(randUser)
	randEmail = "%s@mailinator.com" % randUser
	print(randEmail)
	return randEmail


def createNewUserAA_NewOnboarding(url, randUser, randEmail):
	whichEnv = url.split('.')[1]

	# root of domain
	browser.get (url)
	
	# go to allaccess
	browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)

	browser.find_element_by_partial_link_text("Become").click()
	
	# go to sign up page for allaccess
	browser.find_element_by_partial_link_text("Become").click()

	# fill out new All Access member form
	browser.find_element_by_id("user_first_name").send_keys("testFirstName")
	browser.find_element_by_id("user_last_name").send_keys("%s" % randUser)
	browser.find_element_by_id("user_email").send_keys(randEmail)
	browser.find_element_by_id("user_phone_number").send_keys("6155551234")
	browser.find_element_by_id("user_company_name").send_keys("summit test")
	browser.find_element_by_name("password").send_keys("password")
	browser.find_element_by_id("user_agreed_to_tos").click() # agree to terms checkbox
	# browser.implicitly_wait(30)
	# time.sleep(3)
	browser.find_element_by_name("commit").click() # submit create new user

	if whichEnv == 'qa':
		print("TestEnv = %s" % whichEnv)
		# apply discount code before entering payment https://www.qa.entreleadership.com/pay
		browser.find_element_by_id("coupon_code").send_keys("321") # enter discount code value
		browser.find_element_by_id("coupon_submit").click() # apply discount code
		browser.find_element_by_xpath("//input[@value='Next Page']").click() # submit
	else:
		print("TestEnv = %s \nskipping discount code test" % whichEnv)
		browser.implicitly_wait(5)
		time.sleep(5)   # delays for 5 seconds. You can Also Use Float Value.
		browser.find_element_by_xpath("//input[@value='Next Page']").click() # submit
	

	
	# payment page
	iframe = browser.find_element_by_id("z_hppm_iframe")
	browser.switch_to.frame(iframe)
	browser.find_element_by_id("input-creditCardNumber").send_keys("5454545454545454")
	select_dropdown_value('input-creditCardExpirationMonth', '03')
	select_dropdown_value('input-creditCardExpirationYear', '2037')
	browser.find_element_by_id("input-cardSecurityCode").send_keys("989")
	select_dropdown_value('input-creditCardState', 'Tennessee')
	browser.find_element_by_id("input-creditCardAddress1").send_keys("123 Test Dr")
	browser.find_element_by_id("input-creditCardCity").send_keys("Nashville")
	browser.find_element_by_id("input-creditCardPostalCode").send_keys("37214")
	browser.find_element_by_id("submitButton").click()

	# initial user login
	browser.implicitly_wait(35)
	browser.find_element_by_name("email").send_keys(randEmail)
	browser.find_element_by_name("password").send_keys("password")
	browser.find_element_by_name("commit").click()

def getstartedURL():
	browser.find_element_by_link_text("Get Started Now").click()


def newUserTestNewOnboarding(env, email, pwd, start_num, end_num):
	randUser = email.split('@')[0]
	createNewUserAA_NewOnboarding("https://www.%s.entreleadership.com" % (env), randUser, email)
	getstartedURL()
	newDashBoardOnboardingSteps(env)
	inviteWrtTeamMembers(email, start_num, end_num)
	onbpardFB()
	teamMemberLoginSelectLeader(email, start_num, end_num, "password")


def loginAndTestNewOnboarding(env, email, pwd, num_users_to_create):
	loginEntre("https://www.%s.entreleadership.com" % (env), email, pwd)
	time.sleep(2)
	newDashBoardOnboardingSteps(env)
	inviteWrtTeamMembers(email, num_users_to_create)
	onbpardFB()

# =====================================================================


#========================================== main =================================

# loginWeeklyReport("https://weeklyreport.entreleadership.com", getUsername("./creds.py"), getPwd("./creds.py"))

# loginEntre("https://www.entreleadership.com", getUsername("./creds.py"), getPwd("./creds.py"))

# becomeEntreMember("https://www.entreleadership.com")


# randUser = "genUserBilly%s" % randint(1, 10000)
# randEmail = "%s@mailinator.com" % randUser
# createNewUserAA("https://www.qa.entreleadership.com", randUser, randEmail)


# signUpAAuserForWRT("https://weeklyreport.qa.entreleadership.com/get-started", "testUser4690@mailinator.com", "password" )

# signUpAAuserForWRT("https://weeklyreport.test.entreleadership.com/get-started", "testUser4365@mailinator.com", "password" , False)

# signUpAAuserForWRT("https://weeklyreport.qa.entreleadership.com/get-started", "testUser4067@mailinator.com", "password", False) # testUser8890@mailinator.com

# loginEntre("https://www.qa.entreleadership.com", getUsername("./creds.py"), getPwd("./creds.py"))

# elementExists("https://www.test.entreleadership.com", "by_css_selector", "HeroButter-heading")

# print(getClipboardData())

# Challenge Create new AA user and add 7 team members to his WRT Company
# createNewAAandWRTuser()
# createNewAAonly()
# loginAndTestNewOnboarding("qa", "testuserp8612z@mailinator.com", "password", 1)
# loginAndTestNewOnboarding("qa", "testuserp8612z@mailinator.com", "password", 1)



newUserTestNewOnboarding("qa", randEmailUser(), "password", 0,1)
# teamMemberLoginSelectLeader('testUserP96MPA@mailinator.com', 0, 1, 'password')


# createNewUserAA("https://www.qa.entreleadership.com", 'testACHSummitPayment', 'testACHSummitPayment@mailinator.com')
# testUserP8RUYJ@mailinator.com

# loginWeeklyReport('https://weeklyreport.qa.entreleadership.com', 'testUserP95H8I-0@mailinator.com', 'password')
# time.sleep(3)
# completeWRTform("previousWeek", 0)
# time.sleep(0.5)
# browser.get("https://weeklyreport.qa.entreleadership.com")
# completeWRTform("currentWeek", 0)


# newUserTestNewOnboarding("qa", 'legayusernotonboarded@mailinator.com', "password", 1)

# teamMemberLoginSelectLeader('testUserP8KX4O@mailinator.com', 0, 4, 'password')

# teamMemberLoginSelectLeader('testUserP8IZ7F@mailinator.com', 4, 'password')

# ******   Login and Create new Team Members for Existing Users ****** #
# loginWRT('testUserP8IZ7F@mailinator.com', 'password', 'qa')
# inviteWrtTeamMembers('testUserP8IZ7F@mailinator.com', 2, 4)
# **********************************************************************


# destroy team member test
# loginWeeklyReport("https://weeklyreport.qa.entreleadership.com/sign-in", "genUser9076@mailinator.com", "password")
# Go to "Edit Team" page
# time.sleep(5)
# browser.implicitly_wait(30)
# browser.find_element_by_xpath("//a[contains(text(), 'Weekly Report Tool')]").click()
# time.sleep(1)
# browser.find_element_by_xpath("//a[contains(text(), 'Edit Team')]").click()
# time.sleep(5)
# browser.implicitly_wait(30)
# findTeamMemeber = browser.find_elements_by_xpath("//div[@class='TeamMemberPanel TeamMemberPanel--admin']")
# print("findTeamMemeber = %s" % len(findTeamMemeber))
# findTeamMemeber[5].click()
# browser.find_element_by_xpath("//button[contains(text(), 'Delete')]").click()
# browser.find_element_by_xpath("//button[contains(text(), 'Delete')]").click()



# createUserByCompanyLink("https://weeklyreport.qa.entreleadership.com/sign-up/AQG4mJ-PUWNPPaiE2e7DAi-ZnQKPVwnwRNCyaY5CsZPO7w", 50)

# signUpAAuserForWRT("https://weeklyreport.test.entreleadership.com/get-started", "testUser2689@mailinator.com", "password" , False, False, 7)
