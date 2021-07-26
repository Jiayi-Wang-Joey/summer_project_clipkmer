from Bio import SeqIO
import os
from kmer_jellyfish import jellyfish_count, jellyfish_dump
from datetime import datetime
from gtfparse import read_gtf

os.environ['PATH'] += ':/Users/apple/bin'
os.chdir('/Users/apple/Desktop/Summer_project/dataset/')

def kmer_freq_posit(kmer_count,filename,length):
    total_freq_posit = []
    for record in SeqIO.parse(filename, "fasta"):
        each_freq_dict = {}
        seq = str(record.seq)
        for i in range(0,len(seq)-length+1):
            kmer = seq[i:i+length]
            if kmer in kmer_count.keys():
                each_freq_dict[i] = kmer_count[kmer]
            
        total_freq_posit.append(each_freq_dict)
    #print(total_freq_posit)
    return total_freq_posit

def exon_intron(gtf_file):
    exon_posit = []
    with open(gtf_file,'r') as f:
        lines = f.readlines()
        start = int(lines[0].split()[3])
        
        for line in lines:
            line = line.split('\t')
            if line[2] == 'exon':
                exon = {}
                exon_start = int(line[3]) - start
                exon_length =  int(line[4]) - int(line[3])
                exon_end = exon_start + exon_length
                exon[exon_start] = exon_end
                exon_posit.append(exon) 

    f.close()
    exon = []
    for dict1 in exon_posit:
        if dict1 not in exon:
            exon.append(dict1)

    return exon
            


if __name__ == "__main__":
    start_time = datetime.now()
    filename = input("Enter the input fastq file directory: ")
    length = int(input("Enter the kmer length: "))
    gtf_file = input("Enter the input gtf file directory: ")
    jf = jellyfish_count('RBFOX2.fa',length)
    kmer_count = jellyfish_dump(jf)
    kmer_freq_posit(kmer_count,filename,length)
    exon_intron(gtf_file)
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
        










