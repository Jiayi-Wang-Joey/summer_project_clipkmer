import unittest
def kmer_frequency(sequence = str, length = int):
    frequence = []
    for i in range(0,len(sequence)-length+1):
        fragment = sequence[i:i+length]
        count = sequence.count(fragment)
        frequence.append(count)
    max_frequence = max(frequence)
    return max_frequence

test_sequence1 = "ATCGATCGATCGATCGATCGATCG" # kmer sequence 4, max frequence = 6
test_sequence2 = "AAAAAAAAAA" # kmer sequence 1, max frequence = 10
test_sequence3 = "ATCCGATCCGATCCG" # kmer sequence 5, max frequence = 3

class test(unittest.TestCase):
    def test_kmer_frequency(self):
        self.assertTrue(kmer_frequency(test_sequence1,4) == 6)
        self.assertTrue(kmer_frequency(test_sequence2,1) == 10)
        self.assertTrue(kmer_frequency(test_sequence3,5) == 3)
    
if __name__ == "__main__":
    unittest.main()