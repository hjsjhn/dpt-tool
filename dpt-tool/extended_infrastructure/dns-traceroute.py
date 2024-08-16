import argparse
from scapy.all import *
import time
import json

DEFAULT_MAX_HOPS = 32

def dns_traceroute(dest, qname, qtype, timeout):
    result = {}
    for i in range(1, DEFAULT_MAX_HOPS + 1):
        sport_list = [random.randint(1, 65535) for _ in range(3)]
        pre_strs = ["{}".format(i).ljust(5, " ") if _ == 0 else "".ljust(5, " ") for _ in range(3)]
        route_ips = []
        cost_times = []
        for repeat in range(3):
            p = IP(dst=dest, ttl=i) / UDP(sport=sport_list[repeat], dport=53) / DNS(rd=1, qd=DNSQR(qname=qname,
                                                                                                        qtype=qtype))
            start_time = time.time()
            answer = sr1(p, timeout=timeout, verbose=False)
            end_time = time.time()
            route_ips.append(answer.src if answer is not None else None)
            cost_times.append(end_time - start_time)
        for repeat in range(3):
            result.setdefault(i, []).append({"ip": route_ips[repeat], "time": cost_times[repeat] * 1000})
            print("{} {} {:.5f}ms ".format(pre_strs[repeat], route_ips[repeat], cost_times[repeat] * 1000))
        if dest in route_ips:
            break

    return json.dumps(result)
