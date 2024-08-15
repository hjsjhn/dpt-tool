import sys
sys.path.append('..')
from utils import pydig, edns_opt_dict
from time import sleep
import numpy as np

def check_ipv6_support(server):
    """
    Check if the sever support requests over IPv6

    Args:
        `server`: the DNS server to query

    Returns:
        `True` if the server supports IPv6, `False` otherwise

    Examples:
        `check_ipv6_support("8.8.8.8")`
    """

    response = pydig(["@" + server, "xn--vcs521a757aozf.top"])
    if response.rcode == 0:
        for answer in response.section['ANSWER'].record:
            if answer.rrtype == "A":
                return True
    return False