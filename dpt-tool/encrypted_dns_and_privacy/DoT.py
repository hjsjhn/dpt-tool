from utils import pydig

# NOTE: not accurate now (show `False` for '1.1.1.1' but actually it supports DoT)
def get_dot_info(server_ip):
    # using default port 853
    port = 853
    try:
        response = pydig(["@" + server_ip, "+tls=noauth"])
        rcode = response.rcode
        return f'{server_ip}:{port}' if rcode == 0 else False
    except:
        return False

# Example: get_dot_info('1.1.1.1', 'example.com')