#!/usr/bin/env bash

REFERENCE=$1
TARGET=$2
OUTPUT_PREFIX=$3

SNP_RATE=$4
INDEL_RATE=$5
TRANSITION_TRANSVERSION_RATIO=$6
CNV_RATE=$7
CNV_MIN_SIZE=$8
CNV_MAX_SIZE=$9
NUMBER_OF_READS="${10}"
READ_LENGTH="${11}"
PLOIDY="${12}"
SUBCLONES="${13}"
SIMULATION_LOG_FILE=/ref/$OUTPUT_PREFIX/SIMULATION_IS_RUNNING.txt

# create simulation directory
mkdir -p /ref/$OUTPUT_PREFIX/normal
mkdir -p /ref/$OUTPUT_PREFIX/tumor
for i in `seq 1 $SUBCLONES`
do
   mkdir -p /ref/$OUTPUT_PREFIX/tumor/subclone_$i
done

# print a starting message
printf "SIMULATION STARTED WITH THE FOLLOWING PARAMETERS\n\n" > $SIMULATION_LOG_FILE
printf "SNP Rate: "$SNP_RATE"\n" >> $SIMULATION_LOG_FILE
printf "Indel Rate: "$INDEL_RATE"\n" >> $SIMULATION_LOG_FILE
printf "Transition/Transversion Ratio: "$TRANSITION_TRANSVERSION_RATIO"\n" >> $SIMULATION_LOG_FILE
printf "CNV Rate: "$CNV_RATE"\n" >> $SIMULATION_LOG_FILE
printf "CNV Minimum Size: "$CNV_MIN_SIZE"\n" >> $SIMULATION_LOG_FILE
printf "CNV Maximum Size: "$CNV_MAX_SIZE"\n" >> $SIMULATION_LOG_FILE
printf "Ploidy: "$PLOIDY"\n" >> $SIMULATION_LOG_FILE
printf "Subclones: "$SUBCLONES"\n" >> $SIMULATION_LOG_FILE
printf "Number of Reads: "$NUMBER_OF_READS"\n" >> $SIMULATION_LOG_FILE
printf "Read Length: "$READ_LENGTH"\n\n" >> $SIMULATION_LOG_FILE

# creating and copying files
printf "Copying temporary files for normal reads ..\n" >> $SIMULATION_LOG_FILE
cp /ref/$REFERENCE /ref/$OUTPUT_PREFIX/normal
cp /ref/$TARGET /ref/$OUTPUT_PREFIX/normal
printf "Copying temporary files for tumor reads ..\n\n" >> $SIMULATION_LOG_FILE
for i in `seq 1 $SUBCLONES`
do
    cp /ref/$REFERENCE /ref/$OUTPUT_PREFIX/tumor/subclone_$i
    cp /ref/$TARGET /ref/$OUTPUT_PREFIX/tumor/subclone_$i
done

# generate normal reads
printf "Generating normal reads ..\n\n" >> $SIMULATION_LOG_FILE
cd /easyscnvsim_lib/Wessim/
NORMAL_REFERENCE=/ref/$OUTPUT_PREFIX/normal/$REFERENCE
NORMAL_TARGET=/ref/$OUTPUT_PREFIX/normal/$TARGET
NORMAL_OUTPUT_PREFIX=/ref/$OUTPUT_PREFIX/normal/normal
MODEL_FILE=/easyscnvsim_lib/Wessim/models/ill100v4_p.gzip
python Wessim1.py -R $NORMAL_REFERENCE -B $NORMAL_TARGET -n 10000 -l $READ_LENGTH -M $MODEL_FILE -o $NORMAL_OUTPUT_PREFIX -t 2 -p >> $SIMULATION_LOG_FILE 2>&1
printf "Finished generating normal reads ..\n\n" >> $SIMULATION_LOG_FILE

# clean temporary files
cd /ref/$OUTPUT_PREFIX/normal
rm *.bed*
rm *.fa
rm *.fa.fai

# simulate tumor genome
for i in `seq 1 $SUBCLONES`
do
printf "Simulating tumor variations in subclone $i ..\n" >> $SIMULATION_LOG_FILE
printf "This step takes some time. Be patient and don't terminate the Docker container :)\n\n" >> $SIMULATION_LOG_FILE 2>&1
cd /ref/$OUTPUT_PREFIX/tumor/subclone_$i

/easyscnvsim_lib/SInC/SInC_simulate -S $SNP_RATE -I $INDEL_RATE -p 0 -l 0 -u 0 -t $TRANSITION_TRANSVERSION_RATIO $REFERENCE >> $SIMULATION_LOG_FILE
for entry in /ref/$OUTPUT_PREFIX/tumor/subclone_$i/*
do
    if [[ $entry == *"allele_1"* ]]; then
        mv $entry 'allele_1.fa'
    fi
    if [[ $entry == *"allele_2"* ]]; then
        mv $entry 'allele_2.fa'
    fi
    if [[ $entry == *"SNPs"* ]] && [[ $entry == *"_1.txt" ]]; then
        mv $entry 'SNPs_1.txt'
    fi
    if [[ $entry == *"SNPs"* ]] && [[ $entry == *"_2.txt" ]]; then
        mv $entry 'SNPs_2.txt'
    fi
    if [[ $entry == *"INDELs"* ]] && [[ $entry == *"_1.txt" ]]; then
        mv $entry 'INDELs_1.txt'
    fi
    if [[ $entry == *"INDELs"* ]] && [[ $entry == *"_2.txt" ]]; then
        mv $entry 'INDELs_2.txt'
    fi
    if [[ $entry == *"CNV"* ]] && [[ $entry == *"stdresults"* ]] && [[ $entry != *"_2.txt" ]]; then
        mv $entry 'CNV_stdresults.txt'
        rm CNV_stdresults.txt
    fi
    if [[ $entry == *"CNV"* ]] && [[ $entry != *"stdresults"* ]] && [[ $entry != *"_2.txt" ]]; then
        mv $entry 'CNV_restuls.txt'
        rm CNV_restuls.txt
    fi
done

done
printf "Wait! Wait! Simulating the variations in subclone $i is complete. But it's still generating reads ..\n\n" >> $SIMULATION_LOG_FILE
printf "Cleaning temporary files ..\n\n" >> $SIMULATION_LOG_FILE
rm $REFERENCE

# generate tumor reads
cd /easyscnvsim_lib/CNVSim/
TUMOR_REFERENCE=/ref/$OUTPUT_PREFIX/tumor/subclone_$i/allele_1.fa
TUMOR_TARGET=/ref/$OUTPUT_PREFIX/tumor/subclone_$i/$TARGET
TUMOR_OUTPUT_PREFIX=/ref/$OUTPUT_PREFIX/tumor/subclone_$i/allele_1_
TUMOR_NUMBER_OF_READS=$(($NUMBER_OF_READS / $PLOIDY ))
TUMOR_NUMBER_OF_READS=$(($TUMOR_NUMBER_OF_READS / $SUBCLONES))
python cnv-sim.py -o $TUMOR_OUTPUT_PREFIX -n $NUMBER_OF_READS -g $CNV_RATE -r_min $CNV_MIN_SIZE -r_max $CNV_MAX_SIZE exome $TUMOR_REFERENCE $TUMOR_TARGET >> $SIMULATION_LOG_FILE 2>&1

TUMOR_REFERENCE=/ref/$OUTPUT_PREFIX/tumor/subclone_$i/allele_2.fa
TUMOR_TARGET=/ref/$OUTPUT_PREFIX/tumor/subclone_$i/$TARGET
TUMOR_OUTPUT_PREFIX=/ref/$OUTPUT_PREFIX/tumor/subclone_$i/allele_2_
TUMOR_NUMBER_OF_READS=$(($NUMBER_OF_READS / $PLOIDY ))
TUMOR_NUMBER_OF_READS=$(($TUMOR_NUMBER_OF_READS / $SUBCLONES))
python cnv-sim.py -o $TUMOR_OUTPUT_PREFIX -n $NUMBER_OF_READS -g $CNV_RATE -r_min $CNV_MIN_SIZE -r_max $CNV_MAX_SIZE exome $TUMOR_REFERENCE $TUMOR_TARGET >> $SIMULATION_LOG_FILE 2>&1

cd /ref/$OUTPUT_PREFIX/tumor/subclone_$i/
rm control_1.fastq
rm control_2.fastq
rm allele_1.fa
rm allele_2.fa
rm *targets.bed
mv allele_1_cnv_1.fastq allele_1_tumor_1.fastq
mv allele_1_cnv_2.fastq allele_1_tumor_2.fastq
mv allele_2_cnv_1.fastq allele_2_tumor_1.fastq
mv allele_2_cnv_2.fastq allele_2_tumor_2.fastq

# at the end of the simulation, rename the log file
printf "SIMULATION IS COMPLETE. CHECK THE FOLDERS FOR READS!" >> $SIMULATION_LOG_FILE
mv $SIMULATION_LOG_FILE /ref/$OUTPUT_PREFIX/SIMULATION_IS_COMPLETE.txt