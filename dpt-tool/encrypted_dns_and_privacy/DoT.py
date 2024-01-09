import dns.resolver
import socket

# NOTE: not accurate now (show `False` for '1.1.1.1' but actually it supports DoT)
def get_dot_info(server_ip, domain = 'checkmydns.club'):
    port = 853
    try:
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [server_ip]
        resolver.port = port
        resolver.use_tcp = True

        result = resolver.query(domain, 'A')
        return f'{server_ip}:{port}' 

    except (dns.exception.Timeout, socket.error) as e:
        return False

# Example: get_dot_info('1.1.1.1', 'example.com')