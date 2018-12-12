from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse
import concurrent.futures
import requests


def process_arguments():
    parser = argparse.ArgumentParser(description='Either do a crawl attack or a subdirectory attack on a website')
    parser.add_argument('attack',
                        help='What type of attack you want to do, either (c) crawl website or (s) find subdirectories')
    parser.add_argument('url',
                        help='What website you want to target, make sure that you type in the whole address, e.g. \'https://www.whatever.com\'')
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

        if args[1] in link and link not in links:
            links.append(link)
            print(link)
            crawl_website(link)


def find_subdirectory(base_url, sub_url):
    combined_url = base_url + sub_url
    web_request = requests.get(combined_url)

    if verbose is True:
        print('Testing ' + combined_url)

    if web_request.status_code < 400:
        print('FOUND', combined_url)
        found_urls.append(combined_url)


def find_subdirectories(base_url):
    if not base_url.endswith('/'):
        base_url = base_url + '/'

    print('Checking', base_url)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(find_subdirectory, base_url, url.rstrip()): url for url in subdirectories}

    if len(found_urls) is 0:
        print('Nothing found')
        print()
    else:
        print()
        print('Found:')
        found_urls.sort()
        for found_url in found_urls:
            print(found_url)

        if recursive is True:
            base_urls = found_urls.copy()
            found_urls.clear()

            for base_url in base_urls:
                print()
                print()
                find_subdirectories(base_url)


args = process_arguments()

target_url = args.url

recursive = args.recursive

verbose = args.verbose

subdirectories = []

crawl_attack_names = ['C', 'c', 'Crawl', 'crawl', 'CRAWL']
subdirectory_attack_names = ['S', 's', 'Sub', 'sub', 'SUB', 'Subdirectory', 'subdirectory', 'SUBDIRECTORY']

if check_website(target_url) is False:
    print('Website is down or doesn\'t exist, try again')
    exit()

print('Website is up!')
print()

if args.attack in crawl_attack_names:
    links = []
    crawl_website(target_url)
    exit()
elif args.attack in subdirectory_attack_names:
    found_urls = []
    subdirectories = []

    with open('1000MostCommonWebsiteSubdirectories.txt', 'r') as file:
        for line in file:
            subdirectories.append(line.rstrip())

    find_subdirectories(target_url)
    print()
    print('DONE!')
    exit()
else:
    print('Attack type entered is invalid')
    exit()
