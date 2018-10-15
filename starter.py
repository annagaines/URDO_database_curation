#!/storage/anaconda3/bin/python
import os
import re
import subprocess 
primer_file = "inSilicoPCR_file.txt"
####I need to make this a function to read the primer file which returns the dictionary of dictionaries 
primers = open(primer_file, 'r').read()
entries = [x for x in primers.split('\n') if len(x) != 0]
primer_dict = {}
i = 0 
for entry in entries:
    i += 1
    key = f"primer_{i}"
    primer_name =  re.sub(pattern = ' ', string = entry.split("\t")[0].rstrip(), repl = '_')
    organism = entry.split("\t")[1].rstrip()
    taxa = entry.split("\t")[2].rstrip()
    forward_primer_seq = entry.split("\t")[3].rstrip()
    reverse_comp_primer_seq = entry.split("\t")[4].rstrip()
    primer_dict[key] = {'primer_name':primer_name, 
                        'organism':organism, 
                        'taxa':taxa, 
                        'forward_primer_seq':forward_primer_seq,
                        'reverse_comp_primer_seq': reverse_comp_primer_seq}
###This take the dictionary created after reading the primer file and creates the primer fasta file
file_out = "../primer_file.txt"
with open(file_out, 'w') as out_file:
    for key in primer_dict:
        out_file.write(">{primer_name}_F\n{forward_primer_seq}\n>{primer_name}_RC\n{reverse_comp_primer_seq}\n".format(**primer_dict[key]))

####This needs to take the organism from the primer file and download the genome from NCBI if it is bacteria
for key in primer_dict:
    #print(primer_dict[key]['taxa'])
    if int(primer_dict[key]['taxa']) == 1:
        ncbi_genome_download_cmd = 'ncbi-genome-download -g "{organism}" -F fasta bacteria'.format(**primer_dict[key])
        print(ncbi_genome_download_cmd)
        #os.system(ncbi_genome_download_cmd)
         
###
    