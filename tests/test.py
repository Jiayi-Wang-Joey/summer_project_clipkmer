import unittest
from kmer import read_sequence, kmer_frequency
test_sequence1 = read_sequence("/Users/apple/Desktop/file1.txt") #AAAAA, kmer length = 1, {'A':5}
test_sequence2 = read_sequence("/Users/apple/Desktop/file2.txt") #ATCGATCG, kmer length = 4, {'ATCG':2, 'TCGA':1, 'CGAT':1, 'GATC': 1}

class test(unittest.TestCase):
    def test_kmer_sequence(self):
        self.assertTrue(kmer_frequency(test_sequence1,1)) == {'A': 5}
        self.assertTrue(kmer_frequency(test_sequence2,4)) == {'ATCG': 2, 'TCGA': 1, 'CGAT': 1, 'GATC': 1}

if __name__ == "__main__":
    unittest.main()