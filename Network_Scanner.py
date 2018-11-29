from scapy.layers.inet import ARP, arping, Ether, IP, sr, srp, TCP
from scapy import all
import argparse

def process_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-range', help='Target IP/Range')
    parser.add_argument('-ip', help='IP of computer\'s ports you want to scan')
    parser.add_argument('-p', '--port', help='Ports to scan, defaults to 1-1024, you can also specify single ports')

    try:
        return parser.parse_args()
    except IOError:
        parser.error('Error')


def network_scan(ip):
    answered_list = srp(Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=ip), timeout=1)[0]

    clients_list = []

    if len(answered_list) > 0:
        print('IP\t\t\tMAC Address\n-----------------------------------------')
        for answer in answered_list:
            client_dictionary = {'ip': answer[1].psrc, 'mac': answer[1].hwsrc}
            print('ip:', answer[1].psrc, '\t\t\t', 'mac:', answer[1].hwsrc)
            clients_list.append(client_dictionary)
        return clients_list


def port_scan(ip, ports):
    port_scan_from = ''
    port_scan_to = ''

    if ports is None:
        port_scan_from = '1'
        port_scan_to = '1024'
    elif '-' not in ports:
        port_scan_from = ports
        port_scan_to = ports
    else:
        port_scan_from = ports.split('-')[0]
        port_scan_to = ports.split('-')[1]

    answered_list = sr(IP(dst=ip)/TCP(dport=(port_scan_from, port_scan_to), flags='S'))

    for answer in answered_list:
        print(answer)


arguments = process_arguments()

if arguments.range is not None:
    scan_result = network_scan(arguments.ip)

    if scan_result is not None:
        print('Do you want to scan the computers found?')
        inputted = input()

        if inputted is 'y' or 'Y' or 'Yes' or 'yes' or 'YES':
            for machine in scan_result:
                port_scan(machine['ip'], None)

            port_scan(scan_result, None)
elif arguments.ip is not None:
    port_scan(arguments.ip, arguments.port)
