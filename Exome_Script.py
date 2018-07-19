#program description: 
#we  substring out the exome from the genome, and call varsimlab on the exome. 
#We then go through the SINC error file and correct the positions listed--
# The error positions will be relative to the exome. We want them relative to the genome. 
# genome_position_of_error = exon_position_in_genome + error_position_in_exon
# first we go through the error list and figure out which exon the error belongs to. We then calculate the genome_position_of_error as above. 

import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")
import argparse
import os 
import subprocess
from itertools import accumulate
import bisect
import glob
#all of these imports are part of the python standard library of python3
#required arguments
parser=argparse.ArgumentParser() 
parser.add_argument("filename", help="name of output file") 
parser.add_argument("genome", help="genome to be processessed")
group=parser.add_mutually_exclusive_group(required=True)
group.add_argument("-use_genome", help="generate tumor and normal for entire provided sequence", action="store_true", default=False)
group.add_argument("-bed", help="generate tumor and normal based on bed file containing exonic regions") 

#read generation modifications
read_gen=parser.add_argument_group("read generation parameters", "arguments to adjust read generation") 
read_gen.add_argument("-c", help="read depth of coverage", default=25, type=float)
read_gen.add_argument("-s", help="use single end reads (default paired)", action="store_true", default=False) 
read_gen.add_argument("-l", help="read length. default 100 bp", type=int, default=100)
read_gen.add_argument("-m", help="maximum distance for two bed ranges to be merged into one range. If zero, merges only those ranges that directly overlap with each other", type=int, default=30)

#error generation modifications
#TODO fix these helps. too wordy and unclear: 
error_gen=parser.add_argument_group("error parameters", "arguments to adjust tumor error generation") 
error_gen.add_argument("-cnv", help="percent of total input to be incorporated into a CNV. Values from 0 to 100. 4 would signify 4 percent of input should be included in CNVs", type=float,default=8)
error_gen.add_argument("-cnv_min_size", help="minimum size of CNVs", default=10000, type=int)
error_gen.add_argument("-cnv_max_size", help="CNV_max_size", default=40000, type=int) 
error_gen.add_argument("-snp", help="percent of total input to be turned into SNPs. Values from 0 to 100. A value of 5 indicates 5 percent of genome should be turned into SNPs", type=float, default=.002)
error_gen.add_argument("-indel", help="percent of total input to be included in INDELS. values from 0 to 100, a value of 1 indicates 1 percent of the genome should be included in indels",default=.001, type=float)
 
args=parser.parse_args()

assert args.snp>=0 and args.snp<=100, "SNP rate should be between 0 and 100 percent"
assert args.cnv>=0 and args.cnv<=100, "CNV rate should be between 0 and 100 percent"
assert args.indel>=0 and args.indel<=100, "INDEL rate should be between 0 and 100 percent"
#ensure the user gives acceptable values for cnv, indel and snp rate. we could accomplish this with the choices arg in add_argument, but I think it makes the help page look ugly

def prep_bed(): 
 '''take bed file, merge together ranges that overlap or are within 30 bp of eachother. This prevents the same region being included twice, and prevents INDELS being created between nearby ranges'''
 os.system("module load bedtools")
 #bedtools_location=subprocess.check_output(["which bedtools"], shell=True, universal_newlines=True).strip()
 os.system("sort -k2,2n {} -o {}".format(args.bed, args.bed))
 #sort the bed file based on the start column (required for bedtools merge)
 new_bedfile=args.bed+"_disjoint"
 os.system("{} merge -d {} -i {} > {}".format("/isg/shared/apps/BEDtools/2.27.1/bin/bedtools", args.m, args.bed, new_bedfile))
 #merge together adjacent ranges in bed file, rendering the bed file nonoverlapping

def genome_IO(genome_file): 
 '''We take all the non-header lines out of the genome and contatenate 
    them together into a string which we return'''
 genome=[]
 with open(genome_file, "r") as f: 
  for line in f: 
   if line[0]!= ">":
   #if the line is not a header we add it to our genome string
    genome.append(line.strip())
    #We take out linebreaks (they'll mess with our math). We'll have to add them    back in later
 return ''.join(genome)

def genome_to_exome(genome):
 '''Given genome string, we substring out the exonic regions of the genome using the bed file. Returns a list with two elements: a list of exon sequences, and a list of genome offsets (position of exon in genome)'''
 exon_sequences=[]
 offsets=[]
 exon_ranges=[]
 fh= open(args.bed, "r")
 uniqueexons=list(set(fh.readlines()))
 #boucing it through a set keeps only unique lines
 for line in uniqueexons: 
  line=line.strip().split()
  if line:   
   start=int(line[1])
   end=int(line[2])
   exon_ranges.append((start,end))
 #list of (start,end) tuples, sorted by start position
 for start,end in exon_ranges:
  offsets.append(start) 
  exon=genome[start:end]
  exon_sequences.append(exon)
  #substring out exonic regions
 exome=[exon_sequences, offsets]
 #we could do this as a dict, but our list of lists will speed things up in a few steps 
 fh.close()
 return exome
  
def exome_chunk_index(exome):
 '''we need the position of each exon in the exome. That way we can decide which exon and given error falls into, and what genome offset to use for that error. given the list generated by genome_to_exome this function adds the list of exome positions and returns the three lists''' 
 exomelist=exome[0] 
 genome_offsets=exome[1]
 lengths=list(map(len, exomelist))
 #a list of the lengths of all the exon chunks
 exon_ends=list(accumulate(lengths))
 #the end position of each exon. Found by taking the cumulative sum of the lengths of the exons 
 exon_starts = [(end-length)+1 for (end,length) in zip(exon_ends,lengths)]
 #the start position of each exon (starting at one) 
 exome_with_offsets=[exomelist, genome_offsets, exon_starts] 
 #we've added a list with the start position of each exon in the exome
 return exome_with_offsets

def correct_error_file_faster(error_column, file, exome):
 '''Given an error file, the index of that error files uncorrected positions column, and the exome_with_offsets generated above, this function goes through the file and corrected the error_column to be relative to the genome, rather than the exome.''' 
 uncorrected_error_positions=[]
 #error positions relative to exome
 exon_number_of_errors=[]
 #will contain index of exon that each error belongs to. For example [2,4] means the first error belongs to the 2nd exon, and the 2nd error belongs to the       fourth exon
 corrected_error_positions=[]
 fh=open(file+"corrected", "w")
 if "CNV_results" in file:
  error_file=open(file, "r").readlines()[1:] 
  #ignore the header line of the CNV file. 
 else: 
  error_file=open(file,"r").readlines()  
 for line in error_file: 
  line=line.split()
  error_position=int(line[error_column]) 
  uncorrected_error_positions.append(error_position)
 genome_offsets=exome[1] 
 start_positions =exome[2]
 for error in uncorrected_error_positions:
  exon_number_of_errors.append(bisect.bisect(start_positions, error)-1)
  #determine which exon the particular error falls into, using our list of exon   start positions and a binary search algorithm
 for index, exon_index in enumerate(exon_number_of_errors):
  #iterating through the exon number of each error. 
  start_position=start_positions[exon_index] 
  #start position of exon in genome
  genome_offset=genome_offsets[exon_index] 
 #determine genome offset for each error, based on which exon it falls in
  error_position=uncorrected_error_positions[index]  
  exome_position=error_position-start_position
  #the position of the error within the exon. 
  corrected=genome_offset+exome_position+1
  corrected_error_positions.append(str(corrected))
 for position,line in enumerate(error_file):
  fh.write(corrected_error_positions[position]+"\t"+line) 
 fh.close()

def add_header(filename): 
 '''add a header column to the corrected file names, to make them more understandable.''' 
 fh=open(filename, "r+")
 content=fh.read()
 fh.seek(0,0)
 if "INDEL" in filename:
  #TODO fix
  fh.write("genome_position\ttarget\texome_start\texome_end\twho\tknows\n"+content) 
 if "SNP" in filename: 
  fh.write("genome_position\ttarget\texome_position\toriginal\tvariant\n"+content) 
 if "CNV_results" in filename: 
  fh.write("genome_start_position\ttarget\texome_start_position\ttype\tseq_size\tCNV_size\tallele_1_copies\tallele_2_copies\tNpercent_allele_1\tNpercent_allele_2\n"+content)
 if "stdresults" in filename: 
  fh.write("genome_start\tgenome_end\ttarget\texome_start\texome_end\ttype\n"+content) 
 fh.close() 

def call_varsimlab(genome_file, bed_file):
 '''we call varsimlab on our exonic regions.''' 
 genome=genome_IO(genome_file)
 exome_list=genome_to_exome(genome)  
 exome=exome_list[0] #make a list of the exonic regions 
 exome=''.join(exome)
 exome_with_linebreaks=[]
 for i in range(0, len(exome), 50):
  exome_with_linebreaks.append(exome[i:i+50])
 exome_with_linebreaks='\n'.join(exome_with_linebreaks)
#add in line breaks and a header. art needs them. 
 exome_with_linebreaks=(">exome\n"+exome_with_linebreaks)
 exome_file=open("exome_with_linebreaks.fa", "w") 
 exome_file.write(exome_with_linebreaks)
#exome with linebreaks used by run.sh  
 os.system("./art_run.sh {} {} {} {} {} {} {} {} {} {}".format(args.filename, "exome_with_linebreaks.fa", args.c, args.s, args.snp, args.indel, args.cnv, args.cnv_min_size, args.cnv_max_size, args.l))

if __name__=="__main__" and not args.use_genome:
#if we are doing exome sequencing
 genome=genome_IO(args.genome)
 prep_bed()
 args.bed=args.bed+"_disjoint"
 exomedict=genome_to_exome(genome)
 b=exome_chunk_index(exomedict) 
 call_varsimlab(args.genome, args.bed)
 filelist=glob.glob("{}/tumor/subclone_1/*.txt".format(args.filename))
 for file in filelist:
  if not "stdresults" in file: 
   correct_error_file_faster(1, file, b)
  else:
   correct_error_file_faster(2, file, b)
   correct_error_file_faster(2, file+"corrected", b)
#   correct the start and end of the CNVS in stdresults file
 os.system("rm {}/tumor/subclone_1/*.txt".format(args.filename)) 
 os.system("rm {}/tumor/subclone_1/CNV_stdresults.txtcorrected".format(args.filename))
 os.system("mv {}/tumor/subclone_1/*correctedcorrected {}/tumor/subclone_1/CNV_stdresultscorrected".format(args.filename, args.filename))
 #clean up
 filelist=glob.glob("{}/tumor/subclone_1/*".format(args.filename))
 for file in filelist:
  add_header(file)

elif __name__=="__main__": 
 os.system("./art_run.sh {} {} {} {} {} {} {} {} {} {}".format(args.filename, args.genome, args.c, args.s, args.snp, args.indel, args.cnv, args.cnv_min_size, args.cnv_max_size, args.l))
 #if we're just doing genome sequencing we can simply call run.sh. We don't need to do any error file correcting, or subsequencing. 
