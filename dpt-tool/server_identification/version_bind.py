import dns.resolver
import dns.message
import dns.query
import sys
sys.path.append('..')
from utils import pydig, edns_opt_dict

def get_version_bind(server):
    response = pydig(["@" + server, "version.bind", "TXT", "CH"])
    if response.rcode != 0:
        return "RCODE=" + str(response.rcode_name)
    # print(response.section['ANSWER'].rrname)
    if 'ANSWER' not in response.section or \
        response.section['ANSWER'].rrname != "version.bind.":
        return "NO version.bind info"
    return response.section['ANSWER'].rdata[1:-1]

# print(get_version_bind("80.82.117.140"))