import netifaces

class NetworkInterface:
    interface: str
    ip_address: str
    netmask: str

    def __init__(self, interface, addr, netmask):
        self.interface = interface
        self.ip_address = addr
        self.netmask = netmask

def get_network_interfaces() -> [NetworkInterface]:
    interfaces = netifaces.interfaces()
    
    results = []
    for interface in interfaces:
        ifaddrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in ifaddrs:
            ipv4_info = ifaddrs[netifaces.AF_INET][0]
            # print(ipv4_info)
            ip_address = ipv4_info['addr']
            if ip_address == "127.0.0.1":
                continue
            netmask = ipv4_info['netmask']
            results.append(NetworkInterface(interface, ip_address, netmask))
    return results