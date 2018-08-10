#!/usr/bin/env bash
module load bwa
ref=$(pwd) 
REFERENCE=$2
OUTPUT_PREFIX=$1
SNP_RATE=$5
INDEL_RATE=$6
TRANSITION_TRANSVERSION_RATIO=2
CNV_RATE=$7
CNV_MIN_SIZE=$8
CNV_MAX_SIZE=$9
FOLD_COVERAGE=$3
SINGLE_OR_PAIRED=$4
READ_LENGTH="${10}" 
PLOIDY="${11}"
SEED=$RANDOM
SUBCLONES="${12}"
GENOME="${13}"
sam="${14}"
SIMULATION_LOG_FILE=$ref/$OUTPUT_PREFIX/SIMULATION_IS_RUNNING.txt
M="-m 200"
if [[ "$SINGLE_OR_PAIRED" == "False" ]]; then
        SINGLE_OR_PAIRED="-p"
    else 
        unset SINGLE_OR_PAIRED
        unset M
fi
#if the -s argument was used, then SINGLE_OR_PAIRED will be null. otherwise it will be -p. 
mkdir -p $ref/$OUTPUT_PREFIX/normal
mkdir -p $ref/$OUTPUT_PREFIX/tumor
for i in `seq 1 $SUBCLONES`
do
   mkdir -p $ref/$OUTPUT_PREFIX/tumor/subclone_$i
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
printf "Fold Coverage: "$FOLD_COVERAGE"\n" >> $SIMULATION_LOG_FILE
printf "Read Length: "$READ_LENGTH"\n\n" >> $SIMULATION_LOG_FILE

# creating and copying files
printf "Copying temporary files for normal reads ..\n" >> $SIMULATION_LOG_FILE
cp $ref/$REFERENCE /$ref/$OUTPUT_PREFIX/normal
if [[ $sam == True ]]; then
#    cp $ref/$GENOME /$ref/$OUTPUT_PREFIX/normal
    cp $ref/$GENOME /$ref/$OUTPUT_PREFIX
fi
printf "Copying temporary files for tumor reads ..\n\n" >> $SIMULATION_LOG_FILE
for i in `seq 1 $SUBCLONES`
do
    cp $ref/$REFERENCE /$ref/$OUTPUT_PREFIX/tumor/subclone_$i
done

# generate normal reads
printf "Generating normal reads ..\n\n" >> $SIMULATION_LOG_FILE
cd $ref/
NORMAL_REFERENCE=$ref/$OUTPUT_PREFIX/normal/$REFERENCE
NORMAL_OUTPUT_PREFIX=$ref/$OUTPUT_PREFIX/normal/normal
./art_illumina -i $NORMAL_REFERENCE -rs $SEED $M -s 10 -l 100 $SINGLE_OR_PAIRED -f $FOLD_COVERAGE -o $NORMAL_OUTPUT_PREFIX >> $SIMULATION_LOG_FILE 2>&1
printf "Finished generating normal reads ..\n\n" >> $SIMULATION_LOG_FILE
# clean temporary files
cd $ref/$OUTPUT_PREFIX/normal
if [[ $sam == True ]]; then
    bwa index $ref/$OUTPUT_PREFIX/$GENOME
    if [[ "$SINGLE_OR_PAIRED" != "-p" ]]; then
        bwa mem -t 2 -r "@RG\tID:Tum_Chr20\tSM:Tumor_Chr20" $ref/$OUTPUT_PREFIX/$GENOME $ref/$OUTPUT_PREFIX/normal/normal.fq  > "normal.sam"
    #align single end reads into SAM file     
    else
        bwa mem -t 2 -r "@RG\tID:Tum_Chr20\tSM:Tumor_Chr20" $ref/$OUTPUT_PREFIX/$GENOME $ref/$OUTPUT_PREFIX/normal/normal1.fq $ref/$OUTPUT_PREFIX/normal/normal2.fq  > "normal.sam"
    #align paired end reads into sam file
    fi
fi 
#rm *.fa

# simulate tumor genome
for i in `seq 1 $SUBCLONES`
do
printf "Simulating tumor variations in subclone $i ..\n" >> $SIMULATION_LOG_FILE
printf "This step takes some time. Be patient and don't terminate the Docker container :)\n\n" >> $SIMULATION_LOG_FILE 2>&1
cd /$ref/$OUTPUT_PREFIX/tumor/subclone_$i
if (( $PLOIDY == 3)); then
    $ref/SInC/SInC_simulate -S $SNP_RATE -I $INDEL_RATE -p $CNV_RATE -l $CNV_MIN_SIZE -u $CNV_MAX_SIZE -t $TRANSITION_TRANSVERSION_RATIO $REFERENCE >> $SIMULATION_LOG_FILE
    for entry in /$ref/$OUTPUT_PREFIX/tumor/subclone_$i/*
    do
        if [[ $entry == *"allele_1"* ]]; then
            mv $entry 'allele_3.fa'
        fi
        if [[ $entry == *"allele_2"* ]]; then
            rm $entry
        fi
        if [[ $entry == *"SNPs"* ]] && [[ $entry == *"_1.txt" ]]; then
            mv $entry 'SNPs_3.txt'
        fi
        if [[ $entry == *"SNPs"* ]] && [[ $entry == *"_2.txt" ]]; then
            rm $entry
        fi
        if [[ $entry == *"INDELs"* ]] && [[ $entry == *"_1.txt" ]]; then
            mv $entry 'INDELs_3.txt'
        fi
        if [[ $entry == *"INDELs"* ]] && [[ $entry == *"_2.txt" ]]; then
            rm $entry
        fi
        if [[ $entry == *"CNV"* ]] && [[ $entry == *"stdresults"* ]]; then
            mv $entry 'CNV_stdresults_2.txt'
        fi
        if [[ $entry == *"CNV"* ]] && [[ $entry != *"stdresults"* ]]; then
            mv $entry 'CNV_results_2.txt'
        fi
    done
    printf "Measuring ploidy level .. Still simulating tumor variations in subclone $i ..\n\n" >> $SIMULATION_LOG_FILE
fi

$ref/SInC/SInC_simulate -S $SNP_RATE -I $INDEL_RATE -p $CNV_RATE -l $CNV_MIN_SIZE -u $CNV_MAX_SIZE -t $TRANSITION_TRANSVERSION_RATIO $REFERENCE >> $SIMULATION_LOG_FILE
for entry in $ref/$OUTPUT_PREFIX/tumor/subclone_$i/*
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
    fi
    if [[ $entry == *"CNV"* ]] && [[ $entry != *"stdresults"* ]] && [[ $entry != *"_2.txt" ]]; then
        mv $entry 'CNV_results.txt'
    fi
done

printf "Wait! Wait! Simulating the variations in subclone $i is complete. But it's still generating reads ..\n\n" >> $SIMULATION_LOG_FILE
printf "Cleaning temporary files ..\n\n" >> $SIMULATION_LOG_FILE
rm $REFERENCE

# generate tumor reads
# allele 1
cd $ref/
printf "Generating reads for subclone $i ..\n\n" >> $SIMULATION_LOG_FILE
TUMOR_REFERENCE=$ref/$OUTPUT_PREFIX/tumor/subclone_$i/allele_1.fa
TUMOR_OUTPUT_PREFIX=$ref/$OUTPUT_PREFIX/tumor/subclone_$i/tumor_allele1
./art_illumina -i $TUMOR_REFERENCE -rs $SEED $M -s 10 -l 100 $SINGLE_OR_PAIRED -f $FOLD_COVERAGE -o $TUMOR_OUTPUT_PREFIX >> $SIMULATION_LOG_FILE 2>&1

# allele 2
TUMOR_REFERENCE=$ref/$OUTPUT_PREFIX/tumor/subclone_$i/allele_2.fa
TUMOR_OUTPUT_PREFIX=$ref/$OUTPUT_PREFIX/tumor/subclone_$i/tumor_allele2
./art_illumina -i $TUMOR_REFERENCE -rs $SEED $M -s 10 -l 100 -f $FOLD_COVERAGE $SINGLE_OR_PAIRED -o $TUMOR_OUTPUT_PREFIX >> $SIMULATION_LOG_FILE 2>&1

printf "Finished generating reads for subclone $i ..\n\n" >> $SIMULATION_LOG_FILE
# allele 3
if (( $PLOIDY == 3)); then
    TUMOR_REFERENCE=$ref/$OUTPUT_PREFIX/tumor/subclone_$i/allele_3.fa
    TUMOR_OUTPUT_PREFIX=$ref/$OUTPUT_PREFIX/tumor/subclone_$i/tumor_allele3
    ./art_illumina -i $TUMOR_REFERENCE -rs $SEED $M -s 10 -l 100 -f $FOLD_COVERAGE $SINGLE_OR_PAIRED -o $TUMOR_OUTPUT_PREFIX >> $SIMULATION_LOG_FILE 2>&1
    printf "Finished generating reads for subclone $i ..\n\n" >> $SIMULATION_LOG_FILE
fi

# clean temporary files
cd $ref/$OUTPUT_PREFIX/tumor/subclone_$i
if [[ $sam == True ]]; then
    if [[ "$SINGLE_OR_PAIRED" != "-p" ]]; then
        bwa mem -t 2 -r "@RG\tID:Tum_Chr20\tSM:Tumor_Chr20" $ref/$OUTPUT_PREFIX/$GENOME $ref/$OUTPUT_PREFIX/tumor/subclone_$i/tumor_allele1.fq  > "allele1.sam"
        bwa mem -t 2 -r "@RG\tID:Tum_Chr20\tSM:Tumor_Chr20" $ref/$OUTPUT_PREFIX/$GENOME $ref/$OUTPUT_PREFIX/tumor/subclone_$i/tumor_allele2.fq  > "allele2.sam"
    #align single end reads from each of the two alleles into seperate SAM files
    else
        bwa mem -t 2 -r "@RG\tID:Tum_Chr20\tSM:Tumor_Chr20" $ref/$OUTPUT_PREFIX/$GENOME $ref/$OUTPUT_PREFIX/tumor/subclone_$i/tumor_allele11.fq $ref/$OUTPUT_PREFIX/tumor/subclone_$i/tumor_allele12.fq  > "allele1.sam"
        bwa mem -t 2 -r "@RG\tID:Tum_Chr20\tSM:Tumor_Chr20" $ref/$OUTPUT_PREFIX/$GENOME $ref/$OUTPUT_PREFIX/tumor/subclone_$i/tumor_allele11.fq $ref/$OUTPUT_PREFIX/tumor/subclone_$i/tumor_allele12.fq  > "allele1.sam"
    fi
fi
#align paired end read from each of the two alleles into seperate sam files

#rm *.bed*
rm *.fa
done

# at the end of the simulation, rename the log file
printf "SIMULATION IS COMPLETE. CHECK THE FOLDERS FOR READS!" >> $SIMULATION_LOG_FILE
mv $SIMULATION_LOG_FILE $ref/$OUTPUT_PREFIX/SIMULATION_IS_COMPLETE.txt
