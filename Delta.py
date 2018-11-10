#!/usr/bin/env python3
"""Splits up large matrices into smaller files for Windows.
"""

import argparse
import itertools
import pathlib
import sys
from time import gmtime, strftime

__author__ = "Cecil barnett-Neefs"
__copyright__ = "Copyright 2018, Slapdash programming"
__credits__ = ["Cecil Barnett-Neefs"]
__license__ = "GPL"
__version__ = "1.0"
__email__ = "cil@barnett-neefs.net"

parser = argparse.ArgumentParser(description="Takes tab delimited text files and "
                                             "splits them into files of separated column groups (default 500 per file)")

parser.add_argument("-f", "--file", type=str, help='A string for the target file', required=True)

parser.add_argument("-w", "--width", type=int, default=500, help='Number of samples per file')

args = parser.parse_args()

if args.file:
    file = args.file
    file = file.replace("\\", "/")

if args.width:
    width = args.width

try:
    test=open(file, "r")
except IOError:
    print("Error: File does not appear to exist.")
    sys.exit()

test.close()

filepath = file.replace(".txt", "")

target_name = filepath.split("/")[-1]

pathlib.Path(filepath).mkdir(parents=True, exist_ok=True)

filepath = filepath + "/"

sys.stdout.write(strftime("Sample splitter program DELTA, created by Cecil Barnett-Neefs ("
                          "cil@barnett-neefs.net)\nWARNING - Large files will take a long time to split, "
                          "you have been warned!\n%Y-%m-%d %H:%M:%S", gmtime())+" Working:\n")

leader = []
body = []
total_samples = 0
offset = 0
cycle = 1

while True:
    with open(file, "r") as infile:
        i = 0
        header = infile.readline()
        total_samples = (len(header.split("\t")))-1
        infile.seek(0)
        if (total_samples-offset) < width:
            x = total_samples - offset
            sys.stdout.write(strftime("%Y-%m-%d %H:%M:%S", gmtime())+" Pass: {} - Position: {} of {} ({} Samples)\n".format(cycle, offset, total_samples, x))
        else:
            sys.stdout.write(strftime("%Y-%m-%d %H:%M:%S", gmtime())+" Pass: {} - Position: {} of {} ({} Samples)\n".format(cycle, offset, total_samples, width))
        for line in infile:
            leader.append(line.split("\t")[0].rstrip('\n')+"\t")
            item = "\t".join(line.split("\t")[(1+offset):(width+offset+1)])+"\n"
            body.append(item)
        leader_length = len(leader)
        output_name = "{} Split {}.txt".format(target_name, cycle)
        destination = filepath+output_name
        o = open(destination, "w+")
        while i <= leader_length - 1:
            o.write(leader[i] + body[i])
            i = i + 1
        o.close()
        cycle = cycle+1
        offset = offset+width
        body = []
        leader = []
    if offset >= total_samples:
        break

sys.stdout.write(strftime("%Y-%m-%d %H:%M:%S", gmtime())+" Your file has been split by DELTA!\n-CBN")
