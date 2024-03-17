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
    try:
        for record in response.section['ANSWER'].record:
            if record.rrname == "id.server.":
                return record.rdata[1:-1]
    except:
        pass
    return "NO id.server info"

# print(get_id_server("1.1.1.1"))