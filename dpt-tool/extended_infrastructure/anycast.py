from scapy.all import *
import time
import json
import requests

import ipaddress

def are_ips_in_same_subnet(ip1, ip2):
    netmask = 24
    network1 = ipaddress.ip_network(f'{ip1}/{netmask}', strict=False)
    network2 = ipaddress.ip_network(f'{ip2}/{netmask}', strict=False)
    return network1.network_address == network2.network_address

DEFAULT_MAX_HOPS = 32

def dns_traceroute(dest, qname, qtype = "A", dnsport = 53, timeout = 5):
    result = {"trace": []}
    for i in range(1, DEFAULT_MAX_HOPS + 1):
        sport_list = [random.randint(1, 65535) for _ in range(3)]
        pre_strs = ["{}".format(i).ljust(5, " ") if _ == 0 else "".ljust(5, " ") for _ in range(3)]
        route_ips = []
        cost_times = []
        result["trace"].append([])
        for repeat in range(3):
            p = IP(dst=dest, ttl=i) / UDP(sport=sport_list[repeat], dport=53) / DNS(rd=1, qd=DNSQR(qname=qname,
                                                                                                        qtype=qtype))
            start_time = time.time()
            answer = sr1(p, timeout=timeout, verbose=False)
            end_time = time.time()
            route_ips.append(answer.src if answer is not None else None)
            cost_times.append(end_time - start_time)
        for repeat in range(3):
            result["trace"][i-1].append({"ip": route_ips[repeat], "time": cost_times[repeat] * 1000})
            # print("{} {} {:.5f}ms ".format(pre_strs[repeat], route_ips[repeat], cost_times[repeat] * 1000))
        if dest in route_ips:
            break

    return result

def check_trace(trace_local, trace_remote):
    local_last_node, remote_last_node = None, None
    for i in range(len(trace_local["trace"]) - 1):
        for repeat in range(3):
            if trace_local["trace"][i][repeat]["ip"] is not None:
                local_last_node = trace_local["trace"][i][0]["ip"]
                break
    for i in range(len(trace_remote["trace"]) - 1):
        for repeat in range(3):
            if trace_remote["trace"][i][repeat]["ip"] is not None:
                remote_last_node = trace_remote["trace"][i][0]["ip"]
                break
    # print(local_last_node, remote_last_node)
    return not are_ips_in_same_subnet(local_last_node, remote_last_node)

def check_anycast(server, qname = "baidu.com"):
    """
    Check if the sever supports DNS anycast 

    Args:
        `server`: the DNS server to query

    Returns:
        `True` if the server supports DNS anycast, `False` otherwise

    Examples:
        `check_anycast("8.8.8.8")`
    """
    # print(server)
    url = "http://60.205.184.92"
    params = {
        'dest': server,
        'qname': qname,
    }

    try:
        trace_local = dns_traceroute(server, qname)
    except Exception as e:
        print(e)
        return False
    # print(trace_local)

    try:
        response = requests.get(url, params=params, timeout=120)
    except requests.exceptions.Timeout:
        print("[ERR] Remote traceroute takes too long")
        return False
    except:
        print("[ERR]Remote traceroute request failed")
        return False

    if response.status_code == 200:
        try:
            trace_remote = response.json()
            if check_trace(trace_local, trace_remote):
                return True
            else:
                return False
        except Exception as e:
            return False