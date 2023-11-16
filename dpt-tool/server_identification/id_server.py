import dns.resolver
import dns.message
import dns.query
import sys
sys.path.append('..')
from utils import pydig, edns_opt_dict

def get_id_server(server):
    response = pydig(["@" + server, "id.server", "TXT", "CH"])
    if response.rcode != 0:
        return "RCODE=" + str(response.rcode_name)
    # print(response.section['ANSWER'].rrname)
    if 'ANSWER' not in response.section or \
        response.section['ANSWER'].rrname != "id.server.":
        return "NO id.server info"
    return response.section['ANSWER'].rdata[1:-1]

# print(get_id_server("1.1.1.1"))