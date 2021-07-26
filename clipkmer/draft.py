def jellyfish_shuffled(filename,length):
    random.seed(100)
    total_shuffled_dicts = []
    for i in range(0,100):
        with tempfile.NamedTemporaryFile(mode='wt',delete=False,suffix='.fasta') as shuffled_file:
            for record in SeqIO.parse(filename, "fastq"):
                SeqIO.write(record.id, shuffled_file, 'fasta')
                SeqIO.write()
                shuffled_file.write(''.join(random.sample(str(record.seq),len(str(record.seq)))))
            
            temp_jf = jellyfish_count(shuffled_file.name,length)
            each_shuffled_dict = jellyfish_dump(temp_jf)
            total_shuffled_dicts.append(each_shuffled_dict)
            shuffled_file.close()
        print(total_shuffled_dicts)
        
    return total_shuffled_dicts

def jellyfish_shuffled(filename,length):
    random.seed(100)
    total_shuffled_dicts = []
    with open(filename, "r") as file:
        file_content = file.readlines()
        for i in range(0,100):
            with tempfile.NamedTemporaryFile(mode='wt',delete=False,suffix='.fa') as shuffled_file:
                for j in range(len(file_content)):
                    if file_content[j].startswith('@'):
                        shuffled_file.write(file_content[j].replace('@','>'))
                        shuffled_file.write(''.join(random.sample(file_content[j],len(file_content[j]))))
                    
                        
                temp_jf = jellyfish_count(shuffled_file.name,length)
                stats = jellyfish_stats(temp_jf)
                each_shuffled_dict = jellyfish_dump(temp_jf)
                total_shuffled_dicts.append(each_shuffled_dict)
                shuffled_file.close()
                print(stats)
                print(total_shuffled_dicts)
            file.close()
        
    return total_shuffled_dicts

    def jellyfish_shuffled(filename,length):
    random.seed(100)
    total_shuffled_dicts = []
    for i in range(0,100):
        with tempfile.NamedTemporaryFile(mode='wt',delete=False,suffix='.fasta') as shuffled_file:
            for record in SeqIO.parse(filename, "fastq"):
                shuffled_file.write(">"+record.id + "\n")
                shuffled_file.write(''.join(random.sample(str(record.seq),len(str(record.seq)))) + "\n")
            print(shuffled_file.name)
            temp_jf = jellyfish_count(shuffled_file.name,length)
            each_shuffled_dict = jellyfish_dump(temp_jf)
            total_shuffled_dicts.append(each_shuffled_dict)
            shuffled_file.close()
            print(total_shuffled_dicts)
        
    return total_shuffled_dicts