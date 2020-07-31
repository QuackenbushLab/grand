d=read.csv('./Downloads/otterLiver2.txt',header=F)
genes=read.csv('./Downloads/expressed_genes_liver.txt',header=F,sep='\t')
tfs  =read.csv('./Downloads/expressed_tf_names_liver.txt',header=F)
rownames(d)= t(tfs)
colnames(d)= t(genes)
write.csv(d,'./Downloads/cancer_liver_otter_network.csv',row.names=T,col.names=T)


