## ---------------------------
##
## Script name: df_extractions
##
## Purpose of script: extract up and down regulated genes from dataframe
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

# === CONSTANTS === #
GENE <- "GSE40844"


# === UP_GENES === #
up_genes <- "Virus_Perturbations_from_GEO_up"

geo <- read.table(up_genes, header = FALSE, fill = TRUE )

# find all with GENE
mask <- grepl(GENE, geo$V3)
geo_GENE <- subset(geo, mask)

# clean useless columns
geo_GENE <- geo_GENE[,c(-1,-2,-3)]

# put genes in a list
list_genes <- list()
list_genes <- apply(geo_GENE, 2, function(x) append(list_genes, x) )
list_genes <- do.call(c, list_genes)

# transform in dataframe
genes_matrix <- sapply(list_genes, function(x) unlist(strsplit(x, ",", fixed=TRUE)))
genes_matrix <- t(genes_matrix)
genes_df <- as.data.frame(genes_matrix)

# sort 
df <- genes_df[order(genes_df$V2,decreasing = TRUE),]

# remove duplicates 
m <- duplicated(df$V1)
d <- df[!m,]

# save
write.csv(d, "genes_up_regulate.csv", row.names = FALSE)




# === DOWN_GENES === #
down_genes <- "Virus_Perturbations_from_GEO_down"

geo <- read.table(down_genes, header = FALSE, fill = TRUE )

# find all with GENE
mask <- grepl(GENE, geo$V3)
geo_GENE <- subset(geo, mask)

# clean useless columns
geo_GENE <- geo_GENE[,c(-1,-2,-3)]

# put genes in a list
list_genes <- list()
list_genes <- apply(geo_GENE, 2, function(x) append(list_genes, x) )
list_genes <- do.call(c, list_genes)

# transform in dataframe
genes_matrix <- sapply(list_genes, function(x) unlist(strsplit(x, ",", fixed=TRUE)))
genes_matrix <- t(genes_matrix)
genes_df <- as.data.frame(genes_matrix)

# sort 
df <- genes_df[order(genes_df$V2,decreasing = TRUE),]

# remove duplicates 
m <- duplicated(df$V1)
d <- df[!m,]

# save
write.csv(d, "genes_down_regulate.csv", row.names = FALSE)

