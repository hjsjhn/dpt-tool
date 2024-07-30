import nmap
import requests

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
        return "Request timed out"
    except requests.exceptions.RequestException as e:
        return str(e)

def get_system_fingerprint(ip):
    nm = nmap.PortScanner()
    try:
        nm.scan(ip, arguments='-O')  # -O 参数用于操作系统检测
        if 'osclass' in nm[ip]:
            os_fingerprint = nm[ip]['osclass']
            return os_fingerprint
        elif 'osmatch' in nm[ip]:
            os_fingerprint = nm[ip]['osmatch']
            return os_fingerprint
        else:
            return "No OS information found"
    except Exception as e:
        return str(e)

# ip_address = '208.67.222.222'
# http_fingerprint = get_http_fingerprint(ip_address)
# print("HTTP Fingerprint:", http_fingerprint)

# system_fingerprint = get_system_fingerprint(ip_address)
# print("System Fingerprint:", system_fingerprint)