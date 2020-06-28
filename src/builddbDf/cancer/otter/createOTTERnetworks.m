function createOTTERnetworks()

w0l = importdata('priorLiver.csv');
w0b = importdata('priorBreast.csv');
w0c = importdata('priorCervix.csv');
c1 = readtable('tcga_breast_TPM_otter.txt','ReadRowNames',true);
c2 = readtable('tcga_cervix_TPM_otter.txt','ReadRowNames',true);
c3 = readtable('tcga_liver_TPM_otter.txt','ReadRowNames',true);
cl = corrcoef(c3{:,:}');
cc = corrcoef(c2{:,:}');
cb = corrcoef(c1{:,:}');
p = importdata('ppi.csv');


wb = otter(w0b,p,cb);
wc = otter(w0c,p,cc);
wl = otter(w0l,p,cl);

% 1. networks from the paper
c11 = readtable('otterBreast2.txt','ReadRowNames',false);
c22 = readtable('otterCervix2.txt','ReadRowNames',false);
%c33 = readtable('otterLiver2.txt','ReadRowNames',false); %fails to read (Failed to convert character code.)
%had to do it in R

% relative error
max(max(c11{:,:} ./ wb)) %==1
max(max(c22{:,:} ./ wc)) %==1


% resave expression as .csv with labels
breastsamples= readtable('breast_samples','Delimiter','\t','PreserveVariableNames',1);
cervixsamples= readtable('cervix_samples','Delimiter','\t','PreserveVariableNames',1);
liversamples= readtable('liver_samples','Delimiter','\t','PreserveVariableNames',1);
c1 = readtable('cancer_breast_expression_tcga.txt','ReadRowNames',true);
c2 = readtable('cancer_cervix_expression_tcga.txt','ReadRowNames',true);
c3 = readtable('cancer_liver_expression_tcga.txt','ReadRowNames',true);
c1.Properties.VariableNames=breastsamples.Properties.VariableNames(2:end);
c2.Properties.VariableNames=cervixsamples.Properties.VariableNames(2:end);
c3.Properties.VariableNames=liversamples.Properties.VariableNames(2:end);

writetable(c1,'cancer_breast_expression_tcga.csv','Delimiter',',','WriteVariableNames',true,'WriteRowNames',true); 
writetable(c2,'cancer_cervix_expression_tcga.csv','Delimiter',',','WriteVariableNames',true,'WriteRowNames',true); 
writetable(c3,'cancer_liver_expression_tcga.csv','Delimiter',',','WriteVariableNames',true,'WriteRowNames',true); 

% resave networks as .csv with labels

end