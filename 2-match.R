## ---------------------------
##
## Script name: match
##
## Purpose of script: match covid and influeza genes and extracted the ones that don't match
##
## Authors: Gabriele Berrera and Francesco Penasa
##
## Date Created: 2020/10/24
##
## Email: francesco.penasa-1@studenti.unitn.it, gabriele.berrera@studenti.unitn.it
##
## ---------------------------
##
## Notes:
##   
##
## ---------------------------

# read extracted data
up <- read.csv("genes_up_regulate.csv", header = TRUE)
down <- read.csv("genes_down_regulate.csv", header = TRUE)

# union of the genes
df <- rbind(up, down)

# import covid csv
covid <- read.csv("genes_covid.csv", header = TRUE )
covid_genes <- covid$gene_name

# sort 
df <- df[order(df$V2,decreasing = TRUE),]

# remove duplicates
m <- duplicated(df$V1)
df_unique <- df[!m,]

# match and exclude matched results
excluded <- df_unique[!(df_unique$V1 %in% covid$gene_name),]

# select the first one hundres
my_sample <- excluded[1:100,] 

# save
write.csv(my_sample, "exclusive_genes.csv", row.names = FALSE)
