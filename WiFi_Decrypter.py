import subprocess

#os.system('ls')

subprocess.run('sudo airmon-ng check kill', shell = True)

subprocess.run('sudo airmon-ng', shell = True)

os.system('sudo airmon-ng')

os.system('sudo airmon-ng start wlp3s0')
#
# print('Enter the bssid of the wifi you would like to break')
os.system('sudo airodump-ng wlp3s0mon')

# this keeps running infinitely
# look into using timeout and timeout expired exception to get around this issue
# https://docs.python.org/3.5/library/subprocess.html#frequently-used-arguments
# GOT IT, USE POPEN.WAIT(TIMEOUT=whatever)
print('test')


os.system('sudo NetworkManager') # to start up wifi again as well
#
# bssid = input()
#
# print('Enter the channel')
# channel = input()
#
# print('kick someone off of the network instead?')
# os.system('sudo airodump-ng --bssid ' + bssid + ' -c ' + channel + ' --write ' + bssid + 'wlp3s0mon')
#
