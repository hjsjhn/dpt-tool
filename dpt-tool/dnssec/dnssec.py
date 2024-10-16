import sys
sys.path.append('..')
from time import sleep
from utils import pydig, edns_opt_dict, dnskey_algo_dict

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

    try:
        if "do" in response.section['ADDITIONAL'].optrr.flags:
            return True
        else:
            return False
    except:
        return False

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
    broken_domain = "www.dnssec-failed.org"
    try:
        bad_response = pydig(["@" + server, "+dnssec", broken_domain])
    except:
        bad_response = None

    return response.ad == 1 and (bad_response == None or bad_response.ad == 0)

def check_dnskey_alg(server, alg):
    """
    Args:
        `server`: the DNS server to query
        `alg`: the algorithm to check

    Returns:
        `True` if the server supports the algorithm, `False` otherwise

    Examples:
        `check_dnskey_alg("1.1.1.1", 8)`
    """
    supported_algs = [5, 8, 10, 13, 14]
    if isinstance(alg, str):
        if alg.isdigit():
            alg = int(alg)
        else:
            alg = dnskey_algo_dict[alg]
    elif isinstance(alg, int):
        pass
    else:
        raise TypeError("alg must be int or str")
    if alg not in supported_algs:
        raise ValueError("alg must be one of 5, 8, 10, 13, 14")

    # NOTE: change the domain name and subdomain rules here
    sld = "checkmydns.club"
    subdomain = f"dnskey-alg-{alg}"
    bad_subdomain = f"dnskey-alg-{alg}-f"

    try:
        response = pydig(["@" + server, "+dnssec", '.'.join([subdomain, sld])])
        # print(response.section["ADDITIONAL"].optrr.flags)
        bad_response = pydig(["@" + server, "+dnssec", '.'.join([bad_subdomain, sld])])
        # print(response.section["ADDITIONAL"].optrr.flags, bad_response.section["ADDITIONAL"].optrr.flags)
        if "do" in response.section['ADDITIONAL'].optrr.flags:# and "do" in bad_response.section['ADDITIONAL'].optrr.flags:
            if 0 in response.section['ADDITIONAL'].optrr.ercode and 0 not in bad_response.section['ADDITIONAL'].optrr.ercode:
                return True
    except:
        return False
    return False

def get_dnskey_alg(server):
    """
    Args:
        `server`: the DNS server to query

    Returns:
        a list of supported algorithms

    Examples:
        `get_dnskey_alg("8.8.8.8")`
    """
    supported_algs = [5, 8, 10, 13, 14]
    res = []
    for alg in supported_algs:
        if check_dnskey_alg(server, alg):
            res.append(alg)
        sleep(0.5)
    return res

# print(check_dnskey_alg("1.1.1.1", 8))
# print(check_response_validation("8.8.8.8"))