# Before run this code, please unzip the fastq file. 
import random
from datetime import datetime
import numpy as np
from numpy.core.fromnumeric import mean
import scipy.stats
import statistics
from collections import Counter


def read_sequence(filename):
    with open(filename, "r") as file:  
        sequence = []
        file_content = file.readlines()
        for i in range(len(file_content)):
            if file_content[i].startswith("@"):
                sequence.append(file_content[i+1].strip('\n'))
    sequence = sequence[:10000]
    return sequence

def kmer_frequency(sequence, length):
    output_dict = {}
    sequence = list(filter(lambda sequence: len(sequence) >= length, sequence))
    for line in sequence:
        # Save the kmer frequency for each sequence
        line_dict = {}
            
        for i in range(0,len(line)-length+1):
            fragment = line[i:i+length]
            line_dict.setdefault(fragment, 0)
            line_dict[fragment] += 1
            # Add the kmer frequency in each sequence to the total dictionary 

        for key in line_dict:
            if key in output_dict.keys():
                output_dict[key] += line_dict[key]
            else:
                output_dict[key] = line_dict[key]
                
    return output_dict

def stat_kmer(output_dict):
    mean_of_counts = np.mean(np.array(output_dict.values()))
    median_of_counts = statistics.median(list(output_dict.values()))
    max_kmer = dict(Counter(output_dict).most_common(10))
    one_count_kmer = {}
    for key,value in output_dict.items():
        if output_dict[key] == 1:
            one_count_kmer[key] = output_dict[key]
    
    one_kmer_proportion = len(one_count_kmer)/len(output_dict)
    
    return mean_of_counts, median_of_counts, max_kmer, one_count_kmer, one_kmer_proportion


def shuffled_sequence(sequence, length):
    random.seed(100)
    filtered_sequence = list(filter(lambda sequence: len(sequence) >= length, sequence))
    skipped_sequence_number = len(sequence) - len(filtered_sequence)
    print(f'Warning: Skipped {skipped_sequence_number} sequences')
    
    total_dicts = []
    for i in range(0,100):
        new_sequence = []
        for line in filtered_sequence:
            shuffled_line = ''.join(random.sample(line,len(line)))
            new_sequence.append(shuffled_line)
        
        output_dict = kmer_frequency(new_sequence,length)
        total_dicts.append(output_dict)
    
    return total_dicts

def kmer_count(total_dicts,kmer_sequence):
    kmer_counts = []
    for dicti in total_dicts:
        if kmer_sequence in dicti.keys():
            kmer_counts.append(dicti[kmer_sequence])
        else:
            kmer_counts.append(0) 
    
    return kmer_counts

def counts_mean_CI(total_dicts, confidence = 0.95):

    total_counts = []
    for dicti in total_dicts:
        total_counts.append(list(dicti.values()))
    
    all_counts_dict = {}
    for each_shuffled_counts in total_counts:
        for value in each_shuffled_counts:
            all_counts_dict.setdefault(value, [])
        
    for key in all_counts_dict.keys():
        for each_shuffled_counts in total_counts:
            all_counts_dict[key].append(each_shuffled_counts.count(key))
    
    mean_values = {}
    upper_CI = {}
    lower_CI = {}
    
    for key in all_counts_dict.keys():
        a = 1.0 * np.array(all_counts_dict[key])
        n = len(a)
        m, sd = np.mean(a), scipy.stats.sem(a)
        h = sd * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
        mean_values[key] = m
        upper_CI[key] = m + h
        lower_CI[key] = m - h

    return mean_values, upper_CI, lower_CI

if __name__ == '__main__':
    start_time = datetime.now()
    filename = input("Enter the input fastq file directory: ")
    sequence = read_sequence(filename)
    length = int(input("Enter the kmer length: "))
    total_dicts = shuffled_sequence(sequence,length)
    kmer_sequence = input("Enter the kmer sequence: ")
    kmer_counts = kmer_count(total_dicts,kmer_sequence)
    print(kmer_counts)
    output_dict = kmer_frequency(sequence, length)
    print(output_dict[kmer_sequence])
    mean_values, upper_CI, lower_CI = counts_mean_CI(total_dicts, confidence = 0.95)
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))