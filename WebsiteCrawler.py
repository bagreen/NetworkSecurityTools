from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests


def checkWebsite(url):
    checkRequest = requests.get(url)

    if checkRequest.status_code > 400:
        print('Website is down or doesn\'t exist, try again')
        checkWebsite()
    else:
        print('Website is up')
def crawlWebsite(url):
    webRequest = requests.get(url)
    webSoup = BeautifulSoup(webRequest.text, 'html.parser')

    for link in webSoup.findAll('a'):
        link = urljoin(url, link.get('href'))

        if '#' in link:
            link = link.split('#')[0]

        if targetUrl in link and link not in links:
            links.append(link)
            print(link)
            crawlWebsite(link)
def findSubdirectories(url):
    foundURLs = []

    with open('common.txt', 'r') as ifile:
        for line in ifile:
            line = line.rstrip()
            subURL = url + '/' + line
            webRequest = requests.get(subURL)
            print('Testing', subURL)

            if webRequest.status_code < 400:
                print('FOUND ', subURL)
                foundURLs.append(subURL)

    for subURL in foundURLs:
        checkSubdirectories(subURL)

print('Do you want to find subdirectories (s) or crawl website (c)?')
goal = input()

print('Enter website URL')
url = input()

checkWebsite(url)

if goal is 's':
    findSubdirectories(url)

elif goal is 'c':
    targetUrl = url
    links = []

    crawlWebsite(url)
