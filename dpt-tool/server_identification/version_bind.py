import dns.resolver
import dns.message
import dns.query
import subprocess
import sys
sys.path.append('..')
from utils import pydig, edns_opt_dict, scan_ip_once

def probe_fingerprint(ip_address):
    try:
        # 调用 fpdns 命令
        result = subprocess.run(['fpdns', '-s', ip_address], capture_output=True, text=True)
        
        # 检查命令是否成功执行
        if result.returncode == 0:
            return (True, result.stdout.split(ip_address)[1].strip().lstrip())
        else:
            return (False, f"Error occurred: {result.stderr}")
    except Exception as e:
        return (False, f"Failed to run fpdns: {e}")

def get_version_bind(server):
    res_fpdns = probe_fingerprint(server)
    if res_fpdns[0]:
        return res_fpdns[1]

    res_dnssoftver = scan_ip_once(server, "build")
    if len(res_dnssoftver) > 0:
        return ','.join(res_dnssoftver)

    response = pydig(["@" + server, "version.bind", "TXT", "CH"])
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
