dataset='d1'
load(paste0('net',dataset,'.RData'))
generateNetworks=1
nTissues=dim(net)[2]
offset=2
nTFs=650
tissues = read.csv(paste0('sampleorder_fullnames',dataset,'.txt'),header=FALSE)
tissues=tissues[,1]
if(generateNetworks){
  k=1
  for(i in (1+offset):nTissues){
    d = net[,i]
    d <- matrix(d, nrow = nTFs, byrow = TRUE)
    rownames(d) = net[1:nTFs,1]
    colnames(d) = unique(net[,2])
    write.csv(d,paste0(tissues[k],".csv"))
    system(paste0('aws s3 cp ',tissues[k],'.csv s3://granddb/cancer/glioblastoma_cancer/networks/lioness/ --profile shared'))
    system(paste0('rm ', tissues[k], '.csv'))
    k=k+1
  }
}

# save full dataset
if(dataset=='v'){
  write.csv(net,'Gbm_cancer_GGN_AllSamples.txt')
}else if (dataset=='d1'){
  write.csv(net,'Gbm_cancer_TCGA1_AllSamples.txt')
}else if (dataset=='d2'){
  write.csv(net,'Gbm_cancer_TCGA2_AllSamples.txt') 
}
  
# annotate clinical data
rownames(clin) = tissues
write.csv(paste0(clin,'~/Downloads/GBM_',dataset,'_clinvar.csv'))