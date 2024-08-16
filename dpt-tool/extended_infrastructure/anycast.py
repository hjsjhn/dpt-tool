from scapy.all import *
import time
import json
import requests
import geoip2.database

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
    # use geoip to get the country of the ip
    current_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        reader = geoip2.database.Reader('/'.join([current_dir, "GeoLite2-Country.mmdb"]))
    except Exception as e:
        print(e)
    try:
        local_country = reader.country(local_last_node).country.name
    except:
        local_country = "Unknown1"
    try:
        remote_country = reader.country(remote_last_node).country.name
    except:
        remote_country = "Unknown2"
    reader.close()
    # print(local_country, remote_country)
    return local_country != remote_country

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
    url = "http://47.251.4.152"
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
        response = requests.get(url, params=params, timeout=60)
    except requests.exceptions.Timeout:
        return "Remote traceroute takes too long"
    except:
        return "Remote traceroute request failed"

    if response.status_code == 200:
        try:
            trace_remote = response.json()
            if check_trace(trace_local, trace_remote):
                return True
            else:
                return False
        except Exception as e:
            return False