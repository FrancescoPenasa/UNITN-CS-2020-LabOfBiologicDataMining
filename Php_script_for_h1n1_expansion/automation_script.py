# imports
import os 


# read result files
for file in os.listdir("h1n1_expansion/"):
	os.system("php anno-hsf5.php h1n1_expansion/" + file)
	print(file)
