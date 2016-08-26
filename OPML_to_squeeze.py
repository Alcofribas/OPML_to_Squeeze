#!/bin/python
# -*- coding: utf-8 -*-

# sudo pip install selenium listparser
# sudo apt-get install phantomjs

import time
import listparser as lp
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)

# user specific variables
msb_user = '<USER NAME>'
msb_pass = '<PASSWORD>'

URL = 'http://mysqueezebox.com/user/login?redirect=user/apps'

driver = webdriver.PhantomJS(desired_capabilities=dcap)
# driver = webdriver.Firefox()

driver.get(URL)

driver.save_screenshot('squeeeze.png')

# Anmeldung
# (evtl. gar nicht notwendig)
element = driver.find_element_by_xpath('//*[@id="email"]')
element.send_keys(msb_user)

element = driver.find_element_by_xpath('//*[@id="password"]')
element.send_keys(msb_pass)

element.submit()
# ---

# Kunstpause
time.sleep(1)

# Eintraege löschen

# Zum Löschen eines Eintrages muss folgende URL mit der entsprechenden Nummer aufgerufen werden:
# http://mysqueezebox.com/settings/podcasts/delete/[Nummer]

# Liste der IDs generieren
podcasts = driver.find_elements_by_xpath('//ol/li')
pod_ids = []
for pod in podcasts:
	pod_ids.append(pod.get_attribute("id").replace("draggable_","",1))

# Kontrolle
print pod_ids

# alle löschen
for pod in pod_ids:
	time.sleep(0.5) # Pause, WICHTIG wegen Ladezeit des Browsers
	driver.get("http://mysqueezebox.com/settings/podcasts/delete/" + pod)

# lokale OPML-Datei laden
# TODO: Auswahldialog

opml_path = "/home/oliver/Schreibtisch/antennapod-feeds.opml"
opml_file = open(opml_path)
opml_cont = opml_file.read()
pods = lp.parse(opml_cont)

for feed in pods.feeds:
	element = driver.find_element_by_xpath('//input[@name="url"]')
	element.clear()
	element.send_keys(feed.url)
	driver.find_element_by_xpath('//*[@id="add_button"]').click()
	time.sleep(0.5)

# Squeezebox OPML holen
# opml_link = driver.find_element_by_partial_link_text("OPML").get_attribute("href")
# print opml_link
# opml_file = driver.get(opml_link)
# xPATH to SQL: "select the "href" attribute (@) of an "a" tag that appears anywhere (//), but only where (the bracketed phrase) the textual contents of the "a" tag contain 'Podcasts als OPML'".

# falls der Link statisch ist, kann einfach folgender Ausdruck verwendet werden
# driver.get("http://mysqueezebox.com/public/opml/ecd807dcd498c2ff71d4637c8a0bc3aa546671ec/podcasts.opml")


# loeschen und neu generieren
