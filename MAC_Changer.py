import argparse
import re
import subprocess


def process_arguments():
    parser = argparse.ArgumentParser(description='Change your MAC address')
    parser.add_argument('interface', help='Interface to change the MAC address of')
    parser.add_argument('mac', help='MAC address to change your MAC to')

    try:
        return list(vars(parser.parse_args()).values())
    except IOError:
        parser.error('Error')


def change_mac(args):
    subprocess.run(['sudo', 'ifconfig', args[0], 'down'])
    subprocess.run(['sudo', 'ifconfig', args[0], 'hw', 'ether', args[1]])
    subprocess.run(['sudo', 'ifconfig', args[0], 'up'])


def get_mac(args):
    ifconfig_result = str(subprocess.check_output(['ifconfig', args[0]]), 'utf-8')
    mac_address = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result)

    if mac_address:
        return mac_address.group(0)
    else:
        print('Could not find original MAC address')


def check_arguments(args):
    check_interface = subprocess.Popen(['ifconfig', args[0]], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    check_interface.communicate()

    if check_interface.returncode != 0:
        print('Interface is invalid')
        return False
    else:
        check_mac = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', args[1])

        if not check_mac:
            print('MAC Address is invalid')
            return False

    return True


arguments = process_arguments()

if check_arguments(arguments) is True:
    original_mac = get_mac(arguments)
    change_mac(arguments)
    current_mac = get_mac(arguments)

    if current_mac == arguments[1]:
        print('Changed MAC address on', arguments[0], 'from', original_mac, 'to', current_mac)
    else:
        print('Unknown error!')
