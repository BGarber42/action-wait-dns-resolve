import os
import logging

import backoff
import dns.resolver

resolver = dns.resolver.Resolver()


@backoff.on_exception(
    backoff.expo, dns.resolver.NXDOMAIN, max_time=float(os.environ.get("INPUT_MAXTIME", 60))
)
def resolve(host, record='A'):
    resolver.resolve(host, record)


def main():
    logging.getLogger("backoff").addHandler(logging.StreamHandler())
    my_host = os.environ["INPUT_REMOTEHOST"]
    record_type = os.environ["INPUT_RECORDTYPE"]

    try:
        resolve(my_host, record_type)
    except TimeoutError:
        print("Timed out waiting for resolve")
        raise Exception("Timed out waiting for connection")

    my_output = "Yay!"
    print(f"::set-output name=myOutput::{my_output}")


if __name__ == "__main__":
    main()
