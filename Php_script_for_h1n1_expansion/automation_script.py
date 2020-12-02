# imports
import os 

os.system("cp ../Data/h1n1_expansion ./ -r")

# read result files
for file in os.listdir("h1n1_expansion/"):
	os.system("php anno-hsf5.php h1n1_expansion/" + file)
	print(file)

os.system("mkdir results")
os.system("mv *.csv results/")
os.system("mv results/anno-hsf5.csv anno-hsf5.csv")
os.system("rm h1n1_Hs_.csv")
print(os.system("ls -l results | wc -l"))