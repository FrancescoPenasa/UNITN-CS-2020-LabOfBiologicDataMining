# imports
import csv
import os 

gene_list = []
gene_trans_list = []

# extract gene names 
with open('../most_significant_genes_h1n1.csv', mode = 'r') as file:
	csvFile = csv.reader(file)

	for line in csvFile:
		gene_list.append(line[0]) 

# exec the cmd for every gene name
for gene in gene_list:
	cmd = "php make.php " + gene
	os.system(cmd)

# mv results in a new folder
os.system("mkdir isoforms")
os.system("mv *.lgn isoforms/")


# read result files
for file in os.listdir("isoforms/"):
    with open("isoforms/" + file, mode='r') as reader:
        gene_file = reader.readlines()
        gene_trans_list.append(gene_file[1])


# create the dst csv
os.system("touch all_genes.csv")

# write the results on a single file
with open('all_genes.csv', mode = 'a') as writer:
    writer.write("from,to\n");
    for line in gene_trans_list:
        writer.write(line)

