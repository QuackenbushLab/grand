library('stringr')
setwd('/Users/mab8354/granddb/src/')
load('../data/GTEx_PANDA_tissues.RData')

# 0. PANDA networks
generateExpression=1# Has to be on for Nsamples
generateNetworks=0

# Initialize dataframe
nTissues = dim(net)[2]
tissues  = colnames(net)
tissues2 = tissues
notInLionessTissues2=c('Lymphoblastoid_cell_line','Fibroblast_cell_line','Ovary','Prostate','Testis','Uterus','Vagina','Kidney_cortex','Minor_salivary_gland')
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
    setwd('/Users/mab8354/granddb/data/expression')
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
scriptVec = vector()
for(i in 1:nTissues){
    expLinkVec    = c(expLinkVec, paste0("https://gtexportal.org/home/eqtls/tissue?tissueName=", tissues[i]))
    networkVec    = c(networkVec, paste0("https://granddb.s3.amazonaws.com/tissues/networks/",tissues[i], '.csv'))
    expressionVec = c(expressionVec, paste0("https://granddb.s3.amazonaws.com/tissues/expression/",tissues[i], '.csv'))
    networkVec2   = c(networkVec2, paste0("https://granddb.s3.amazonaws.com/tissues/networks/lioness/",tissues[i],'_AllSamples','.csv'))
}               
tissueVec     = gsub('_',' ',colnames(net))
tissueVecWsc  = colnames(net)
tissueVec2    = setdiff(tissueVec,notInLionessTissues2)
tissueLinkVec = expLinkVec 
toolVec1      = rep("PANDA", nTissues)
toolVec2      = rep("PANDA-LIONESS", nTissues-length(indnotInLionessTissues2))
netzooVec     = rep("netZooM", nTissues)
netzooVec2    = rep("netZooM", nTissues-length(indnotInLionessTissues2))
netzooLinkVec = rep("https://github.com/netZoo/netZooM/releases", nTissues)
netzooLinkVec2= rep("https://github.com/netZoo/netZooM/releases", nTissues-length(indnotInLionessTissues2))
netzooRelVec  = rep("0.1", nTissues)
#networkVec   = rep("https://granddb.s3.amazonaws.com/tissues/networks/GTEx_PANDA_tissues.RData", nTissues)
ppiVec        = rep("https://granddb.s3.amazonaws.com/tissues/ppi/tissues_ppi.txt", nTissues)
ppiLinkVec    = rep("http://string90.embl.de/", nTissues)
motifVec      = rep("https://granddb.s3.amazonaws.com/tissues/motif/tissues_motif.txt", nTissues)
motifVec2     = rep("https://granddb.s3.amazonaws.com/tissues/motif/tissues_lioness_motif.txt", nTissues)
#expressionVec = rep("https://granddb.s3.amazonaws.com/tissues/expression/tissues_expression.txt", nTissues)
#expLinkVec    = 
tfsVec        = rep(nTFs, nTissues)
genesVec      = rep(dim(genes)[1], nTissues)
refsVec1      = rep("https://www.cell.com/cell-reports/fulltext/S2211-1247(17)31418-3?_returnURL=https%3A%2F%2Flinkinghub.elsevier.com%2Fretrieve%2Fpii%2FS2211124717314183%3Fshowall%3Dtrue", nTissues)
refsVec11     = rep("https://www.cell.com/cell-reports/fulltext/S2211-1247(20)30776-2#.XvKB22ciE0k", nTissues)
refsVec3      = rep("Sonawane et al. (2017)", nTissues)
refsVec33     = rep("Lopes-Ramos et al. (2020)", nTissues)
refsVec2      = rep("https://zenodo.org/record/838734", nTissues)
regVec        = rep("TF", nTissues)
motifDescVec  = rep("Motif", nTissues)

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
df['refs3']       = c(refsVec3,refsVec33[-indnotInLionessTissues2])
df['reg']        = c(regVec,regVec[-indnotInLionessTissues2])
df['motifDesc']  = c(motifDescVec,motifDescVec[-indnotInLionessTissues2])

cols = c('tissue','nnets')
df2 <- data.frame(matrix(ncol = length(cols), nrow = nTissues))
colnames(df2) = cols
df2['tissue']     = c(tissueVecWsc)
nsamples=rep(3,length(tissues))
nsamples[indnotInLionessTissues2]=2
df2['nnets']      = nsamples
setwd('/Users/mab8354/granddb/')
write.csv(df2,"data/tissues.csv",row.names = FALSE)
#s3:// could not download so I switched to https://granddb.s3.amazonaws.com

# 1.PUMA networks
#clear variables
exp=''
expTS=''
net=''
netTS=''
edges=''
samples =''
genes=''
pos=''
matTissue=''
# load new file
load('data/GTEx_PUMA_tissues.RData')
generateExpression=1 #have to be on
generateNetworks  =1

# Resave tissues expression
iterExp=0
nSamples = vector()
if(generateExpression){
    setwd('/Users/mab8354/granddb/data/expression')
    for(tissue in tissues2){
        iterExp=iterExp+1
        indTissue = which(samples[,2] == tissue)
        matTissue = exp[,indTissue]
        write.csv(matTissue,paste0(tissues[iterExp],"_PUMA.csv"))
        nSamples=c(nSamples,length(indTissue))
    }
}

# Resave miRanda networks
nMir=dim(unique(netM['miRNA']))[1]
b=unique(netM['Gene'])
if(generateNetworks){
    nMir=dim(unique(netM['miRNA']))[1]
    a=netM['miRNA']
    b=unique(netM['Gene'])
    setwd('/Users/mab8354/granddb/data/networks')
    for(i in 1:nTissues){
        d = netM[,tissues2[i]]
        d <- matrix(d, nrow = nMir, byrow = TRUE)
        rownames(d) = a[1:nMir,1] 
        colnames(d) = b[,1]
        write.csv(d,paste0(tissues[i],"_miRanda_PUMA.csv"))
    }
}

# Resave TargetScan networks
if(generateNetworks){
    nMir=dim(unique(netT['miRNA']))[1]
    a=netT['miRNA']
    b=unique(netT['Gene'])
    setwd('/Users/mab8354/granddb/data/networks')
    for(i in 1:nTissues){
        d = netT[,tissues2[i]]
        d <- matrix(d, nrow = nMir, byrow = TRUE)
        rownames(d) = a[1:nMir,1] 
        colnames(d) = b[,1]
        write.csv(d,paste0(tissues[i],"_TargetScan_PUMA.csv"))
    }
}

# Save miRanda regulation prior
d = netM[,c('miRNA','Gene','Prior')]
write.table(d,paste0("tissue_miRanda_prior.txt"),sep = "\t",row.names=FALSE,col.names=FALSE)

# Save TargetScan regulation prior
d = netT[,c('miRNA','Gene','Prior')]
write.table(d,paste0("tissue_TargetScan_prior.txt"),sep = "\t",row.names=FALSE,col.names=FALSE)

# build PUMA dataframe
cols = c('tissue','tissueLink','tool','netzoo','netzooLink','netzooRel','network','ppi','ppiLink','motif','expression','expLink','tfs','genes','refs')
df3 <- data.frame(matrix(ncol = length(cols), nrow = nTissues*2))
colnames(df3) = cols

# build vectors
expLinkVec = vector()
networkVec = vector()
networkVec2= vector()
expressionVec = vector()
for(i in 1:nTissues){
    expLinkVec = c(expLinkVec, paste0("https://gtexportal.org/home/eqtls/tissue?tissueName=", tissues[i]))
    networkVec = c(networkVec, paste0("https://granddb.s3.amazonaws.com/tissues/networks/puma/",tissues[i], '_miRanda_PUMA.csv'))
    networkVec2= c(networkVec2, paste0("https://granddb.s3.amazonaws.com/tissues/networks/puma/",tissues[i], '_TargetScan_PUMA.csv'))
    expressionVec = c(expressionVec, paste0("https://granddb.s3.amazonaws.com/tissues/expression/puma/",tissues[i], '_PUMA.csv'))
}              

tissueVec     = gsub('_',' ',colnames(netM)) #make sure to match tissues of netT (they do)  gsub('_',' ',colnames(netT)) == gsub('_',' ',colnames(netM)) 
tissueLinkVec = expLinkVec 
toolVec1      = rep("PUMA", nTissues)
netzooVec     = rep("netZooM", nTissues)
netzooLinkVec = rep("https://github.com/netZoo/netZooM/releases", nTissues)
netzooRelVec  = rep("0.3", nTissues)
ppiVec        = rep("-", nTissues)
ppiLinkVec    = rep("-", nTissues)
motifVecmir      = rep("https://granddb.s3.amazonaws.com/tissues/motif/tissue_MiRanda_prior.txt", nTissues)
motifVects      = rep("https://granddb.s3.amazonaws.com/tissues/motif/tissue_TargetScan_prior.txt", nTissues)
tfsVec        = rep(nMir, nTissues)
genesVec      = rep(dim(b)[1], nTissues)
refsVec1      = rep("https://academic.oup.com/bioinformatics/article/doi/10.1093/bioinformatics/btaa571/5858977", nTissues)
refsVec2      = rep("https://zenodo.org/record/1313768#.XvlUDpNKi_t", nTissues)
refsVec3      = rep("Kuijjer et al. (2020)", nTissues)
regVec        = rep("miRNA", nTissues)
motifDescVec  = rep("miRanda", nTissues)

# Populate df3
df3['tissue']     = c(tissueVec[4:41],tissueVec[4:41])
df3['tissueLink'] = c(tissueLinkVec,tissueLinkVec)
df3['tool']       = c(toolVec1,toolVec1)
df3['netzoo']     = c(netzooVec,netzooVec)
df3['netzooLink'] = c(netzooLinkVec,netzooLinkVec)
df3['netzooRel']  = c(netzooRelVec,netzooRelVec)
df3['network']    = c(networkVec,networkVec2)
df3['ppi']        = c(ppiVec,ppiVec)
df3['ppiLink']    = c(ppiLinkVec,ppiLinkVec)
df3['motif']      = c(motifVecmir,motifVects)
df3['expression'] = c(expressionVec,expressionVec)
df3['expLink']    = c(tissueLinkVec,tissueLinkVec)
df3['tfs']        = c(tfsVec,tfsVec)
df3['genes']      = c(genesVec,genesVec)
df3['samples']    = c(nSamples,nSamples)
df3['refs']       = c(refsVec1,refsVec1)
df3['refs2']      = c(refsVec2,refsVec2)
df3['refs3']      = c(refsVec3,refsVec3)
df3['reg']        = c(regVec,regVec)
df3['motifDesc']  = c(motifDescVec,rep("TargetScan", nTissues))

# Save to csv 
tt=rbind(df,df3)
for(i in 1:dim(tt)[1]){
    scriptVec=c(scriptVec,paste0('https://granddb.s3.amazonaws.com/tissues/scripts/reproducetissue', i, 'Network.m'))   
}
tt['script']= scriptVec
write.csv(tt,"../tissueslanding.csv",row.names = FALSE)
