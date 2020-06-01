import csv
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, help="Input file path")
parser.add_argument('-o', type=str, help="Output file path")
parser.add_argument('-r', type=str, help="Top level domain we are interested in, without the dot, e.g. pl, com, gov")
args = parser.parse_args()

inputPath = args.i
outputPath = args.o
dom = args.r

if __name__ == '__main__':
    with open(inputPath, 'r') as f:
	    with open(outputPath, 'w') as o:
		    csvReader = csv.reader(f)
		    for row in csvReader:
			    match = re.search(fr'.*(\.{dom})', row[1])
			    if(match):
				    # print(match.group())
				    o.write(match.group() + "\n")
