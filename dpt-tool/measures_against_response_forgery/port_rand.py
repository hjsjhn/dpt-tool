import sys
sys.path.append('..')
import utils.network_interfaces as network_interfaces
from utils import pydig, edns_opt_dict
from time import sleep
import numpy as np
import requests

REPEAT = 100

def check_port_randomization(server):
    """
    This function checks if the recursive DNS server randomizes the source port of the query sent to the authoritative server
    We consider the server supports port randomization if the port range covers at least 50% of the total available ports and 
    the standard deviation is not less than 10000

    Args:
        `server`: the DNS server to query

    Returns:
        `True` if the server supports 0x20 encoding, `False` otherwise

    Examples:
        `check_port_randomization("8.8.8.8")`
    """

    ports = []
    cnt = REPEAT
    while cnt:
        cnt -= 1
        response = pydig(["@" + server, "a.rdns.dnsmeasurement.com", "TXT"])
        if response.rcode == 0:
            for answer in response.section['ANSWER'].record:
                if answer.rrtype == "TXT":
                    ports.append(int(answer.rdata.split("##")[0].split("#")[-1]))

    port_min = min(ports)
    port_max = max(ports)
    port_range = port_max - port_min

    std_deviation = np.std(ports)

    total_port_range = 65535 - 1024 + 1
    coverage_rate = port_range / total_port_range
    # print(f"端口最小值: {port_min}")
    # print(f"端口最大值: {port_max}")
    # print(f"端口范围: {port_range}")
    # print(f"标准差: {std_deviation:.2f}")
    # print(f"覆盖率: {coverage_rate:.2%}")
    # print(ports)
    return True if coverage_rate >= 0.5 and std_deviation >= 10000 else False
