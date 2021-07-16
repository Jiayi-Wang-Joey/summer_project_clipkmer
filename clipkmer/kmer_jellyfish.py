import subprocess
import tempfile
from datetime import datetime
import os
import csv

os.chdir('/Users/apple/Desktop/Summer_project/dataset/')

def jellyfish_count(filename = str,length = int):
    command = subprocess.run(
        ['jellyfish','count','-m',str(length),'-t','4','-s','1G',filename],
        capture_output=True,
        check = True
        )

    count_command = subprocess.run(
        ["jellyfish","dump","-c","-t","-o","kmer_counts.tsv","mer_counts.jf"],
        capture_output=True,
        check=True
    )

    kmer_count = {}
    with open("kmer_counts.tsv","r") as f:
        tsvreader = csv.reader(f, delimiter = "\t")
        for row in tsvreader:
            kmer_count[row[0]] = row[1]
    
    return kmer_count
    

def jellyfish_stats():
    kmer_stats = subprocess.check_output(
        ["jellyfish","stats","mer_counts.jf"],
        universal_newlines=True
        )
    kmer_stats = kmer_stats.split('\n')
    stats_result = []
    for string in kmer_stats:
        string = string.split(' ')
        stats_result.append(string[-1])
    
    stats_result.remove('')
    stats_result = [ int(x) for x in stats_result ]

    return stats_result

def jellyfish_histo():
    histo_command = subprocess.check_output(["jellyfish","histo","-o","kmer_histo.tsv","mer_counts.jf"],
    universal_newlines=True
    )
    
    histo_output = {}
    with open("kmer_histo.tsv","r") as f:
        tsvreader = csv.reader(f, delimiter = " ")
        for row in tsvreader:
            histo_output[int(row[0])] = int(row[1])
    
    return histo_output


if __name__ == "__main__":
    start_time = datetime.now()
    filename = input("Enter the input fastq file directory: ")
    length = int(input("Enter the kmer length: "))
    kmer_count = jellyfish_count(filename,length)
    stats_result = jellyfish_stats()
    histo_output = jellyfish_histo()
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))