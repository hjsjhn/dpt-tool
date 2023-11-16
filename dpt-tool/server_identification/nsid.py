"""
    NSID: Name Server Identifier
    NSID is a DNS extension that allows a name server to identify itself
    with a name rather than an IP address.

    NSID is useful for various purposes such as network troubleshooting, 
    performance optimization, and tracking issues.
"""

import dns.resolver
import dns.message
import dns.query
import sys
sys.path.append('..')
from utils import pydig, edns_opt_dict


def check_nsid_support(server):
    response = pydig(["@" + server, "+nsid"])
    # print(edns_opt_dict["NSID"] in response.section['ADDITIONAL'].optrr.options)
    return edns_opt_dict["NSID"] in response.section['ADDITIONAL'].optrr.options


# print(check_nsid_support("8.8.8.8"))
