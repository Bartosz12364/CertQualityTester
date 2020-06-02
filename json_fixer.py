import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, help="Input file path")
parser.add_argument('-o', type=str, help="Output file path")
args = parser.parse_args()

inputPath = args.i
outputPath = args.o

if __name__ == "__main__":
    with open(inputPath, 'r') as inputFile:
        with open(outputPath, 'w') as outputFile:
            originalLines = inputFile.readlines()
            newLines = []
            for line in originalLines:
                l = re.sub('^\}', '},', line)
                newLines.append(l)
            outputFile.seek(0, 0)
            outputFile.write("[\n")
            newLines[-1] = "}\n"
            outputFile.writelines(newLines)
            outputFile.close()
        with open(outputPath, 'a') as outputFile:
            outputFile.write("]")
