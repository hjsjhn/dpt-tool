import dns
import sys
sys.path.append('..')
import utils.network_interfaces as network_interfaces
from utils import pydig, edns_opt_dict

def check_ecs(server: str) -> bool:
    """
    Check whether the specified DNS server supports EDNS Client Subnet (ECS)
    extension by sending a DNS query with ECS option to the server and checking

    Args:
        `server`: the DNS server to query

    Returns:
        `True` if the server supports ECS, `False` otherwise

    Examples:
        `check_ecs('8.8.8.8')`
    """
    domain = 'o-o.myaddr.l.google.com'

    response = pydig(["@" + server, domain, "TXT"])

    for ans in response.section["ANSWER"].record:
        if 'client-subnet' in ans.rdata:
            return True
    return False

    # cso = clientsubnetoption.ClientSubnetOption(client_subnet)
    # message = dns.message.make_query(domain, 'A')
    # message.use_edns(options=[cso])
    # r = dns.query.udp(message, server)
    # for options in r.options:
    #     if isinstance(options, ClientSubnetOption):
    #         return True
    # return False

# Example: print(check_ecs('8.8.8.8', 'checkmydns.club'))
# print(check_ecs('8.8.8.8', 'checkmydns.club'))