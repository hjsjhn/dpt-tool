import dns.resolver
import socket

# NOTE: not accurate now (show `False` for '1.1.1.1' but actually it supports DoT)
def check_tls_support(server_ip, domain):
    port = 853
    try:
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [server_ip]
        resolver.port = port
        resolver.use_tcp = True

        result = resolver.query(domain, 'A')
        return True

    except (dns.exception.Timeout, socket.error) as e:
        return False

# Example: check_tls_support('1.1.1.1', 'example.com')