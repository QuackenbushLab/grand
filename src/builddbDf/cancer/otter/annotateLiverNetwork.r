d=read.csv('./Downloads/otterLiverTumor.csv',header=F)
genes=read.csv('./Downloads/expressed_genes_liverTumor_otter.txt',header=F,sep='\t')
tfs  =read.csv('./Downloads/expressed_tf_names_liverTumor_otter.txt',header=F)
rownames(d)= t(tfs)
colnames(d)= t(genes)
write.csv(d,'./Downloads/nets/cancer_liver_otter_network.csv',row.names=T,col.names=T)


d=read.csv('./Downloads/otterCervixTumor.csv',header=F)
genes=read.csv('./Downloads/expressed_genes_cervixTumor_otter.txt',header=F,sep='\t')
tfs  =read.csv('./Downloads/expressed_tf_names_cervixTumor_otter.txt',header=F)
rownames(d)= t(tfs)
colnames(d)= t(genes)
write.csv(d,'./Downloads/nets/cancer_cervix_otter_network.csv',row.names=T,col.names=T)


