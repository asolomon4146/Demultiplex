#!/usr/bin/env python

import bioinfo
import argparse
import matplotlib.pyplot as plt
import gzip

def get_args():
    parser = argparse.ArgumentParser(description="A program to extract information from contigs.fa file from velvetg")
    parser.add_argument("-i", "--input", help="Your input data file name is", required=True, type = str)
    parser.add_argument("-l", "--length", help="The length of each read is", required=True, type = int)
    parser.add_argument("-p", "--plot", help="The file you want to write your plot to is", required=True, type = str)
    return parser.parse_args()

args = get_args()
read_length: int = int(args.length)

input_file = args.input

def init_list(lst: list, value: float=0.0) -> list:
    '''This function takes an empty list and will populate it with
    the value passed in "value". If no value is passed, initializes list
    with the number found in args.length of 0.0.'''
    
    for i in range(0,read_length):
        lst.append(value)
    return lst

my_list: list = []
my_list = init_list(my_list)

def populate_list(input_file: str) -> tuple[list, int]:
    """Creates an empty list, opens the fastq file, reads it line by line,
    parses out the quality scores, converts them to numbers, sums the Qscores in each base, returns the list with a counter"""
    i = 0
    sum_Q = init_list([], 0.0)
    with gzip.open(input_file, "rt") as f:
        for line in f:
            line = line.strip()
            if (i+1) %4 == 0:
                for c, base in enumerate(line):
                    sum_Q[c]+=(bioinfo.convert_phred(base))
            i+=1
    return sum_Q, i

my_list, num_lines = populate_list(input_file)

my_list = [j/(num_lines/4) for j in my_list]
num_reads = num_lines/4
print("# Base Pair" + "\t" + "Mean Quality Score")
for k, mqs in enumerate(my_list):
    print(f'{k}\t{mqs}')

#Plotting with matplotlib:
print("Object type of read_length variable:", type(read_length), "\nAnd the value of read_length is:", read_length)
fig, ax = plt.subplots(figsize=(14, 6))

positions = list(range(1, (read_length+1)))

ax.plot(positions, my_list, '.-', color='blue', linewidth=1)
ax.set_title('Average Quality Score by Nucleotide Position', fontsize = 16)
ax.set_xlabel('Nucleotide Position', fontsize = 14)
ax.set_ylabel('Mean Quality Score', fontsize = 14)

plt.tight_layout()
plt.savefig(args.plot)
