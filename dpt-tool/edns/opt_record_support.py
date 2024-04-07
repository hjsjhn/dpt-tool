import time
from utils import pydig, edns_opt_dict

MAX_TRIES = 10

def check_dns_opt_record_once(server: str, domain: str = "checkmydns.club") -> bool:
    """
    Make a DNS query to the specified DNS server and check if the response
    contains OPT records

    Args:
        `server`: the DNS server to query

    Returns:
        `True` if the response contains OPT records, `False` otherwise

    Examples:
        `check_dns_opt_record('1.1.1.1', 'checkmydns.club')`
    """
    response = pydig(["@" + server, "+edns", ])
    try:
        ercode = response.section['ADDITIONAL'].optrr.ercode
        return ercode != 0
    except:
        return False
    
def check_dns_opt_record(server: str, domain: str = "checkmydns.club") -> bool:
    """
    Make DNS queries to the specified DNS server and check if the response
    contains OPT records

    Args:
        `server`: the DNS server to query

    Returns:
        - `Yes` if the server supports OPT records always
        - `No` if the server does not support OPT records always
        - `Partial` if the server supports OPT records sometimes

    Examples:
        `check_dns_opt_record('1.1.1.1', 'checkmydns.club')`
    """
    las = None
    ret = None
    for _ in range(MAX_TRIES):
        ret = "Yes" if check_dns_opt_record_once(server, domain) else "No"
        if las is not None and las != ret:
            return "Partial"
        las = ret
        time.sleep(1)
    return ret