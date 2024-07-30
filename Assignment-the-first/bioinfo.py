#!/usr/bin/env python

# Author: asol asol@uoregon.edu

# Check out some Python module resources:
#   - https://docs.python.org/3/tutorial/modules.html
#   - https://python101.pythonlibrary.org/chapter36_creating_modules_and_packages.html
#   - and many more: https://www.google.com/search?q=how+to+write+a+python+module

'''This module is a collection of useful bioinformatics functions
written during the Bioinformatics and Genomics Program coursework.
You will need to add copies of this file to each location when you turn in an assignment.
You should update this docstring to reflect what you would like it to say

0.1 - Added convert_phred()
0.2 - Added qual_score()
0.3 - Added median_calc
0.4 - Added oneline fasta
0.5 - Added GC content and validate base seq
'''

__version__ = "0.3"         # Read way more about versioning here:
                            # https://en.wikipedia.org/wiki/Software_versioning

DNA_bases = set('ATGCatcg')     #can declare within funtion, slightly more efficient outside
RNA_bases = set('AUGCaucg')

def convert_phred(letter: str) -> int:
    '''Converts a single character into a phred score'''
    return ord(letter)-33

def qual_score(phred_score: str) -> float:
    '''Takes the average quality score of an entire Phred string'''
    total_qscore: int = 0
    avg: float = 0
    
    for i, letter in enumerate(phred_score):
        total_qscore+=convert_phred(letter)
    avg = total_qscore/len(phred_score)
    return(avg)

def validate_base_seq(seq,RNAflag=False):
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    return set(seq)<=(RNA_bases if RNAflag else DNA_bases)

def gc_content(DNA):
    assert validate_base_seq(DNA), "String contains invalid characters"
    
    DNA = DNA.upper()
    a = DNA.count('A')
    t = DNA.count('T')
    c = DNA.count('C')
    g = DNA.count('G')
    gc = g+c
    total = g+t+a+c
    return gc/total



def calc_median(lst: list) -> float:
    '''Given a sorted list, returns the median value of the list'''
    '''This function takes in a sorted list and returns the median.
    Checks if the length of the list is odd or even.
        #If False:
            #a) divide the length of the list by 2.
            #b) Subtract one from that number to get the position of the median of that list.
            #c) Call that position in the list to get the median value.
        #If Even:
            #a) divide the length of the list by 2 with floor division. Store it into a var called upper_med_pos
            #b) subtract one from upper_med_pos and store it into a var called lower_med_pos.
            #c) Take the mean of the values associated with upper_med_pos and lower_med_pos for the list.
    '''

    median: float = 0
    even: bool = False
    if len(lst)%2 == 0: #Determines if the list is odd or even in size
        even = True
    else:
        even = False
    if even == False:
        med_pos = int(len(lst)//2)
        median = lst[med_pos]

    if even == True:
        upper_med_pos = int(len(lst)/2)
        lower_med_pos = upper_med_pos - 1
        median = (lst[upper_med_pos]+lst[lower_med_pos])/2
        #print("median:", median)
    return median
    

def oneline_fasta(file_in: str, file_out: str):
    '''Takes in a correctly formatted fasta file,
    pulls the sequence lines into one single line per feature, and writes the output to a new specified file'''
    import re

    with open(file_in, "r") as f_in:
        with open(file_out, "w") as f_out:
            firstline: str = f_in.readline()
            f_out.write(firstline)
            for i, line in enumerate(f_in):
                line = line.strip()
                if re.findall("^>", line):
                    f_out.write('\n')
                    f_out.write(line)
                    f_out.write('\n')
                else:
                    f_out.write(line)

if __name__ == "__main__":
    # write tests for functions above, Leslie has already populated some tests for convert_phred
    # These tests are run when you execute this file directly (instead of importing it)
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("2") == 17, "wrong phred score for '2'"
    assert convert_phred("@") == 31, "wrong phred score for '@'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    print("Your convert_phred function is working! Nice job")


