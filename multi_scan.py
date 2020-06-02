import argparse
import os
import ipaddress
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-a', type=str, help="Addresses input file path")
parser.add_argument('-p', type=str, help="Ports and protocols input file path")
parser.add_argument('-o', type=str, help="Output file path")
parser.add_argument('-t', type=str, help="tls-scan timeout value")
parser.add_argument('-b', type=str, help="tls-scan concurrency value")
args = parser.parse_args()

aFilePath = args.a
pFilePath = args.p
oFilePath = args.o
timeOut = args.t
conc = args.b
filesToMerge = []

if __name__ == '__main__':
    with open(pFilePath, 'r') as pFile:
        for line in pFile:
            l = line.strip().split()
            if l:
                print(l)
                tlsscanout = oFilePath + str(l[0]) + str(l[1])
                filesToMerge.append(tlsscanout)
                args = ("./tls-scan", rf"--infile={aFilePath}", rf"--outfile={tlsscanout}", "--cacert=ca-bundle.crt", "--pretty", "--all", rf"--port={l[0]}", rf"--starttls={l[1]}", rf"-t {timeOut}", rf"-b {conc}")
                p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                p.wait()
                output = p.stdout.read()
                print(output)
    print(f"Merging files: {filesToMerge} into file {oFilePath}")
    with open(oFilePath, 'w') as oFile:
        for fTM in filesToMerge:
            with open(fTM, 'r') as ftmFile:
                content = ftmFile.read()
                oFile.write(content)
            os.unlink(fTM)
