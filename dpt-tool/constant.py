# write a code with the following requirements:
# take a list of options from command line with -c or --choice
# take a list of servers from command line with -s or --server
# use the corresponding function to query each server and output a table with each server as a column, and each option as a row
# the options are:
# all: all the options below
# opt_record: function check_dns_opt_record, output row Support OPT Record (RFC 6891)
# udp_payload_size: function check_dns_udp_payload_size, output row Default UDP payload size
# client_subnet: function check_ecs, output the row Client Subnet (RFC 7871)
# nsid: function check_nsid_support, output the row NSID (RFC 5001)
# version_bind: function get_version_bind, output the row version.bind CHAOS/TXT
# server_id: function get_id_server, output the row id.server CHAOS/TXT
# do_bit: function check_do_bit, output the row DO bit
# response_validation: function check_response_validation, output the row Response validation
# dnskey_algorithm: function get_dnskey_alg, output the row DNSKEY algorithms (RFC 8624)
# dot: function get_dot_info, output the row DNS-over-TLS (RFC 7858)
# doh: function get_doh_info, output the row DNS-over-HTTPS (RFC 8484)
# 0x20: function check_0x20_encoding, output the row 0x20 encoding
# ede: function get_ede_support_category, output the row EDNS Extended Errors (EDE)

from dnssec import *
from edns import *
from encrypted_dns_and_privacy import *
from extended_errors import *
from measures_against_response_forgery import *
from server_identification import *

RETRIES = 3        # how many times to try for a single test
TOTAL_RETRIES = 3  # how many times to try for the entire test queue
TIMEOUT = 0.5      # timeout for a single test (second)

# %%
default_server = {
    "Cloudflare": ["1.1.1.1", "1.0.0.1"],
    "Google Public DNS": ["8.8.8.8", "8.8.4.4"],
    "DNS PAI": ["101.226.4.6", "123.125.81.6", "101.226.4.6", "101.226.4.6"],
    "CNNIC SDNS": ["1.2.4.8"],
    "DNSPod": ["119.29.29.29"],
    "DNS.Watch": ["84.200.69.80", "84.200.70.40"],
    "Oracle Dyn": ["216.146.35.35", "216.146.36.36"],
    "Level3": ["209.244.0.3", "209.244.0.4"],
    "OpenDNS": ["208.67.222.222", "208.67.220.220"],
    "OpenNic": ["134.195.4.2", "217.160.166.161"],
    "Quad9": ["9.9.9.9", "9.9.9.10", "9.9.9.11"],
    "Verisig Open DNS": ["64.6.64.6", "64.6.65.6"],
    "One DNS": ["117.50.10.10"],
    "Yandex DNS": ["77.88.8.8", "77.88.8.1", "77.88.8.88", "77.88.8.7"],
    "Comodo DNS": ["8.26.56.26", "8.20.247.20"],
    "SafeDNS": ["195.46.39.39", "195.46.39.40"],
    "Freenom World": ["80.80.80.80", "80.80.81.81"],
    "CleanBrowsing": ["185.228.168.9"],
    "Alternate DNS": ["76.76.19.19", "76.223.122.150"],
    "Ali DNS": ["223.5.5.5"],
    "Baidu DNS": ["180.76.76.76"],
    "114 DNS": ["114.114.114.114", "114.114.115.115", "114.114.114.119", "114.114.114.110"],
    "Quad101": ["101.101.101.101"]
}
choice_to_func = {
    "opt_record": check_dns_opt_record,
    "udp_payload_size": check_dns_udp_payload_size,
    "client_subnet": check_ecs,
    "nsid": check_nsid_support,
    "version_bind": get_version_bind,
    "server_id": get_id_server,
    "do_bit": check_do_bit,
    "response_validation": check_response_validation,
    "dnskey_algorithm": get_dnskey_alg,
    "dot": get_dot_info,
    "doh": get_doh_info,
    "0x20": check_0x20_encoding,
    "ede": get_ede_support_category
}
choice_to_name = {
    "opt_record": "Support OPT Record (RFC 6891)",
    "udp_payload_size": "Default UDP payload size",
    "client_subnet": "Client Subnet (RFC 7871)",
    "nsid": "NSID (RFC 5001)",
    "version_bind": "version.bind CHAOS/TXT",
    "server_id": "id.server CHAOS/TXT",
    "do_bit": "DO bit",
    "response_validation": "Response validation",
    "dnskey_algorithm": "DNSKEY algorithms (RFC 8624)",
    "dot": "DNS-over-TLS (RFC 7858)",
    "doh": "DNS-over-HTTPS (RFC 8484)",
    "0x20": "0x20 encoding",
    "ede": "EDNS Extended Errors (EDE)"
}
default_choice = list(choice_to_func.keys())