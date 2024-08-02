# Assignment the First

## Part 1
1. Be sure to upload your Python script. Provide a link to it here: [Part1.py](qual_score_dist.py)

[Part1.py filtering for N's and with median](qual_score_dist.py) <-- This script was made retroactively just to perform some data exploration on index 1 to determine a good quality score threshold.

| File name | label | Read length | Phred encoding |
|---|---|---|---|
| 1294_S1_L008_R1_001.fastq.gz | Forward read (read 1) | 101 | PHRED +33 |
| 1294_S1_L008_R2_001.fastq.gz | Index 1 | 8 | PHRED +33 |
| 1294_S1_L008_R3_001.fastq.gz | Index 2 | 8 | PHRED +33 |
| 1294_S1_L008_R4_001.fastq.gz | Reverse read (Read 2) | 101 | PHRED +33  |

1. To find the length of each sequence line:
		1. `zcat 1294_S1_L008_R1_001.fastq.gz | head -12 | awk 'NR%4 == 2 { print length(), $0}'`
		2. `zcat 1294_S1_L008_R2_001.fastq.gz | head -12 | awk 'NR%4 == 2 { print length(), $0}'`
		3. `zcat 1294_S1_L008_R4_001.fastq.gz | head -12 | awk 'NR%4 == 2 { print length(), $0}'`
		4. `zcat 1294_S1_L008_R4_001.fastq.gz | head -12 | awk 'NR%4 == 2 { print length(), $0}'`
	2. To find the phred encoding for each file
		1. `zcat 1294_S1_L008_R4_001.fastq.gz | head -8 | awk 'NR%4 == 0 { print($0)}' | grep ".<"`


2. Per-base NT distribution
i) Use markdown to insert your 4 histograms here.
Forward read histogram:
       ![Forward read histogram](https://github.com/asolomon4146/Demultiplex/blob/master/Assignment-the-first/1294_S1_L008_R1_001.png)
Index 1 histogram:
       ![Index 1 histogram](https://github.com/asolomon4146/Demultiplex/blob/master/Assignment-the-first/1294_S1_L008_R2_001.png)
Index 2 histogram:
       ![Index 2 histogram](https://github.com/asolomon4146/Demultiplex/blob/master/Assignment-the-first/1294_S1_L008_R3_001.png)
Reverse read histogram:
       ![Reverse read histogram](https://github.com/asolomon4146/Demultiplex/blob/master/Assignment-the-first/1294_S1_L008_R4_001.png)
   
ii) Using the median of one million reads from the center of index 1 (to avoid flow cell edge bias) as a representaiton of the median for all index reads, I would choose a quality score threshold of 27. Taking the median of medians (34) we find that it is similar enough to the mean of means (34.8) after filtering for N's that I chose a quality score threshold that was two standard deviations (3.3 each) below the mean. With a quality score threshold of 27 and a hamming distance no less than 2 for each index, that means that there is a 4*10^-6 chance of an index being mis assigned to the wrong sample. Extrapolated over 320 million reads and 24 samples, that means that after quality filtering, each sample will maintain just 53 mis assigned biological reads.

 iii) To count how many indexes contain undetermined base calls (contains an N) I used the following bash command:
 
1. `zcat /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz | head -12 | awk 'NR%4 == 2 {print($0)} | grep -c "N"`
 
2. 3,976,613 indexes in file 2 contain undetermined base calls.
 
3. 3,328,051 indexes in file 3 contain undetermined base calls.
 
## Part 2
1. Define the problem:
   Looking through a lane of sequencing data, I would like to determine the level of index hopping that occurred for dual-index paired end Illumina reads. There is a list of 24 different indexes and I need to create a series of files which contain which reads' indexes hopped and with what index they hopped.
2.  Describe output:
   This script will create a fastq file containing the record and the index-pairs appended to the header for each index that was not hopped. If it was hopped, then they are placed into a hopped file, and they will also undergo quality score filtering. If a read does not pass a minimum quality score threshold or if an index is not found in the original list of indexes (such as containing an N) then it will be placed into one of two unknown files. There will be 52 total fastq files generated.
5. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [>=6 expected output FASTQ files](../TEST-output_FASTQ).
    
7. Pseudocode:
```
#read 1 and read 2 refer to biological read 1 and 2 (the actual sequence lines)
#Record refers to all four lines of the record, not just the sequence.

i_library_forward = {}
i_library_forward.add(The 5th field of the index file given by argparse which contains the indexes)
i_library_rev = {}
i_library_rev.add(the reverse complement of i_library_forward)
#Added a reverse complement copy of each index to the library so that i2 can match the reverse complements.

#List of high level functions
def revcomp(seq1: str, seq2: str) -> bool:
	#A function to:
		1. check if two sequences (seq1 and seq2) are reverse compliments,return True or False as a bool named rc. This will be used on i1 and i2 (the indexes).
	return rc
Input: "GTAGCGTA", "TACGCTAC" (these are example indexes)
Expected output: True

def modify_header(record, i1, i2, file_handle):
	#A function to:
		1. take the indexes and append them to the end of the header line of a record
		2. Append the whole modified record to a given file handle.
	return None

u: int = 0 #Number of read pairs with unknown indexes
m: int = 0 #Number of read pairs with index matches
h: int = 0 #Number of read pairs with index hopping occured.

With Open (R1, R2, R3, R4):
	Read each file one line at a time:
		i1 = line(R2) #index 1, aka barcode 1
		i2 = line(R3) #index 2, aka barcode 2
		r1 = line(R1) #read 1 sequence
		r2 = line(R4) #read 2 sequence
		
		record1 = whole record of read1 sans header
		record2 = whole record of read2 sans header
		
		if i1 not in i_libary_forward or i2 not in i_library_rev or bioinfo.qualscore(i1) < qscore_threshold or bioinfo.qualscore(i2) < qscore_threshold:
			modify_header(record1, i1, i2, unknown1.fq)
			modify_header(record2, i1, i2, unknown2.fq)
			u+=1
		else:
			if revcomp(i1, i2) == True:
				modify_header(record1, i1, i2, i1_match.fq)
				modify_header(record2, i1, i2, i2_match.fq)
				m+=1
			else:
				modify_header(record1, i1, i2, hop1.fq)
				modify_header(record2, i1, i2, hop2.fq)
				h+=1
```
   
9. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement
