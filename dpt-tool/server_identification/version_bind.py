import dns.resolver
import dns.message
import dns.query
import sys
sys.path.append('..')
from utils import pydig, edns_opt_dict

def get_version_bind(server):
    response = pydig(["@" + server, "version.bind", "TXT", "CH"], VERBOSE=2)
    if response.rcode != 0:
        return "RCODE=" + str(response.rcode_name)
    # print(str(response.section['ANSWER'].record[0].rrname))
    try:
        for record in response.section['ANSWER'].record:
            if record.rrname == "version.bind.":
                return record.rdata[1:-1]
    except:
        pass
    return "NO version.bind info"

# print(get_version_bind("80.82.117.140"))