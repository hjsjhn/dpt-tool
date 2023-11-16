edns_opt_dict = {
    "NSID": 3,
    "DAU": 5,
    "DHU": 6,
    "NHU": 7,
    "ECS": 8,
    "EDE": 15
}


"""
DNSKEY Algorithms in RFC8624
   +--------+--------------------+-----------------+-------------------+
   | Number | Mnemonics          | DNSSEC Signing  | DNSSEC Validation |
   +--------+--------------------+-----------------+-------------------+
   | 1      | RSAMD5             | MUST NOT        | MUST NOT          |
   | 3      | DSA                | MUST NOT        | MUST NOT          |
   | 5      | RSASHA1            | NOT RECOMMENDED | MUST              |
   | 6      | DSA-NSEC3-SHA1     | MUST NOT        | MUST NOT          |
   | 7      | RSASHA1-NSEC3-SHA1 | NOT RECOMMENDED | MUST              |
   | 8      | RSASHA256          | MUST            | MUST              |
   | 10     | RSASHA512          | NOT RECOMMENDED | MUST              |
   | 12     | ECC-GOST           | MUST NOT        | MAY               |
   | 13     | ECDSAP256SHA256    | MUST            | MUST              |
   | 14     | ECDSAP384SHA384    | MAY             | RECOMMENDED       |
   | 15     | ED25519            | RECOMMENDED     | RECOMMENDED       |
   | 16     | ED448              | MAY             | RECOMMENDED       |
   +--------+--------------------+-----------------+-------------------+
"""
dnskey_algo_dict = {
    "RSAMD5": 1,
    "DSA": 3,
    "RSASHA1": 5,
    "DSA-NSEC3-SHA1": 6,
    "RSASHA1-NSEC3-SHA1": 7,
    "RSASHA256": 8,
    "RSASHA512": 10,
    "ECC-GOST": 12,
    "ECDSAP256SHA256": 13,
    "ECDSAP384SHA384": 14,
    "ED25519": 15,
    "ED448": 16
}