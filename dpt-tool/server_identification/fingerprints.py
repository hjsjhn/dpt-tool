import nmap
import requests
import subprocess
from utils import scan_ip_once

def get_http_fingerprint(ip):
    url = f'http://{ip}'
    try:
        response = requests.get(url, timeout=1)
        headers = response.headers
        fingerprint = {
            "status_code": response.status_code,
            "headers": dict(headers),
            "content": response.text[:200]  # 截取前200个字符作为示例
        }
        return fingerprint
    except requests.exceptions.Timeout:
        print("[ERR]Request timed out")
        return False
    except requests.exceptions.RequestException as e:
        print("[ERR]" + str(e))
        return False

def nmap_get_system_fingerprint(ip):
    nm = nmap.PortScanner()
    try:
        nm.scan(ip, arguments='-O')  # -O 参数用于操作系统检测
        if 'osclass' in nm[ip] and len(nm[ip]['osclass']) > 0:
            os_fingerprint = nm[ip]['osclass']
            return (True, os_fingerprint)
        elif 'osmatch' in nm[ip] and len(nm[ip]['osmatch']) > 0:
            os_fingerprint = nm[ip]['osmatch']
            print(os_fingerprint)
            return (True, os_fingerprint)
        else:
            return (False, "No OS information found")
    except Exception as e:
        return (False, str(e))

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

def get_system_fingerprint(ip):
    res_fpdns = probe_fingerprint(ip)
    if res_fpdns[0]:
        return res_fpdns[1]

    res_dnssoftver = scan_ip_once(ip, "build")
    if len(res_dnssoftver) > 0:
        return ','.join(res_dnssoftver)

    res_nmap = nmap_get_system_fingerprint(ip)
    if res_nmap[0]:
        return res_nmap[1]
    else:
        return "No OS information found"


# ip_address = '208.67.222.222'
# http_fingerprint = get_http_fingerprint(ip_address)
# print("HTTP Fingerprint:", http_fingerprint)

# system_fingerprint = get_system_fingerprint(ip_address)
# print("System Fingerprint:", system_fingerprint)