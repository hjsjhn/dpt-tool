import uuid
import sys
sys.path.append('..')
import utils.network_interfaces as network_interfaces
from utils import pydig, edns_opt_dict
from time import sleep
import requests

def check_0x20_encoding(server, sld='checkmydns.club', auth_server='108.61.171.88:88'):
    """
    Args:
        `server`: the DNS server to query
        `sld`: the second level domain to check
        `auth_server`: the authoritative server for the domain

    Returns:
        `True` if the server supports 0x20 encoding, `False` otherwise

    Examples:
        `check_0x20_encoding("8.8.8.8", "checkmydns.club", "108.61.171.88")`
    """
    uuid_str = str(uuid.uuid4())
    response = pydig(["@" + server, f"{uuid_str}.{sld}"])
    sleep(1)
    max_try = 3
    while max_try > 0:
        sleep(1)
        try:
            url = f"http://{auth_server}/data/{uuid_str}"
            response = requests.get(url, timeout=(1,2))
            if response.status_code == 200:
                # get the json content from response
                content = response.json()
                if content["uuid"] == uuid_str:
                    return True if content["0x20"] else False
                break
            else:
                max_try -= 1
        except:
            max_try -= 1
    return False

# print(check_0x20_encoding("8.8.8.8", "checkmydns.club", "108.61.171.88:88"))