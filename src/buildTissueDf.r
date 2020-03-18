library('stringr')
setwd('/Users/mab8354/granddb/src/')
load('GTEx_PANDA_tissues.RData')

generateExpression=1
generateNetworks=0
countSamples=1

# Initialize dataframe
nTissues = dim(net)[2]
tissues  = colnames(net)
tissues2 = tissues
notInLionessTissues2=c('Ovary','Prostate','Testis','Uterus','Vagina','Kidney_cortex','Minor_salivary_gland')
indnotInLionessTissues2=which(tissues2 %in% notInLionessTissues2)
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
df <- data.frame(matrix(ncol = length(cols), nrow = nTissues+nTissues-length(indnotInLionessTissues2)))
colnames(df) = cols

# Resave tissues expression
iterExp=0
nSamples = vector()
if(generateExpression){
    setwd('/Users/mab8354/granddb/expression')
    for(tissue in tissues2){
        iterExp=iterExp+1
        indTissue = which(samples[,2] == tissue)
        matTissue = exp[,indTissue]
        write.csv(matTissue,paste0(tissues[iterExp],".csv"))
        nSamples=c(nSamples,length(indTissue))
    }
}

# resave networks
if(generateNetworks){
    setwd('/Users/mab8354/granddb/networks')
    for(i in 1:nTissues){
        d = net[,i]
        d <- matrix(d, nrow = nTFs, byrow = TRUE)
        rownames(d) = edges$TF[1:nTFs]
        colnames(d) = unique(edges$Gene)
        write.csv(d,paste0(tissues[i],".csv"))
    }
}

# build vectors
expLinkVec = vector()
networkVec = vector()
networkVec2 = vector()
expressionVec = vector()
for(i in 1:nTissues){
    expLinkVec = c(expLinkVec, paste0("https://gtexportal.org/home/eqtls/tissue?tissueName=", tissues[i]))
    networkVec = c(networkVec, paste0("https://granddb.s3.amazonaws.com/tissues/networks/",tissues[i], '.csv'))
    expressionVec = c(expressionVec, paste0("https://granddb.s3.amazonaws.com/tissues/expression/",tissues[i], '.csv'))
    networkVec2 = c(networkVec2, paste0("https://granddb.s3.amazonaws.com/tissues/networks/lioness/",tissues[i],'_AllSamples','.csv'))
}
tissueVec     = colnames(net)
tissueVec2    = setdiff(tissueVec,notInLionessTissues2)
tissueLinkVec = expLinkVec 
toolVec1       = rep("PANDA", nTissues)
toolVec2       = rep("LIONESS", nTissues-length(indnotInLionessTissues2))
netzooVec     = rep("netZooM", nTissues)
netzooVec2     = rep("netZooM", nTissues-length(indnotInLionessTissues2))
netzooLinkVec = rep("https://github.com/netZoo/netZooM/releases", nTissues)
netzooLinkVec2 = rep("https://github.com/netZoo/netZooM/releases", nTissues-length(indnotInLionessTissues2))
netzooRelVec  = rep("0.1", nTissues)
#networkVec    = rep("https://granddb.s3.amazonaws.com/tissues/networks/GTEx_PANDA_tissues.RData", nTissues)
ppiVec        = rep("https://granddb.s3.amazonaws.com/tissues/ppi/tissues_ppi.txt", nTissues)
ppiLinkVec    = rep("http://string90.embl.de/", nTissues)
motifVec      = rep("https://granddb.s3.amazonaws.com/tissues/motif/tissues_motif.txt", nTissues)
motifVec2      = rep("https://granddb.s3.amazonaws.com/tissues/motif/tissues_lioness_motif.txt", nTissues)
#expressionVec = rep("https://granddb.s3.amazonaws.com/tissues/expression/tissues_expression.txt", nTissues)
#expLinkVec    = 
tfsVec        = rep(nTFs, nTissues)
genesVec      = rep(dim(genes)[1], nTissues)
refsVec1      = rep("https://www.cell.com/cell-reports/fulltext/S2211-1247(17)31418-3?_returnURL=https%3A%2F%2Flinkinghub.elsevier.com%2Fretrieve%2Fpii%2FS2211124717314183%3Fshowall%3Dtrue", nTissues)
refsVec11     = rep("https://www.biorxiv.org/content/10.1101/082289v1.full", nTissues)
refsVec2      = rep("https://zenodo.org/record/838734", nTissues)

# Populate df
df['tissue']     = c(tissueVec,tissueVec[-indnotInLionessTissues2])
df['tissueLink'] = c(tissueLinkVec,tissueLinkVec[-indnotInLionessTissues2])
df['tool']       = c(toolVec1,toolVec2)
df['netzoo']     = c(netzooVec,netzooVec2)
df['netzooLink'] = c(netzooLinkVec,netzooLinkVec2)
df['netzooRel']  = c(netzooRelVec,netzooRelVec[-indnotInLionessTissues2])
df['network']    = c(networkVec,networkVec2[-indnotInLionessTissues2])
df['ppi']        = c(ppiVec,ppiVec[-indnotInLionessTissues2])
df['ppiLink']    = c(ppiLinkVec,ppiLinkVec[-indnotInLionessTissues2])
df['motif']      = c(motifVec,motifVec2[-indnotInLionessTissues2])
df['expression'] = c(expressionVec,expressionVec[-indnotInLionessTissues2])
df['expLink']    = c(tissueLinkVec,tissueLinkVec[-indnotInLionessTissues2])
df['tfs']        = c(tfsVec,tfsVec[-indnotInLionessTissues2])
df['genes']      = c(genesVec,genesVec[-indnotInLionessTissues2])
df['samples']    = c(nSamples,nSamples[-indnotInLionessTissues2])
df['refs']       = c(refsVec1,refsVec11[-indnotInLionessTissues2])
df['refs2']      = c(refsVec2,rep('',nTissues-length(indnotInLionessTissues2)))

# Save to csv
setwd('/Users/mab8354/granddb/')
write.csv(df,"tissueslanding.csv",row.names = FALSE)

cols = c('tissue','nnets')
df2 <- data.frame(matrix(ncol = length(cols), nrow = nTissues))
colnames(df2) = cols
df2['tissue']     = c(tissueVec)
nsamples=rep(2,length(tissues))
nsamples[indnotInLionessTissues2]=1
df2['nnets']      = nsamples
write.csv(df2,"tissues.csv",row.names = FALSE)
#s3:// could not download so I switched to https://granddb.s3.amazonaws.com


