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

% resave PPI as .csv with labels
breasttfs= readtable('expressed_tf_names_breast.txt','Delimiter','\t','PreserveVariableNames',1,'ReadVariableNames',false);
cervixtfs= readtable('expressed_tf_names_cervix.txt','Delimiter','\t','PreserveVariableNames',1,'ReadVariableNames',false);
livertfs = readtable('expressed_tf_names_liver.txt','Delimiter','\t','PreserveVariableNames',1,'ReadVariableNames',false);
PPI=array2table(p, 'VariableNames', breasttfs{:,1},'RowNames',breasttfs{:,1});
writetable(PPI,'cancer_breast_otter_ppi.csv','Delimiter',',','WriteVariableNames',true,'WriteRowNames',true); 
writetable(PPI,'cancer_cervix_otter_ppi.csv','Delimiter',',','WriteVariableNames',true,'WriteRowNames',true); 
writetable(PPI,'cancer_liver_otter_ppi.csv','Delimiter',',','WriteVariableNames',true,'WriteRowNames',true); 

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

%%
% Resave expression samples with TCGA sample ID
tbl1=readtable('cancer_breast_expression_tcga.csv','Delimiter',','); 
tbl2=readtable('cancer_cervix_expression_tcga.csv','Delimiter',','); 
tbl3=readtable('cancer_liver_expression_tcga.csv','Delimiter',','); 

tbl3varNames = readtable('metadata_liver_07202020','Delimiter',','); 
tbl3.Properties.VariableNames(2:end) = tbl3varNames.gdc_cases_samples_portions_analytes_aliquots_submitter_id;
writetable(tbl3,'cancer_liver_expression_tcga.csv','Delimiter',',','WriteVariableNames',true,'WriteRowNames',true); 

tbl2varNames = readtable('metadata_cervix_07202020','Delimiter',','); 
tbl2.Properties.VariableNames(2:end) = tbl2varNames.gdc_cases_samples_portions_analytes_aliquots_submitter_id;
writetable(tbl2,'cancer_cervix_expression_tcga.csv','Delimiter',',','WriteVariableNames',true,'WriteRowNames',true);

tbl1varNames = readtable('metadata_breast_07202020','Delimiter',','); 
%resolve duplicates
[a,b]=unique(tbl1varNames.gdc_cases_samples_portions_analytes_aliquots_submitter_id);
indNonUnique = setdiff(1:height(tbl1varNames),b);
j=0;
for termi = indNonUnique
    term=tbl1varNames.gdc_cases_samples_portions_analytes_aliquots_submitter_id(termi);
    term=[term{1},'-',num2str(j)];
    j=j+1;
    tbl1varNames.gdc_cases_samples_portions_analytes_aliquots_submitter_id(termi) = {term};
end
tbl1.Properties.VariableNames(2:end) = tbl1varNames.gdc_cases_samples_portions_analytes_aliquots_submitter_id;
writetable(tbl1,'cancer_breast_expression_tcga.csv','Delimiter',',','WriteVariableNames',true,'WriteRowNames',true);
%%
% resave networks as .csv with labels
genesB= readtable('expressed_genes_breast.txt','Delimiter','\t','PreserveVariableNames',1,'ReadVariableNames',false);
genesC= readtable('expressed_genes_cervix.txt','Delimiter','\t','PreserveVariableNames',1,'ReadVariableNames',false);
cb = readtable('otterBreast2.txt','ReadRowNames',false);
cc = readtable('otterCervix2.txt','ReadRowNames',false);
%cl = readtable('otterLiver2.txt','ReadRowNames',false); %fails to read (Failed to convert character code.)
%had to do it in R annotateLiverNetwork.r
cb.Properties.VariableNames = genesB{:,1};
cb.Properties.RowNames = breasttfs{:,1};
cc.Properties.VariableNames = genesC{:,1};
cc.Properties.RowNames = cervixtfs{:,1};
writetable(cb,'cancer_breast_otter_network.csv','Delimiter',',','WriteVariableNames',true,'WriteRowNames',true); 
writetable(cc,'cancer_cervix_otter_network.csv','Delimiter',',','WriteVariableNames',true,'WriteRowNames',true); 

% Annotate motif
cb = readtable('cancer_breast_expression_tcga.csv','ReadRowNames',true);
cc = readtable('cancer_cervix_expression_tcga.csv','ReadRowNames',true);
cl = readtable('cancer_liver_expression_tcga.csv','ReadRowNames',true);
w0b=array2table(w0b, 'VariableNames', cb.Properties.RowNames,'RowNames',breasttfs{:,1});
w0c=array2table(w0c, 'VariableNames', cc.Properties.RowNames,'RowNames',cervixtfs{:,1});
w0l=array2table(w0l, 'VariableNames', cl.Properties.RowNames,'RowNames',livertfs{:,1});
writetable(w0b,'cancer_breast_otter_motif.csv','Delimiter',',','WriteVariableNames',true,'WriteRowNames',true); 
writetable(w0c,'cancer_cervix_otter_motif.csv','Delimiter',',','WriteVariableNames',true,'WriteRowNames',true); 
writetable(w0l,'cancer_liver_otter_motif.csv','Delimiter',',','WriteVariableNames',true,'WriteRowNames',true);

end