import argparse
import pandas as pd
import json
from tqdm import tqdm
from constant import default_choice, default_server, choice_to_func, choice_to_name

def str_to_dict_list(input_str):
    try:
        result = json.loads(input_str)
        if not isinstance(result, dict):
            raise argparse.ArgumentTypeError("Invalid input. Must be a dictionary.")
        for key, value in result.items():
            if not isinstance(value, list):
                raise argparse.ArgumentTypeError("Invalid input. Values must be lists.")
        return result
    except json.JSONDecodeError as e:
        raise argparse.ArgumentTypeError("Invalid input. Must be a valid JSON string.") from e

# %%
parser = argparse.ArgumentParser(description='A Tool to Detect the Basic Property of Public DNS', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-c', '--choice', nargs='+', type=str, help="""
The options of the test.
Example: -c all or -c opt_record, udp_payload_size
Supported options:
    all: all the options below
    opt_record: Support OPT Record (RFC 6891)
    udp_payload_size: Default UDP payload size
    client_subnet: Client Subnet (RFC 7871)
    nsid: NSID (RFC 5001)
    version_bind: version.bind CHAOS/TXT
    server_id: id.server CHAOS/TXT
    do_bit: DO bit
    response_validation: Response validation
    dnskey_algorithm: DNSKEY algorithms (RFC 8624)
    dot: DNS-over-TLS (RFC 7858)
    doh: DNS-over-HTTPS (RFC 8484)
    0x20: 0x20 encoding
    ede: EDNS Extended Errors (EDE)
""")
parser.add_argument('-s', '--server', nargs='+', type=str_to_dict_list, help="""
The DNS servers to test
Input must be in JSON format and contains a dictionary of server name to the ip list of that server.
Example: -s '{"Cloudflare": ["1.1.1.1", "1.0.0.1"], "Google Public DNS": ["8.8.8.8"]}'
""")
parser.add_argument('-o', '--output', type=str, help="The output file path")

args = parser.parse_args()
if args.choice == None:
    raise argparse.ArgumentTypeError("Invalid input. Must specify at least one choice.")
if len(args.choice) == 1 and ',' in args.choice[0]:
    args.choice = args.choice[0].split(',')
if args.output == None:
    args.output = "./result.csv"
args.server = args.server[0]
# print(args.choice)
# print(args.server)


if args.choice == ["all"]:
    args.choice = default_choice
else:
    # check if the choice is contained in default_choice using function instead of for loop
    if not set(args.choice).issubset(set(default_choice)):
        # output the choice that is not contained in default_choice
        raise argparse.ArgumentTypeError("Invalid input. The following choice is not supported:", ','.join(list(set(args.choice) - set(default_choice))))

if args.server is None:
    args.server = default_server

df = pd.DataFrame(columns=["Name", "Address"] + args.choice)
# apply the function to each server and each choice, output the result to the dataframe
funcs = [choice_to_func[choice] for choice in args.choice]

for name in tqdm(args.server.keys(), desc="Processing DNS servers"):
    for ip in tqdm(args.server[name], desc="    Processing ips", leave=False):
        df.loc[len(df)] = [name, ip, *[func(ip) for func in funcs]]

# print(df)
df.to_csv(args.output, index=False)