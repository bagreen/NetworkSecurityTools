from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse
import requests


def process_arguments():
    parser = argparse.ArgumentParser(description='Either do a crawl attack or a subdirectory attack on a website')
    parser.add_argument('attack',
                        help='What type of attack you want to do, either (c) crawl website or (s) find subdirectories')
    parser.add_argument('url',
                        help='What website you want to target, make sure that you type in the whole address, e.g. \'https://www.whatever.com\'')
    parser.add_argument('-v', '--verbose', help='Adds more verbosity', action='store_true')

    try:
        return list(vars(parser.parse_args()).values())
    except IOError:
        parser.error('Error')


def check_website(url, verbosity):
    web_request = requests.get(url)

    if verbosity is True:
        print('Website status code:', web_request.status_code)

    if web_request.status_code > 400:
        print('Website is down or doesn\'t exist, try again')
        return False
    else:
        print('Website is up!')
        return True


def crawl_website(url):
    web_request = requests.get(url)
    web_soup = BeautifulSoup(web_request.text, 'html.parser')

    for link in web_soup.findAll('a'):
        link = urljoin(url, link.get('href'))

        if '#' in link:
            link = link.split('#')[0]

        if args[1] in link and link not in links:
            links.append(link)
            print(link)
            crawl_website(link)


def find_subdirectories(url, verbosity):
    print('Finding subdirectories for', url)
    found_urls = []

    with open('1000MostCommonWebsiteSubdirectories.txt', 'r') as file:
        for line in file:
            line = line.rstrip()
            sub_url = url + '/' + line
            web_request = requests.get(sub_url)

            if verbosity is True:
                print('Testing', sub_url)

            if web_request.status_code < 400:
                print('FOUND ', sub_url)
                found_urls.append(sub_url)

    print()
    print('Found these subdirectories of', url)
    for found_url in found_urls:
        print(found_url)
    print()

    for sub_url in found_urls:
        find_subdirectories(sub_url, verbosity)


args = process_arguments()

crawl_attack_names = ['C', 'c', 'Crawl', 'crawl', 'CRAWL']
subdirectory_attack_names = ['S', 's', 'Sub', 'sub', 'SUB', 'Subdirectory', 'subdirectory', 'SUBDIRECTORY']

if check_website(args[1], args[2]) is True:
    if args[0] in crawl_attack_names:
        links = []
        crawl_website(args[1])
    elif args[0] in subdirectory_attack_names:
        find_subdirectories(args[1], args[2])
    else:
        print('Attack type entered is invalid')
