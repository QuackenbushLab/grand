library('stringr')
setwd('/Users/mab8354/granddb/src')
load('GTEx_PANDA_tissues.RData')

# Initialize dataframe
nTissues = dim(net)[2]
tissues  = colnames(net)
# Convert tissue name to capital letter for compatibility with gtex
nTFs = dim(net)[1]/dim(genes)[1]
k=0
for(tissue in tissues){
    k=k+1
    pos=gregexpr('_', tissue)
    for(i in 1:length(pos[[1]])){
        posi=pos[[1]][i]
        if(posi != -1){
            substr(tissue, posi+1, posi+1) <- toupper(substr(tissue, posi+1, posi+1)) 
            tissues[k] = tissue
        }
    }
}
cols = c('tissue','tissueLink','tool','netzoo','netzooLink','netzooRel','network','ppi','ppiLink','motif','expression','expLink','tfs','genes','refs')
df <- data.frame(matrix(ncol = length(cols), nrow = nTissues))
colnames(df) = cols

# resave networks
setwd('/Users/mab8354/granddb/networks')
for(i in 1:nTissues){
    d = net[,i]
    d <- matrix(d, nrow = nTFs, byrow = TRUE)
    rownames(d) = edges$TF[1:nTFs]
    colnames(d) = unique(edges$Gene)
    write.csv(d,paste0(tissues[i],".csv"))
}

# build vectors
expLinkVec = vector()
networkVec = vector()
for(i in 1:nTissues){
    expLinkVec = c(expLinkVec, paste0("https://gtexportal.org/home/eqtls/tissue?tissueName=", tissues[i]))
    networkVec = c(networkVec, paste0("https://granddb.s3.amazonaws.com/tissues/networks/",tissues[i], '.csv'))
}
tissueVec     = colnames(net)
tissueLinkVec = expLinkVec 
toolVec       = rep("PANDA", nTissues)
netzooVec     = rep("netZooM", nTissues)
netzooLinkVec = rep("https://github.com/netZoo/netZooM/releases", nTissues)
netzooRelVec  = rep("0.1", nTissues)
#networkVec    = rep("https://granddb.s3.amazonaws.com/tissues/networks/GTEx_PANDA_tissues.RData", nTissues)
ppiVec        = rep("https://granddb.s3.amazonaws.com/tissues/ppi/tissues_ppi.txt", nTissues)
ppiLinkVec    = rep("http://string90.embl.de/", nTissues)
motifVec      = rep("https://granddb.s3.amazonaws.com/tissues/motif/tissues_motif.txt", nTissues)
expressionVec = rep("https://granddb.s3.amazonaws.com/tissues/expression/tissues_expression.txt", nTissues)
#expLinkVec    = 
tfsVec        = rep(nTFs, nTissues)
genesVec      = rep(dim(genes)[1], nTissues)
refsVec       = rep("https://www.cell.com/cell-reports/fulltext/S2211-1247(17)31418-3?_returnURL=https%3A%2F%2Flinkinghub.elsevier.com%2Fretrieve%2Fpii%2FS2211124717314183%3Fshowall%3Dtrue", nTissues)
refsVec2      = rep("https://zenodo.org/record/838734", nTissues)

# Populate df
df['tissue']     = tissueVec
df['tissueLink'] = tissueLinkVec
df['tool']       = toolVec
df['netzoo']     = netzooVec
df['netzooLink'] = netzooLinkVec
df['netzooRel']  = netzooRelVec
df['network']    = networkVec
df['ppi']        = ppiVec
df['ppiLink']    = ppiLinkVec
df['motif']      = motifVec
df['expression'] = expressionVec
df['expLink']    = tissueLinkVec
df['tfs']        = tfsVec
df['genes']      = genesVec
df['refs']       = refsVec
df['refs2']      = refsVec2

# Save to csv
setwd('/Users/mab8354/granddb/')
write.csv(df,"tissues.csv",row.names = FALSE)