library('recount') # to process gene expression
colDataRse=colData(rse_gene) # rse_gene_breast.Rdata

setwd('/Users/mab8354/granddb/static/data')
databreast=read.csv('metadata_breast_01232021.csv')

a=databreast['gdc_cases.samples.portions.analytes.aliquots.submitter_id']

b=colDataRse@listData$gdc_cases.samples.portions.analytes.aliquots.submitter_id

indInter=match(a[,1], b)

#create new column
databreast$cgc_slide_percent_tumor_nuclei='NA'
databreast['cgc_slide_percent_necrosis']='NA'

#fill column
databreast['cgc_slide_percent_tumor_nuclei']=colDataRse@listData$cgc_slide_percent_tumor_nuclei[indInter]
databreast['cgc_slide_percent_necrosis']=colDataRse@listData$cgc_slide_percent_necrosis[indInter]

#write file
write.csv(databreast,'/Users/mab8354/granddb/static/data/metadata_breast_01292021.csv', row.names = FALSE)
