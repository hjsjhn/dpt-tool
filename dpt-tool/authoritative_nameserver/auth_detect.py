import sys
sys.path.append('..')
from time import sleep
from utils import pydig, edns_opt_dict, dnskey_algo_dict

def get_main_auth(domain):
    """
    Get the main authoritative nameserver for a domain

    Args:
        `domain`: the domain to query

    Returns:
        the IP of main authoritative nameserver for the domain

    Examples:
        `get_main_auth("google.com")`
    """
    response = pydig([domain, "SOA"])

    if response.rcode == 0:
        for answer in response.section['ANSWER'].record:
            if answer.rrtype == "SOA":
                ns1 = answer.rdata.split(" ")[0]
                return ns1
    return None

def get_backup_auth(domain):
    """
    Get the backup authoritative nameserver for a domain

    Args:
        `domain`: the domain to query

    Returns:
        the IP of backup authoritative nameserver for the domain

    Examples:
        `get_backup_auth("google.com")`
    """
    main_auth = get_main_auth(domain)
    if main_auth is None:
        return None
    response = pydig([domain, "NS"])

    ret = []
    if response.rcode == 0:
        for answer in response.section['ANSWER'].record:
            if answer.rrtype == "NS":
                ns2 = answer.rdata.split(" ")[0]
                if ns2 != main_auth:
                    ret.append(ns2)
    return ret
