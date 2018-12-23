from subprocess import PIPE, run
import re


def get_network_data():
    ifconfig = run(['ifconfig'], stdout=PIPE).stdout.decode('utf-8')

    interfaces = {}
    interface = ''
    for line in ifconfig.splitlines():
        words = line.split()

        # blank?
        if len(words) is 0:
            interface = ''

        elif interface is '':
            interface = words[0][:-1]
            interfaces[interface] = {}

        else:
            for i in range(0, len(words), 2):
                try:
                    interfaces[interface][words[i]] = words[i + 1]
                except IndexError:
                    pass

    return interfaces


def get_interfaces_data(part):
    ifconfig = get_network_data()
    data = []

    for interface in ifconfig:
        try:
            data.append(ifconfig[interface][part])
        except KeyError:
            data.append('')

    return data


def get_interface_data(interface, part):
    ifconfig = get_network_data()
    data = ''

    try:
        data = (ifconfig[interface][part])
    except KeyError:
        data = ''
    return data


def get_interfaces():
    ifconfig = get_network_data()
    data = []

    for interface in ifconfig:
        data.append(interface)

    return data


def get_ip(interface):
    return get_interface_data(interface, 'inet')


def get_ips():
    return get_interfaces_data('inet')


def get_mac(interface):
    return get_interface_data(interface, 'ether')


def get_macs():
    return get_interfaces_data('ether')


def test():
    print('Test!')

    test = run(['ifconfig'], stdout=PIPE).stdout.decode('utf-8')

    print(test)
    print()

    regex = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

    matches = regex.findall(test)

    print(matches)
