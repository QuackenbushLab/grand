a=readtable('motif.txt');
varNames=unique(a.Var2);
rowNames=unique(a.Var1);
tblNet=array2table(AgNet, 'VariableNames', varNames','RowNames', rowNames);
writetable(tblNet,'gbm_cancer_TCGA1.csv','WriteVariableNames',1,'WriteRowNames',1);

sampleOrder=readtable('sampleorder_fullnames.txt','ReadVariableNames',0);
expTbl=readtable('expression.txt','ReadRowNames',1);
expTbl.Properties.VariableNames=sampleOrder{:,:};
writetable(expTbl,'cancer_glioblastoma_d1_expression.txt','WriteVariableNames',1,'WriteRowNames',1);
%%
a=readtable('motif.txt');
varNames=unique(a.Var2);
rowNames=unique(a.Var1);
tblNet=array2table(AgNet, 'VariableNames', varNames','RowNames', rowNames);
writetable(tblNet,'gbm_cancer_TCGA2.csv','WriteVariableNames',1,'WriteRowNames',1);

sampleOrder=readtable('sampleorder_fullnames.txt','ReadVariableNames',0);
expTbl=readtable('expression.txt','ReadRowNames',1);
expTbl.Properties.VariableNames=sampleOrder{:,:};
writetable(expTbl,'cancer_glioblastoma_d2_expression.txt','WriteVariableNames',1,'WriteRowNames',1);
%%
a=readtable('motif.txt');
b=readtable('expression.txt','ReadRowNames',1);
varNames=b.Properties.RowNames;
rowNames=unique(a.Var1);
tblNet=array2table(AgNet, 'VariableNames', varNames','RowNames', rowNames);
writetable(tblNet,'gbm_cancer_ggn.csv','WriteVariableNames',1,'WriteRowNames',1);

sampleOrder=readtable('sampleorder.txt','ReadVariableNames',0);
expTbl=readtable('expression.txt','ReadRowNames',1);
expTbl.Properties.VariableNames=sampleOrder{:,:};
writetable(expTbl,'cancer_glioblastoma_v_expression.txt','WriteVariableNames',1,'WriteRowNames',1);