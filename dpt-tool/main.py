import argparse
import multiprocessing
import pandas as pd
import json
from tqdm import tqdm
from time import sleep
from constant import default_choice, default_server, choice_to_func, choice_to_name, RETRIES, TOTAL_RETRIES, TIMEOUT

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
        print(input_str)
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
else:
    args.server = args.server[0]

df = pd.DataFrame(columns=["Name", "Address"] + args.choice)
# apply the function to each server and each choice, output the result to the dataframe
funcs = [choice_to_func[choice] for choice in args.choice]

def test_with_retry(func, ip):
    for i in range(RETRIES):
        try:
            ret = func(ip)
            if isinstance(ret, bool):
                ret = "Yes" if ret else "No"
            return ret
        except:
            sleep(TIMEOUT)
            pass
    return "FAILED"

def start_test(name, ip):
    ret = [name, ip]
    for func in funcs:
        # print(func, ip)
        ret.append(test_with_retry(func, ip))
        # print(ret[-1])
        sleep(TIMEOUT)
    return ret
    # return [name, ip, *[test_with_retry(func, ip) for func in funcs]]


queue = args.server
for i in range(TOTAL_RETRIES):
    if not queue:
        break
    nqueue = {}
    for name in tqdm(queue.keys(), desc=f"Processing DNS servers(round {i+1})"):
        for ip in tqdm(queue[name], desc=f"    Processing {name}'s ips", leave=False):
            sleep(1)
            ret = None
            with multiprocessing.Pool() as pool:
                result = pool.apply_async(start_test, (name,ip,))
                ret = None
                try:
                    ret = result.get(timeout=1200)
                except:
                    if name in nqueue:
                        nqueue[name].append(ip)
                    else:
                        nqueue[name] = [ip]
                """
                for cnt in range(3):
                    try:
                        ret = result.get(timeout=180)
                        break
                    # except multiprocessing.TimeoutError:
                    except Exception as e:
                        print(e)
                        sleep(1)
                """
            # df.loc[len(df)] = [name, ip, *[func(ip) for func in funcs]]
            if ret:
                df.loc[len(df)] = ret
        df.to_csv(args.output, index=False)
    queue = nqueue
    if queue:
        sleep(5)

if queue:
    print("The DNS resolvers below failed the test:")
    for name in queue:
        print(f"{name}: ", end='')
        for ip in queue[name]:
            print(ip, end=' ')
        print()

# print(df)
df.to_csv(args.output, index=False)
