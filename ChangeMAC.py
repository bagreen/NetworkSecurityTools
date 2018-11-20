import optparse, re, subprocess

def arguments():
    parser = optparse.OptionParser()

    parser.add_option('-i', '--interface', dest = 'interface', help = 'Interface of which the MAC address will be changed')
    parser.add_option('-m', '--mac', dest = 'newMAC', help = 'New MAC address')

    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error('Specify an interface')
    if not options.newMAC:
        parser.error('Specify a MAC address')
def changeMac():
    subprocess.call('sudo ifconfig ' + options.interface + ' down', shell = True)
    subprocess.call('sudo ifconfig ' + options.interface + ' hw ether ' + options.newMAC, shell = True)
    subprocess.call('sudo ifconfig ' + options.interface + ' up', shell = True)
def getMac():
    ifconfigResult = subprocess.check_output(['ifconfig', interface])
    macAddress = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfigResult)

    if macAddress:
        return macAddress.group(0)
    else:
        print('Could not find original MAC address')

arguments()
changeMac()

currentMac = getMac()

if currentMac == options.newMAC:
    print('Changed MAC address on ' + options.interface + ' to ' + options.newMAC)
else:
    print('Unknown error!')
