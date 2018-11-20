import subprocess

print('Enter interface, if you don\'t know type unknown')
interface = input()

print('Enter new MAC address')
newMAC = input()

subprocess.call('sudo ifconfig ' + interface + ' down', shell=True)
subprocess.call('sudo ifconfig ' + interface + ' hw ether ' + newMAC, shell=True)
subprocess.call('sudo ifconfig ' + interface + ' up', shell=True)
