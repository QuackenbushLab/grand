#files=c('artery_tibial','artery_coronary','artery_aorta','adrenal_gland','adipose_visceral_omentum','adipose_subcutaneous')
#larger machine remaining = 'brain_0','muscle_skeletal','skin','whole_blood'
#files=c('brain_1','brain_2','breast_mammary_tissue')
#files=c('esophagus_muscularis','esophagus_mucosa','esophagus_gastroesophageal_junction','colon_transverse','colon_sigmoid')
#files=c('heart_atrial_appendage','heart_left_ventricle','liver','lung','muscle_skeletal','nerve_tibial')
#files=c('pancreas','pituitary','skin','small_intestine_terminal_ileum','spleen','stomach')
#files=c('small_intestine_terminal_ileum','spleen','stomach')
#files=c('thyroid','whole_blood')
files=c('skin','whole_blood','muscle_skeletal')
for (file in files){
  print(file)
  load(paste0(file,'.RData'))
  print(dim(net))
  write.csv(net,paste0(file,'.csv'))
  net=''
}

# Nsamples
# artery_tibial             19476492      357
# artery_coronary           19476492      140
# "artery_aorta"           19476492      247
# "adrenal_gland"          19476492      159
# "adipose_visceral_omentum" 19476492      234
# "adipose_subcutaneous"     19476492      380

# "brain_1"
# 19476492      254
# "brain_2"
# 19476492      360
# "breast_mammary_tissue"
# 19476492      217

#[1] "esophagus_muscularis"
#[1] 19476492      283
#[1] "esophagus_mucosa"
#[1] 19476492      330
#[1] "esophagus_gastroesophageal_junction"
#[1] 19476492      176
#[1] "colon_transverse"
#[1] 19476492      203
#[1] "colon_sigmoid"
#[1] 19476492      173

#[1] "heart_atrial_appendage"
#[1] 19476492      217
#[1] "heart_left_ventricle"
#[1] 19476492      267
#[1] "liver"
#[1] 19476492      137
#[1] "lung"
#[1] 19476492      360
#[1] "nerve_tibial"
#[1] 19476492      334


#[1] "pancreas"
#[1] 19476492      193
#[1] "pituitary"
#[1] 19476492      124


#[1] "small_intestine_terminal_ileum"
#[1] 19476492      104
#[1] "spleen"
#[1] 19476492      118
#[1] "stomach"
#[1] 19476492      204

#[1] "thyroid"
#[1] 19476492      355

#[1] "brain_0"
#[1] 19476492      779

#[1] "skin"
#[1] 19476492      661
#[1] "whole_blood"
#[1] 19476492      444
#[1] "muscle_skeletal"
#[1] 19476492      469

#Missing: 
#fibroblast
#lymphoblast
#kidney cortex
#minor salivary gland
#ovary
#prostate
#testis
#uterus
#vagina






# Nsamples
# artery_tibial             19476492      357
# artery_coronary           19476492      140
# "artery_aorta"           19476492      247
# "adrenal_gland"          19476492      159
# "adipose_visceral_omentum" 19476492      234
# "adipose_subcutaneous"     19476492      380


totalSamples = 254 + 360 + 217 + 283 + 330 + 176 + 203 + 173 + 217 + 267 + 137 + 360 + 334 + 193 + 124 + 104 + 118 + 204 + 355 + 779 + 661 + 444 + 469 + 380 +234 +159 +247 +140 +357






