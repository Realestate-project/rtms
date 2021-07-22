from bs4 import BeautifulSoup
from pprint import pprint
import requests
from selenium import webdriver
import time
import urllib.request

browser = webdriver.Chrome('./chromedriver') #크롬 조작.
browser.implicitly_wait(5) #5초를 기다려준다. 셀레니움은 느리기 때문에.

browser.get('https://map.kakao.com/')
browser.find_element_by_id("search.keyword.query").send_keys('서울코인노래방') #아이디 입력
browser.find_element_by_xpath('//*[@id="search.keyword.submit"]').click()








