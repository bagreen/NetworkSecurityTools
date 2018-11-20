import scapy

def scan(ip):
    arpRequest = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst = 'ff:ff:ff:ff:ff:ff')
    arpRequestBroadcast =  broadcast / arpRequest

scan('10.0.2.1/24')
