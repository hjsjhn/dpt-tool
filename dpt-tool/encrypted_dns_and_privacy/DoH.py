import socket
import ssl
import requests
import json
import dns.message
import dns.query
import dns.rdatatype
import base64


def get_certificate_and_domain(ip, port):
    context = ssl.create_default_context()
    with socket.create_connection((ip, port)) as sock:
        with context.wrap_socket(sock, server_hostname=ip) as ssock:
            cert = ssock.getpeercert()
            domains = [san_entry[1] for san_entry in cert.get('subjectAltName', []) if san_entry[0] == 'DNS']
            return cert, domains

def check_doh_support(doh_url, domain):
    headers = [ 'application/dns-json', 'application/dns-message' ]
    query = dns.message.make_query(domain, dns.rdatatype.A)
    wire_data = query.to_wire()
    base64_encoded_data = base64.b64encode(wire_data).decode('utf-8')
    params = { 'dns': base64_encoded_data[:-2], 'name': domain }

    for key, value in params.items():
        for header in headers:
            try:
                response = requests.get(doh_url, headers={'accept': header}, params={key: value}, timeout=(1,2))
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                # print("Error making request:", e)
                continue

            if response.status_code == 200:
                return True
            else:
                # print("Response Error with code: " + response.status_code)
                pass

def get_doh_info(server, query_domain = 'checkmydns.club'):
    """
    Get DNS resolver's DoH url information through server ip. (only for url with suffix '/dns-query')

    NOTE: For some DNS resolver, the DoH url may not be the same as the server ip.
    """
    ip, port = server, 443

    cert, domains = get_certificate_and_domain(ip, port)
    results = []
    for domain in domains:
        if "*." in domain:
            domains.append(domain[2:])
            domain = "dns." + domain[2:]
    domains = list(set(domains))
    # print(domains)
    domains = [domain for domain in domains if "dot" not in domain]
    for domain in domains:
        if "*." in domain:
            continue
        domain = "https://" + domain
        if check_doh_support(domain + '/dns-query', query_domain):
            results.append(domain)
    results = list(set(results))
    return results

# print(get_doh_info("77.88.8.8", "www.baidu.com"))