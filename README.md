# dpt-tool

## Overview
The dpt-tool is a utility written in Python 3 designed to test various basic properties of public DNS servers. It provides a simple way to examine and analyze the supported features of these servers through a command-line interface.

## Installation
To install the dpt-tool, use the following command:
```bash
pip install -r requirements.txt
```
This will resolve the necessary dependencies for the tool to run.

## Usage

To use the tool, you can follow the example commands below.

### Example 1: Performing all tests with default DNS servers

```bash
python main.py -c all
```

### Example 2: Specifying the DNS servers and output file
```bash
python main.py -c udp_payload_size, do_bit -s '{"Cloudflare": ["1.1.1.1", "1.0.0.1"], "Google Public DNS": ["8.8.8.8"]}' -o output.txt
```

The available test options are:

- `opt_record`: Support OPT Record (RFC 6891)
- `udp_payload_size`: Default UDP payload size
- `client_subnet`: Client Subnet (RFC 7871)
- `nsid`: NSID (RFC 5001)
- `version_bind`: version.bind CHAOS/TXT
- `server_id`: id.server CHAOS/TXT
- `do_bit`: DO bit
- `response_validation`: Response validation
- `dnskey_algorithm`: DNSKEY algorithms (RFC 8624)
- `dot`: DNS-over-TLS (RFC 7858)
- `doh`: DNS-over-HTTPS (RFC 8484)
- `0x20`: 0x20 encoding
- `ede`: EDNS Extended Errors (EDE)

For specifying the DNS servers, the input must be in JSON format containing a dictionary of server names mapped to a list of IP addresses for each server.

## Feedback

Feedback and contributions are welcome! If you encounter any issues or have ideas for improvements, please feel free to open an issue or a pull request on the GitHub repository.
