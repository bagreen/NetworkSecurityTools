import requests

def checkSubdirectories(url):
    foundURLs = []

    with open("common.txt", "r") as ifile:
        for line in ifile:
            line = line.rstrip()
            subURL = url + '/' + line
            #print("testing " + subURL)

            webRequest = requests.get(subURL)

            if webRequest.status_code < 400:
                print("FOUND " + subURL)
                foundURLs.append(subURL)

    for subURL in foundURLs:
        checkSubdirectories(subURL)

print("Enter website URL you want to find subdirectories for")
url = input()

checkRequest = requests.get(url)

if checkRequest.status_code > 400:
    print("Website is down or doesn't exist, try again")
else:
    print("Website is up")
    checkSubdirectories(url)

# print("Enter wordlist you want to use: ")
# wordlist = input()
