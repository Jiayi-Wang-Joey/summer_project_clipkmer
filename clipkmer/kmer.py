# define a function to define the frequency of a certain length of fragment in a DNA sequence 
def read_sequence(filename):
    with open(filename,'r') as file:
        sequence = file.read()
        sequence = sequence.replace("\n","")
    return sequence

def kmer_frequency(sequence,length):
    output = {}
    for i in range(0,len(sequence)-length+1):
        fragment = sequence[i:i+length]
        count = sequence.count(fragment)
        output[fragment] = count
    print(output)
    return output
        



if __name__ == '__main__':
    filename = input("Enter the file directory: ")
    sequence = read_sequence(filename)
    length = int(input("Enter the kmer length: "))
    kmer_frequency(sequence,length)