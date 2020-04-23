import argparse
import os
import ipaddress

parser = argparse.ArgumentParser()
parser.add_argument('-b', type=str, help="Range beginning address")
parser.add_argument('-e', type=str, help="Range end address")
parser.add_argument('-f', type=str, help="Output file path")
args = parser.parse_args()

range_beg = ipaddress.ip_address(args.b)
range_end = ipaddress.ip_address(args.e)
out_path = args.f


if __name__ == "__main__":
    with open(out_path, 'w') as file:
        while range_beg <= range_end:
            file.write(str(range_beg) + "\n")
            range_beg += 1
