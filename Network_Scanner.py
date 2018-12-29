from scapy.layers.inet import ARP, Ether, IP, sr, sr1, srp, TCP
import argparse
import network_data
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_arguments():
    parser = argparse.ArgumentParser(description='Code that can either scan your network for devices on it, or scan a computer for open ports')
    parser.add_argument('-ip', help='IP of computer\'s port/s you want to scan, or the network that you want to scan')
    parser.add_argument('-p', '--ports', help='Range of ports to scan, two ports should be specified. If you would just like to scan one port, type it in twice', nargs=2, type=int)
    parser.add_argument('-range', help='Target range of IP if you are scanning the network')

    try:
        return parser.parse_args()
    except IOError:
        parser.error('Error')


def network_scan(ip):
    answered_list = srp(Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=ip), timeout=1, verbose=False)[0]

    clients_list = []

    if len(answered_list) > 0:
        answered_list.sort(key=lambda value: value[1].psrc)
        answered_list.sort(key=lambda value: len(value[1].psrc))

        print('Found these devices on', ip, '\n------------------------------------------')
        for answer in answered_list:
            print(answer[1].psrc, '\t\t', answer[1].hwsrc)
            client = {'ip': answer[1].psrc, 'mac': answer[1].hwsrc}
            clients_list.append(client)

    else:
        print('No devices were found on your network')

    return clients_list


def ports_scan(ip, min_port, max_port):
    ports_list = []


    # with ThreadPoolExecutor as executor:
    #     for
    #     future = executor.submit(port_scan, ip, port)
    for port in range(min_port, max_port):
        response = port_scan(ip, port)

        if response:
            ports_list.append(port)

    if len(ports_list) > 0:
        if len(ports_list) > 1:
            ports_list.sort()

            print('Ports open on', ip, '\n------------------------------')
            for port in ports_list:
                print(port)

        else:
            print('Port open on', ip, '\n-----------------------------')
            print(ports_list[0])

    else:
        if min_port < max_port:
            print('There are no ports open on', ip, 'between port', min_port, 'and', max_port)
        else:
            print('Port', min_port, 'on', ip, 'is not up')
# def ports_scan(ip, min_port, max_port):
#     ports_list = []
#
#     for port in range(min_port, max_port):
#         response = port_scan(ip, port)
#
#         if response:
#             ports_list.append(port)
#
#     if len(ports_list) > 0:
#         if len(ports_list) > 1:
#             ports_list.sort()
#             ports_list.sort(key=lambda value: len(value))
#
#             print('Ports open on', ip, '\n------------------------------------------')
#             for port in ports_list:
#                 print(port)
#
#         else:
#             print('Port open on', ip, '\n------------------------------------------')
#             print(ports_list[0])
#
#     else:
#         if min_port < max_port:
#             print('There are no ports open on', ip, 'between port', min_port, 'and', max_port)
#         else:
#             print('Port', min_port, 'on', ip, 'is not up')


def port_scan(ip, port):
    try:
        packet_flags = sr1(IP(dst=ip) / TCP(dport=port, flags='S'), timeout=2, verbose=False).getlayer(TCP).flags
    except AttributeError:
        return False

    if packet_flags == 0x12:
        return True
    else:
        return False


def main():
    arguments = process_arguments()

    if arguments.ip is not None and arguments.ports is not None and arguments.range is None:
        ports_scan(arguments.ip, arguments.ports[0], arguments.ports[1])

    else:
        if arguments.range is None:
            ip = network_data.get_ip('wlp3s0')
            network_scan(ip + '/24')

        else:
            network_scan(arguments.ip + arguments.range)

    exit()

if __name__ == '__main__':
    main()
