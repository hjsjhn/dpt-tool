import dns.message
import dns.query

"""
    To get default payload size to authoritative,
    you need to query the domain you own using the target public DNS resolver and 
    fetch data from your authoritative server.

    Example:
        Using command `tcpdump -i enp1s0 -s 0 -w test.pcap` on authoritative server, 
        and send DNS query using the target public DNS resolver.
        Then open `test.pcap` and filter out the DNS query packet from the target public DNS resolver 
        to see default UDP payload size to authoritative.
"""

def check_dns_udp_payload_size(stub_server: str, domain: str = 'checkmydns.club') -> int:
    """
    Make a DNS query to the specified DNS server and check the UDP payload size

    Args:
        `stub_server`: the stub server to query
        `domain`: the domain to query (careful with the domain, it may be a CNAME leading to a different UDP payload size)

    Returns:
        the UDP payload size to stub server (note that the UDP payload size to authoritative server should be obtained from your authoritative server)
    """
    # Create a DNS query message for stub server
    query_stub = dns.message.make_query(domain, dns.rdatatype.ANY)
    query_stub.use_edns(payload=4096)

    # Send the query message to the stub server
    response_stub = dns.query.udp(query_stub, stub_server)

    # Get the UDP payload size from the response for stub server
    udp_payload_size_stub = response_stub.payload

    return int(udp_payload_size_stub)


# Example: print(check_dns_udp_payload_size('1.1.1.1', 'checkmydns.club'))