import sys
sys.path.append('..')
import utils.network_interfaces as network_interfaces
from utils import pydig, edns_opt_dict
from time import sleep
import requests

def check_0x20_encoding(server, domain='encoding20.checkmydns.club', specific_ip="127.0.0.1"):
    """
    This function checks if the DNS server supports 0x20 encoding by querying the specific domain
    Note that this function need support from the AuthDNS encoding20 plugin
    Check if the specific IP is returned in the response to determine if the server supports 0x20 encoding
    Args:
        `server`: the DNS server to query
        `domain`: the specific domain for encoding20 plugin
        `specific_ip`: the specific IP set in AuthDNS encoding20 plugin

    Returns:
        `True` if the server supports 0x20 encoding, `False` otherwise

    Examples:
        `check_0x20_encoding("8.8.8.8", "encoding20.checkmydns.club", "127.0.0.1")
    """
    response = pydig(["@" + server, domain, "A"])
    if response.rcode == 0:
        for answer in response.section['ANSWER'].record:
            if answer.rrtype == "A" and answer.rdata == specific_ip:
                return True
    return False

# print(check_0x20_encoding("8.8.8.8", "encoding20.checkmydns.club", "127.0.0.1"))