import dns.message
import dns.query

def check_dns_opt_record(server: str, domain: str = "checkmydns.club") -> bool:
    """
    Make a DNS query to the specified DNS server and check if the response
    contains OPT records

    Args:
        `server`: the DNS server to query
        `domain`: the domain to query

    Returns:
        `True` if the response contains OPT records, `False` otherwise

    Examples:
        `check_dns_opt_record('1.1.1.1', 'checkmydns.club')`
    """
    # Create a DNS query message
    query = dns.message.make_query(domain, dns.rdatatype.TXT)
    query.flags |= dns.flags.DO

    # Send the query message to the specified DNS server
    response = dns.query.udp(query, server)

    # Check if the response contains OPT records
    return response.options != []