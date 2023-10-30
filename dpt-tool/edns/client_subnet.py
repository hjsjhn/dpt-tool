import dns
import clientsubnetoption
from clientsubnetoption import ClientSubnetOption
import sys
sys.path.append('..')
import utils.network_interfaces as network_interfaces

def check_ecs(server: str, domain: str) -> bool:
    """
    Check whether the specified DNS server supports EDNS Client Subnet (ECS)
    extension by sending a DNS query with ECS option to the server and checking

    Args:
        `server`: the DNS server to query
        `domain`: the domain to query

    Returns:
        `True` if the server supports ECS, `False` otherwise

    Examples:
        `check_ecs('8.8.8.8', 'checkmydns.club')`
    """
    client_subnet = network_interfaces.get_network_interfaces()[0].netmask

    cso = clientsubnetoption.ClientSubnetOption(client_subnet)
    message = dns.message.make_query(domain, 'A')
    message.use_edns(options=[cso])
    r = dns.query.udp(message, server)
    for options in r.options:
        if isinstance(options, ClientSubnetOption):
            return True
    return False

# Example: print(check_ecs('8.8.8.8', 'checkmydns.club'))