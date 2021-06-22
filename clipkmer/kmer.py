# define a function to define the frequency of a certain length of fragment in a DNA sequence 
def kmer_frequency():
    filename = input("Please enter your sequence file (including directory): ")
    # define the kmer length
    length = int(input("Please enter kmer length: "))
    with open(filename,'r') as file:
        sequence = file.read()
        sequence = sequence.replace("\n","")
        output = {}
        for i in range(0,len(sequence)-length+1):
            fragment = sequence[i:i+length]
            count = sequence.count(fragment)
            output[fragment] = count
        print(output)
        



if __name__ == '__main__':
    kmer_frequency()