#!/bin/python
# -*- coding: utf-8 -*-

# sudo pip install selenium listparser
# sudo apt-get install phantomjs

import sys
import time
import listparser as lp
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Evaluate CL Arguments and Display Usage Information

if len(sys.argv) < 3:
	print ("Usage: python OPML_to_squeeze.py [Username] [Password] [OPML file to import]")
	sys.exit(0)

# User specific variables
msb_user = sys.argv[1]
msb_pass = sys.argv[2]

# Location of local OPML file to import
opml_path = sys.argv[3]

# mysqueezebox.com URL (the redirect saves us one step)
URL = 'http://mysqueezebox.com/user/login?redirect=user/apps'

# Start Browser and load mysqueezebox.com
dcap = dict(DesiredCapabilities.PHANTOMJS)
driver = webdriver.PhantomJS(desired_capabilities=dcap)
driver.get(URL)

# Login on mysqueezebox.com
print ("Loggin in to mysqueezebox.com")
element = driver.find_element_by_xpath('//*[@id="email"]')
element.send_keys(msb_user)

element = driver.find_element_by_xpath('//*[@id="password"]')
element.send_keys(msb_pass)

element.submit()

# Wait for page to load
time.sleep(1)

# Delete current podcast subscription list
print ("Deleting current subscription list")
# The URL scheme for deleting entries in the list is
# http://mysqueezebox.com/settings/podcasts/delete/[ID]

# Generate list of IDs
podcasts = driver.find_elements_by_xpath('//ol/li')
pod_ids = []
for pod in podcasts:
	pod_ids.append(pod.get_attribute("id").replace("draggable_","",1))

# Send them to /dev/null
for pod in pod_ids:
	# important time delay for server response
	time.sleep(0.5)
	driver.get("http://mysqueezebox.com/settings/podcasts/delete/" + pod)

# Load local OPML file
try:
	opml_file = open(opml_path)
	opml_cont = opml_file.read()
except IOError as e:
	print "I/O error({0}): {1}".format(e.errno, e.strerror)
	sys.exit(1)

pods = lp.parse(opml_cont)

# Create new subscription list, one entry at a time
print ("Creating new subscription list from OPML file")
for feed in pods.feeds:
	element = driver.find_element_by_xpath('//input[@name="url"]')
	element.clear()
	element.send_keys(feed.url)
	driver.find_element_by_xpath('//*[@id="add_button"]').click()
	time.sleep(0.7)
