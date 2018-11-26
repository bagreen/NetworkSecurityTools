import argparse, scapy

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest = 'target', help = 'Target IP/Range')
    options = parser.parse_args()
    return options

#def scan(ip):
    # answered, unanswered = srp(Ether(dst = 'ff:ff:ff:ff:ff:ff')/ARP(pdst = ip), timeout = 1)
    #
    # clients = []
    # for response in answered:
    #     clientDictionary = {'ip' : response[1].psrc, 'mac' : response[1].hwsrc}
    #     clients.append(clientDictionary)
    # return clients

options = arguments()
scapy.arping(ip)
# scanResult = scan(options.target)
