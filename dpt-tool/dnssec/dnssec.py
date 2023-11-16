import sys
sys.path.append('..')
import utils.network_interfaces as network_interfaces
from utils import pydig, edns_opt_dict

def check_do_bit(server):
    """
    In DNSSEC (Domain Name System Security Extensions), the DO (DNSSEC OK) bit is a part of the DNS message header. 
    It is used to indicate that the sender of the DNS query Request supports DNSSEC and desires to receive DNSSEC-protected responses.

    Args:
        `server`: the DNS server to query

    Returns:
        `True` if the server supports DO, `False` otherwise

    Examples:
        `check_do_bit("8.8.8.8")`
    """
    response = pydig(["@" + server, "+dnssec"])

    return "do" in response.section['ADDITIONAL'].optrr.flags

def check_response_validation(server):
    """
    Args:
        `server`: the DNS server to query

    Returns:
        `True` if the server supports response validation, `False` otherwise

    Examples:
        `check_response_validation("8.8.8.8")`
    """
    response = pydig(["@" + server, "+dnssec"])

    return response.ad == 1

# print(check_response_validation("8.8.8.8"))