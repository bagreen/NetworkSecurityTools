from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse
import concurrent.futures
import requests
import subprocess


def process_arguments():
    parser = argparse.ArgumentParser(description='Either do a crawl attack or a subdirectory attack on a website')
    parser.add_argument('url',
                        help='What website you want to target, make sure that you type in the whole address, e.g. \'https://www.whatever.com\'')
    parser.add_argument('attack',
                        help='What type of attack you want to do, either (c) crawl website or (s) find subdirectories')
    parser.add_argument('-v', '--verbose', help='Adds more verbosity', action='store_true')
    parser.add_argument('-r', '--recursive', help='Search the website recursively', action='store_true')

    try:
        return parser.parse_args()
    except IOError:
        parser.error('Error')


def check_website(url):
    web_request = requests.get(url)

    if verbose is True:
        print('Website status code:', web_request.status_code)

    if web_request.status_code > 400:
        return False
    else:
        return True


def crawl_website(url):
    web_request = requests.get(url)
    web_soup = BeautifulSoup(web_request.text, 'html.parser')

    for link in web_soup.findAll('a'):
        link = urljoin(url, link.get('href'))

        if '#' in link:
            link = link.split('#')[0]

        if url in link and link not in links:
            links.append(link)
            print(link)

    if recursive is True:
        for link in links:
            crawl_website(link)


def find_subdirectory(url, sub_url):
    combined_url = url + sub_url
    web_request = requests.get(combined_url)

    testing = 'Testing ' + combined_url

    print(testing, ' '*(100 - len(testing)), end='\r')

    if web_request.status_code < 400:
        print('+', combined_url, ' '*(102 - len(testing)))
        found_sub_urls.append(combined_url)

    return


def find_subdirectories(url):
    if not url.endswith('/'):
        url = url + '/'

    print('---- Checking', url, '----')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(find_subdirectory, url, sub_url.rstrip()): sub_url for sub_url in subdirectories}

    if len(found_sub_urls) is 0:
        print()
        print('Nothing found')
        print()
    else:
        found_sub_urls.sort()

        for found_sub_url in found_sub_urls:
            found_urls.append(found_sub_url)

        if recursive is True:
            recursive_urls = found_sub_urls.copy()
            found_sub_urls.clear()

            for url in recursive_urls:
                print()
                print()
                find_subdirectories(url)


def crawl_and_find_subdirectories(url):
    print('TBD!')


args = process_arguments()

attack_mode = args.attack
target_url = args.url
recursive = args.recursive
verbose = args.verbose

links = []
found_urls = []
found_sub_urls = []
subdirectories = []

if check_website(target_url) is False:
    print('Website is down or doesn\'t exist, try again')
    exit()

print('Website is up!')
print()

if attack_mode in ['C', 'c', 'Crawl', 'crawl', 'CRAWL']:
    crawl_website(target_url)
elif attack_mode in ['S', 's', 'Sub', 'sub', 'SUB', 'Subdirectory', 'subdirectory', 'SUBDIRECTORY']:
    with open('1000MostCommonWebsiteSubdirectories.txt', 'r') as file:
        for line in file:
            subdirectories.append(line.rstrip())

    find_subdirectories(target_url)
elif attack_mode in ['B', 'b', 'BOTH', 'Both', 'both']:
    crawl_and_find_subdirectories(target_url)
else:
    print('Attack type entered is invalid')
    exit()

found_urls = sorted(found_urls, key=lambda s: s.casefold())

extra = False

if len(found_urls) % 2 is 1:
    found_urls.append(' ')
    extra = True

split = len(found_urls) // 2

first_column = found_urls[0:split]
second_column = found_urls[split:]

print()
print()
subprocess.call(['clear'])
print('Found:')

for i in range(0, split):
    print(first_column[i], ' ' * (53 - len(first_column[i])), second_column[i])

if extra:
    del found_urls[-1]
exit()
