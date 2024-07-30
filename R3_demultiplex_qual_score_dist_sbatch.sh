#!/usr/bin/bash

#SBATCH --partition=bgmp
#SBATCH --account=bgmp
#SBATCH --mem=100G
#SBATCH --time=0-3
#SBATCH --mail-user=$asol@uoregon.edu 
#SBATCH --mail-type=ALL

/usr/bin/time -v ./Assignment-the-first/qual_score_dist.py -i /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz -p Assignment-the-first/1294_S1_L008_R3_001.png -l 8
exit