import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, help="Input file path")
parser.add_argument('-o', type=str, help="Output file path")
args = parser.parse_args()

inputPath = args.i
outputPath = args.o

if __name__ == '__main__':
    addresses = []
    addressCount = 0
    exceptionCount = 0
    with open(inputPath) as f:
        with open(outputPath, 'w') as fi:
            lines = f.read().splitlines()
            for line in lines:
                try:
                    a = socket.gethostbyname(str(line))
                    fi.write(a)
                    fi.write("\n")
                    addressCount += 1
                    if addressCount % 1000 == 0:
                        print(f"{addressCount} adresses have been written to file...")
                except:
                    exceptionCount += 1
                    print(f"exception #{exceptionCount} occured...")
    print(f"{exceptionCount} exceptions occured")
