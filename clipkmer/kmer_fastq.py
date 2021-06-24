# Before run this code, please unzip the fastq file. 
def read_sequence(filename):
    with open(filename, "r") as file, open(output_file, "w") as sequences: 
        file_content = file.readlines()
        for i in range(len(file_content)):
            if file_content[i].startswith("@"):
                sequences.writelines(file_content[i+1])
    
    return output_file

def kmer_frequency(output_file, length):
    output_dict = {}
    with open(output_file, 'r') as sequences:
        for line in sequences:
            # Save the kmer frequency for each sequence
            line_dict = {}
            for i in range(0,len(line)-length+1):
                fragment = line[i:i+length]
                count = line.count(fragment)
                line_dict[fragment] = count
            
            # Add the kmer frequency in each sequence to the total dictionary 
            for key in line_dict:
                if key in output_dict.keys():
                    output_dict[key] = output_dict[key] + line_dict[key]
                else:
                    output_dict[key] = line_dict[key]

    # What if the kmer length is longer than the single sequence length in fastq file?
    # 
    return output_dict

        

if __name__ == '__main__':
    filename = input("Enter the input fastq file directory: ")
    output_file = input("Enter the output file name: ")
    read_sequence(filename)
    length = int(input("Enter the kmer length: "))
    kmer_frequency(output_file,length)