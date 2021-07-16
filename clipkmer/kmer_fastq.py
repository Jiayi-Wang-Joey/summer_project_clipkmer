# Before run this code, please unzip the fastq file. 
from os import stat
import random
from datetime import datetime
import scipy
import numpy as np
from numpy.core.defchararray import count
from numpy.core.fromnumeric import mean
import statistics
from collections import Counter
from numpy import array


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
    mean_of_counts = array([values for values in output_dict.values()]).mean()
    median_of_counts = statistics.median(list(output_dict.values()))
    max_kmer = dict(Counter(output_dict).most_common(1))
    max_kmer = list(max_kmer.values())[0]
    one_count_kmer = 0
    for key in output_dict.keys():
        if output_dict[key] == 1:
            one_count_kmer += 1
    one_kmer_proportion = one_count_kmer/len(output_dict)
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

def shuffled_stat(total_dicts):
    shuffled_mean = []
    shuffled_mid = []
    shuffled_max = []
    shuffled_one_count_kmer = []
    shuffled_one_count_proportion = []
    for dicts in total_dicts:
        mean_of_counts, median_of_counts, max_kmer, one_count_kmer, one_kmer_proportion = stat_kmer(dicts)
        shuffled_mean.append(mean_of_counts)
        shuffled_mid.append(median_of_counts)
        shuffled_max.append(list(max_kmer.values())[0])
        shuffled_one_count_kmer.append(len(one_count_kmer))
        shuffled_one_count_proportion.append(one_kmer_proportion)
    
    shuffled_mean = np.mean(np.array(shuffled_mean))
    shuffled_mid = np.mean(np.array(shuffled_mid))
    shuffled_max = np.mean(np.array(shuffled_max))
    shuffled_one_count_kmer = np.mean(np.array(shuffled_one_count_kmer))
    shuffled_one_count_proportion = np.mean(np.array(shuffled_one_count_proportion))

    return shuffled_mean, shuffled_mid, shuffled_max, shuffled_one_count_kmer, shuffled_one_count_proportion

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
    

def kmer_enrichment(total_dicts,output_dict):
    p_value = {}
    for key in output_dict.keys():
        count = 0
        for dicts in total_dicts:
            if key in dicts.keys() and dicts[key] >= output_dict[key]:
                count += 1
        
        p_value[key] = count/100

    return p_value

if __name__ == '__main__':
    start_time = datetime.now()
    filename = input("Enter the input fastq file directory: ")
    sequence = read_sequence(filename)
    length = int(input("Enter the kmer length: "))
    total_dicts = shuffled_sequence(sequence,length)
    kmer_sequence = input("Enter the kmer sequence: ")
    kmer_counts = kmer_count(total_dicts,kmer_sequence)
    output_dict = kmer_frequency(sequence, length)
    mean_of_counts, median_of_counts, max_kmer, one_count_kmer, one_kmer_proportion = stat_kmer(output_dict)
    mean_values, upper_CI, lower_CI = counts_mean_CI(total_dicts, confidence = 0.95)
    p_value = kmer_enrichment(total_dicts,output_dict)
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))