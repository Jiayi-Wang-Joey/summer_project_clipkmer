# Before run this code, please unzip the fastq file. 
import random
from datetime import datetime

def read_sequence(filename):
    with open(filename, "r") as file: 
        sequence = []
        file_content = file.readlines()
        for i in range(len(file_content)):
            if file_content[i].startswith("@"):
                sequence.append(file_content[i+1].strip('\n'))
    return sequence

def kmer_frequency(sequence, length):
    output_dict = {}
    # sequence = list(filter(lambda sequence: len(sequence) >= length, sequence))
    sequence = sequence[:100000]
    for line in sequence:
        # Save the kmer frequency for each sequence
        line_dict = {}
            
        for i in range(0,len(line)-length+1):
            fragment = line[i:i+length]
            if fragment in line_dict.keys():
                line_dict[fragment] += 1
            else:
                line_dict.setdefault(fragment, 1)
            # line_dict[fragment] += 1 if fragment in line_dict.keys() else line_dict.setdefault(fragment, 1)
                
            # Add the kmer frequency in each sequence to the total dictionary 
        for key in line_dict:
            if key in output_dict.keys():
                output_dict[key] += line_dict[key]
            else:
                output_dict[key] = line_dict[key]
                
    return output_dict

def shuffled_sequence(sequence, length):
    random.seed(100)
    filtered_sequence = list(filter(lambda sequence: len(sequence) >= length, sequence))
    skipped_sequence_number = len(sequence) - len(filtered_sequence)
    print(f'Warning: Skipped {skipped_sequence_number} sequences')
    
    filtered_sequence = filtered_sequence[:100000]
    total_dicts = []
    
    for i in range(0,100):
        new_sequence = []
        for line in filtered_sequence:
            shuffled_line = ''.join(random.sample(line,len(line)))
            new_sequence.append(shuffled_line)
        
        output_dict = kmer_frequency(new_sequence, length)
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
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))