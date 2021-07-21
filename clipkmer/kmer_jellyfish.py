import subprocess
from sys import stdout
import tempfile
from datetime import datetime
import os
import csv
import random

os.chdir('/Users/apple/Desktop/Summer_project/dataset/')

def jellyfish_count(filename,length):
    # Use the jellyfish count command to generate the jf file for further analysis
    with tempfile.NamedTemporaryFile(mode="wt", delete=False) as out_f:
        command_result = subprocess.run(['jellyfish','count','-m',str(length),'-t','4','-s','1G','-o',out_f.name,filename],
        check=True,
        stdout = out_f
        )
        jf = out_f.name
        out_f.close()
        return jf

def jellyfish_dump(jf):
    # Use the jf file to generate a dictionary that contains the counts of each kmer
    with tempfile.NamedTemporaryFile(mode="wt",delete=False,suffix='.tsv') as kmer_tsv:
        count_command = subprocess.run(
            ["jellyfish","dump","-c","-t","-o",kmer_tsv.name,jf],
            check = True,
            stdout = kmer_tsv
        )
        kmer_tsv.close()
        
    kmer_count = {}
    with open(kmer_tsv.name,"r") as f:
        tsvreader = csv.reader(f, delimiter = "\t")
        for row in tsvreader:
            kmer_count[row[0]] = row[1]
    print(len(kmer_count))
    return kmer_count
    

def jellyfish_stats(jf):
    # Use the jf file to get the statistics of the kmer counts
    kmer_stats = subprocess.check_output(
        ["jellyfish","stats",jf],
        universal_newlines=True
        )
    
    kmer_stats = kmer_stats.split('\n')
    stats_result = []
    for string in kmer_stats:
        string = string.split(' ')
        stats_result.append(string[-1])
    
    stats_result.remove('')
    stats_result = [ int(x) for x in stats_result ]
    
    # stats_result is a list that contains Unique, Distinct, Total and Max. 
    return stats_result

def jellyfish_histo(jf):
    # Use the jf file to get a dictonary of the histogram data: {kmer count: the count of this kmer-count}
    with tempfile.NamedTemporaryFile(mode = "wt", delete = False, suffix = ".tsv") as histo:
        histo_command = subprocess.run(
            ["jellyfish","histo","-o",histo.name,jf],
            check = True,
            stdout = histo
        )
        histo.close()

    histo_output = {}
    with open(histo.name,"r") as f:
        tsvreader = csv.reader(f, delimiter = " ")
        for row in tsvreader:
            histo_output[int(row[0])] = int(row[1])
   
    return histo_output

def jellyfish_shuffled(filename,length):
    random.seed(100)
    total_shuffled_dicts = []
    for i in range(0,100):
        with open(filename, "r") as file, tempfile.NamedTemporaryFile(mode='wt',delete=False,suffix='.fq') as shuffled_file:
            file_content = file.readlines()
            for j in range(len(file_content)-3):
                if file_content[j].startswith('A') or file_content[j].startswith('T') or file_content[j].startswith('C') or file_content[j].startswith('G'):
                    shuffled_file.write(''.join(random.sample(file_content[j],len(file_content[j]))))
                else:
                    shuffled_file.write(file_content[j])
                    
            each_shuffled_dict = jellyfish_count('tempfile.fq',length)
            total_shuffled_dicts.append(each_shuffled_dict)
            file.close()
            shuffled_file.close()
        
    
    
    return total_shuffled_dicts

          

if __name__ == "__main__":
    start_time = datetime.now()
    filename = input("Enter the input fastq file directory: ")
    length = int(input("Enter the kmer length: "))
    jf = jellyfish_count(filename,length)
    jellyfish_dump(jf)
    jellyfish_stats(jf)
    jellyfish_histo(jf)
    jellyfish_shuffled(filename,length)
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))