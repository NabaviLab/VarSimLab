#!/bin/bash
#SBATCH --job-name=myscript
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 4
#SBATCH --mail-type=END
#SBATCH --mem=15G
#SBATCH --mail-user=thomas.davis@uconn.edu
#SBATCH -o myscript_%j.out
#SBATCH -e myscript_%j.err
#SBATCH --partition=general
#SBATCH --qos=general
module load python
for i in `seq 1 1`
 do 
    python3 Exome_Script.py sim$i ./testseq -bed ./test.bed -c 2 -cnv 5 -cnv_min_size 4 -cnv_max_size 5 -indel 2 -s -subclones 1 
#    python3 Exome_Script.py sim$i ~/chr20.fa -bed ~/chr20_exons_with_150_added.bed -c 2 -cnv 5 -cnv_min_size 10 -cnv_max_size 100
 done
