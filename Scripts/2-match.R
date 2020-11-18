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
up <- read.csv("../Files/genes_up_regulate.csv", header = TRUE)
down <- read.csv("../Files/genes_down_regulate.csv", header = TRUE)

# union of the genes
df <- rbind(up, down)

# sort 
df <- df[order(df$V2,decreasing = TRUE),]

# remove duplicates
m <- duplicated(df$V1)
df_unique <- df[!m,]

v = c(1:nrow(df_unique))
plot(v[1:200],df_unique[1:200,2],xlab="ranked genes",ylab="significance",type="p",main="Genes significance distribution")

# select the first one hundres
my_sample <- df_unique[1:100,] 

# save
write.csv(my_sample, "../Files/most_significant_genes_h1n1.csv", row.names = FALSE)
