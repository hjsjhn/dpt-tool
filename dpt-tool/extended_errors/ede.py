import sys
sys.path.append('..')
import numpy as np
import utils.network_interfaces as network_interfaces
from utils import pydig, edns_opt_dict

domain = "extended-dns-errors.com"

subdomain_list = [
    "valid",
    "unsigned",
    "allow-query-none",
    "allow-query-localhost",
    "no-ds",
    "ds-bad-tag",
    "ds-bad-key-algo",
    "ds-unassigned-key-algo",
    "ds-reserved-key-algo",
    "ds-unassigned-digest-algo",
    "ds-bogus-digest-value",
    "rrsig-exp-all",
    "rrsig-exp-a",
    "rrsig-not-yet-all",
    "rrsig-not-yet-a",
    "rrsig-exp-before-all",
    "rrsig-exp-before-a",
    "rrsig-no-all",
    "rrsig-no-a",
    "no-rrsig-ksk",
    "no-rrsig-dnskey",
    "bad-nsec3-hash",
    "bad-nsec3-next",
    "bad-nsec3param-salt",
    "bad-nsec3-rrsig",
    "nsec3-missing",
    "nsec3-rrsig-missing",
    "nsec3param-missing",
    "no-nsec3param-nsec3",
    "no-zsk",
    "bad-zsk",
    "no-ksk",
    "bad-rrsig-ksk",
    "bad-ksk",
    "bad-rrsig-dnskey",
    "no-dnskey-256",
    "no-dnskey-257",
    "no-dnskey-256-257",
    "bad-zsk-algo",
    "unassigned-zsk-algo",
    "reserved-zsk-algo",
    "ed448",
    "v6-mapped",
    "v6-unspecified",
    "v4-hex",
    "v6-link-local",
    "v6-localhost",
    "v6-mapped-dep",
    "v6-doc",
    "v6-unique-local",
    "v6-nat64",
    "v6-multicast",
    "v4-private-10",
    "v4-private-172",
    "v4-private-192",
    "v4-this-host",
    "v4-loopback",
    "v4-link-local",
    "v4-doc",
    "v4-reserved",
    "dsa",
    "nsec3-iter-200",
    "rsamd5",
]

def get_ede_support_list(server: str) -> list:
    """
    Get the EDNS Extended Errors (EDE) support list of specified DNS server 

    Args:
        `server`: the DNS server to query
    """
    res = []
    # take 10 subdomains randomly to query
    new_subdomain_list = np.random.choice(subdomain_list, 10, replace=False)
    for subdomain in new_subdomain_list:
        threshold = 3
        while threshold > 0:
            try:
                response = pydig(["@" + server, "+dnssec", f"{subdomain}.{domain}"])
                break
            except:
                threshold -= 1 
        if threshold == 0:
            continue
        try:
            options = response.section['ADDITIONAL'].optrr.options
            if edns_opt_dict["EDE"] in options:
                res.append(options[edns_opt_dict["EDE"]].data["info_code"])
        except:
            pass
    res = list(set(res))
    return res

def get_ede_support_category(server: str) -> list:
    """
    Get the EDNS Extended Errors (EDE) support category of specified DNS server 

    Args:
        `server`: the DNS server to query
    """
    res = {
        "DNSSEC": [1, 2, 5, 6, 7, 8, 9, 10, 11, 12],
        "Local Policy": [4, 15, 16, 17, 18],
        "Caching": [3, 13, 19],
        "Others": [14, 20, 21, 22, 23, 24]
    }
    val = get_ede_support_list(server)
    for key in res:
        res[key] = list(set(res[key]) & set(val))
    return res

# print(get_ede_support_category("1.1.1.1"))