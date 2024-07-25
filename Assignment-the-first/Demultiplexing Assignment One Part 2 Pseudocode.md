```
#read 1 and read 2 refer to biological read 1 and 2 (the actual sequence lines)
#Record refers to all four lines of the record, not just the sequence.

i_library_forward = {}
i_library_forward.add(The 5th field of the index file given by argparse which contains the indexes)
i_library_rev = {}
i_library_rev.add(the reverse complement of i_library_forward)
#Added a reverse complement copy of each index to the library so that i2 can match the reverse complements.

#List of functions
def revcomp(seq1: str, seq2: str) -> bool:
	#A function to:
		1. check if two sequences (seq1 and seq2) are reverse compliments,return true or false. This will be used on i1 and i2.
	return rc
Input: "GTAGCGTA", "TACGCTAC"
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
