import argparse
import re
import subprocess


def process_arguments():
    parser = argparse.ArgumentParser(description='Change your MAC address')
    parser.add_argument('interface')
    parser.add_argument('mac')

    parsed = parser.parse_args()

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


arg_results = process_arguments()

original_mac = get_mac(arg_results)
change_mac(arg_results)
current_mac = get_mac(arg_results)

if current_mac == arg_results[1]:
    print('Changed MAC address on', arg_results[0], 'from', original_mac, 'to', current_mac)
else:
    print('Unknown error!')
