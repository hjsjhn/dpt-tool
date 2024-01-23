from utils import pydig, edns_opt_dict

def check_dns_opt_record(server: str) -> bool:
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
    response = pydig(["@" + server, "+edns"])
    try:
        ercode = response.section['ADDITIONAL'].optrr.ercode
        return ercode != 0
    except:
        return False