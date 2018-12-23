from subprocess import PIPE, run
import network_data
import argparse
from scapy.layers.inet import ARP, arping, Ether, IP, sr, srp, TCP
import nmap
import concurrent.futures


def process_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', help='Scan name of ip address')
    parser.add_argument('-o', help='Scan operating system of ip address')
    parser.add_argument('-s', help='Scans network for computers on it', action='store_true')

    try:
        return parser.parse_args()
    except IOError:
        parser.error('Error')


def scan_network():
    found = []
    ip = network_data.get_ip('wlp3s0') + '/24'
    answered_list = srp(Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=ip), timeout=2)[0]

    if len(answered_list) > 0:
        for answer in answered_list:
            found.append(answer[1].psrc)

    return found


def find_os(ip):
    scanner = nmap.PortScanner()
    scanner.scan(ip, arguments='-O -T5')

    try:
        print(ip, '-', scanner[ip]['osmatch'][0]['name'])
    except IndexError:
        pass
    except KeyError:
        pass


def find_name(ip):
    scanner = nmap.PortScanner()
    scanner.scan(ip, arguments='-T5')

    try:
        print(ip, '-', scanner[ip].hostname())
    except KeyError:
        pass


def port_scan(ip, ports):
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


def main():
    parser = process_arguments()

    if parser.s is True:
        found = scan_network()
        found.sort()
        found.sort(key=len)

        print('\nFound\n---------------')
        for value in found:
            print(value)

        print('Do you now want to find names (n) or find operating systems (o)?')
        entered = input()

        if entered is 'n':
            print('\nName\n---------------')
            for value in found:
                find_name(value)
        elif entered is 'o':
            print('\nOS Top Guess\n---------------')
            for value in found:
                find_os(value)
    elif parser.n is not None:
        print('Name\n---------------')
        find_name(parser.n)
    elif parser.o is not None:
        print('OS Top Guess\n---------------')
        find_os(parser.o)


if __name__ == '__main__':
    main()
