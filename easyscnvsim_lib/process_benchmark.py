import sys

target_file = sys.argv[1]
benchmark_file = sys.argv[2]

targets = []
with open(target_file, 'r') as f:
    for line in f:
        target = line.split('\t')
        targets.append((int(target[1].strip()), int(target[2].strip())))

def filter_snps(benchmark_file):
    global targets
    snps = []
    with open(benchmark_file, 'r') as f:
        for line in f:
            snp = line.split('\t')
            # check to see if this SNP lies in any of the targets
            for t in targets:
                snp[1] = int(snp[1])
                if snp[1] <= t[1]:
                    if snp[1] >= t[0]:
                        snps.append(snp)
                        break

    with open(benchmark_file, 'w') as f:
        for snp in snps:
            f.write('\t'.join(map(str,snp)))


def filter_indels(benchmark_file):
    indels = []
    with open(benchmark_file, 'r') as f:
        for line in f:
            indel = line.split('\t')
            # check to see if this indel lies in any of the targets
            for t in targets:
                indel[1] = int(indel[1])
                indel[2] = int(indel[2])
                if indel[1] <= t[1]:
                    if indel[1] >= t[0]:
                        indels.append(indel)
                        break
                if indel[2] <= t[1]:
                    if indel[2] >= t[0]:
                        indels.append(indel)
                        break

    with open(benchmark_file, 'w') as f:
        for indel in indels:
            f.write('\t'.join(map(str,indel)))

def filter_cnv_results(benchmark_file):
    cnvs = []
    with open(benchmark_file, 'r') as f:
        header = f.read()
        for line in f:
            cnv = line.split('\t')
            # check to see if this CNV lies in any of the targets
            for t in targets:
                cnv[1] = int(cnv[1])
                if cnv[1] <= t[1]:
                    if cnv[1] >= t[0]:
                        cnvs.append(cnv)
                        break

    with open(benchmark_file, 'w') as f:
        f.write(header.strip() + '\n')
        for cnv in cnvs:
            f.write('\t'.join(map(str,cnv)))


def filter_cnv_std_restuls(benchmark_file):
    cnvs = []
    with open(benchmark_file, 'r') as f:
        for line in f:
            cnv = line.split('\t')
            # check to see if this SNP lies in any of the targets
            for t in targets:
                cnv[1] = int(cnv[1])
                cnv[2] = int(cnv[2])
                if cnv[1] <= t[1]:
                    if cnv[1] >= t[0]:
                        cnvs.append(cnv)
                        break
                if cnv[2] <= t[1]:
                    if cnv[2] >= t[0]:
                        cnvs.append(cnv)
                        break

    with open(benchmark_file, 'w') as f:
        for cnv in cnvs:
            f.write('\t'.join(map(str, cnv)))

if benchmark_file.endswith('SNPs_1.txt') or benchmark_file.endswith('SNPs_2.txt'):
    filter_snps(benchmark_file)
elif benchmark_file.endswith('INDELs_1.txt') or benchmark_file.endswith('INDELs_2.txt'):
    filter_indels(benchmark_file)
elif benchmark_file.endswith('CNV_restuls.txt'):
    filter_cnv_results(benchmark_file)
elif benchmark_file.endswith('CNV_stdresults.txt'):
    filter_cnv_std_restuls(benchmark_file)
