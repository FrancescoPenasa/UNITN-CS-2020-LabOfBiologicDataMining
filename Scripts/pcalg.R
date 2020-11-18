if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("graph")
BiocManager::install("pcalg")
BiocManager::install("Rgraphviz")
BiocManager::install("Rgraphviz")

setwd("D:/scuola/QCB/Secondo anno/Data Mining/Project/UNITN-CS-2020-LabOfBiologicDataMining/Scripts")

gitUrl <- "https://raw.githubusercontent.com/msdslab/pcalg/master/datasets/"

# Dataset loading - change 1.csv into your dataset of choice
dat <- read.csv("../Files/pcalg_input.csv")
suffStat <- list(C = cor(dat), n = nrow(dat))

library(pcalg)

res <- pc(suffStat, labels = names(dat),
          indepTest = gaussCItest, # the type of independence test
          alpha = 0.01) # the alpha level of the independence test
plot(res)

G <- res@graph

library(graph)
edges = edges(G)
nodes = nodes(G)

labels = as.data.frame(cbind(nodes,nodes))
names(labels) <- c("Id","Label")

network = data.frame()
names(network) <- c("Source","Target")
for(node in names(edges)){
  
  for(n in edges[[node]]){
    temp <- data.frame(node,n)
    names(temp) <- c("from","to")
    network = rbind(network,temp)
  }
}

write.csv(labels,"../Files/labels_pc.csv",row.names = FALSE)
write.csv(network,"../Files/net_pc.csv",row.names = FALSE)
