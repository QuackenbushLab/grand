load('/Users/mab8354/granddb/src/builddbDf/cancer/lioness_pdac.RData')

df=read.csv('/Users/mab8354/granddb/static/data/pancreas_tcga.csv')

colnames(lioness_pdac)[3:length(colnames(lioness_pdac))] = df['gdc_cases.samples.portions.analytes.aliquots.submitter_id'][2:dim(df['gdc_cases.samples.portions.analytes.aliquots.submitter_id'])[1],1]
write.csv(lioness_pdac,'Pancreas_cancer_AllSamples.txt')

nTissues=dim(df)[1]
offset=2
k=1
nTFs=length(unique(lioness_pdac[,1]))
tissues=colnames(lioness_pdac)[3:length(colnames(lioness_pdac))]
for(i in (1+offset):nTissues){
  d = lioness_pdac[,i]
  d <- matrix(d, nrow = nTFs, byrow = TRUE)
  rownames(d) = lioness_pdac[1:nTFs,1]
  colnames(d) = unique(lioness_pdac[,2])
  write.csv(d,paste0(tissues[k],".csv"))
  system(paste0('aws s3 cp ',tissues[k],'.csv s3://granddb/cancer/pancreas_cancer/networks/lioness/ --profile shared'))
  system(paste0('rm ', tissues[k], '.csv'))
  k=k+1
}