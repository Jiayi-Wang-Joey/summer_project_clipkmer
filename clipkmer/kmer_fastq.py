# Before run this code, please unzip the fastq file. 
import random

def read_sequence(filename):
    with open(filename, "r") as file: 
        sequence = []
        file_content = file.readlines()
        for i in range(len(file_content)):
            if file_content[i].startswith("@"):
                sequence.append(file_content[i+1])
    return sequence

def kmer_frequency(sequence, length):
    output_dict = {}
    
    for line in sequence:
        # Save the kmer frequency for each sequence
        line_dict = {}
        used_counts = 0
        skipped_counts = 0
        if len(line) >= length:
            for i in range(0,len(line)-length+1):
                fragment = line[i:i+length]
                count = line.count(fragment)
                line_dict[fragment] = count
                
            # Add the kmer frequency in each sequence to the total dictionary 
            for key in line_dict:
                if key in output_dict.keys():
                    output_dict[key] += line_dict[key]
                else:
                    output_dict[key] = line_dict[key]
                
            used_counts += 1

        else:
            print("Warning: The kmer length is longer than nucleotide sequence")
            skipped_counts += 1
    
    return output_dict

def shuffled_sequence(sequence, kmer_sequence):
    random.seed(100)
    kmer_counts = []
    
    for i in range(0,100):
        count = 0

        for line in sequence:
            shuffled_line = ''.join(random.sample(line,len(line)))

            if len(line) >= length:
                for i in range(0,len(shuffled_line)-length+1):
                    count += shuffled_line.count(kmer_sequence)

            else:
                print("Warning: The kmer length is longer than nucleotide sequence")

        kmer_counts.append(count)

    print(kmer_counts)
    return kmer_counts

if __name__ == '__main__':
    filename = input("Enter the input fastq file directory: ")
    sequence = read_sequence(filename)
    length = int(input("Enter the kmer length: "))
    kmer_sequence = input("Enter the kmer sequence: ") # The same length as the input length
    shuffled_sequence(sequence,kmer_sequence)