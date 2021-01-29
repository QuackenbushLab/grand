for tissue = {'breast','cervix','liver'}
    clear motif network ppi expression
    geneNames = readtable(['expressed_genes_' tissue{1} 'Tumor_otter.txt'],'ReadRowNames',...
                        false,'ReadVariableNames',false);

    tfNames = readtable(['expressed_tf_names_' tissue{1} 'Tumor_otter.txt'],'ReadRowNames',...
        false,'ReadVariableNames',false);
    motif = readtable(['motif_prior_matrix_', tissue{1},'Tumor_otter.txt']);
    
    if isequal(tissue{1},'breast')
        network = readtable(['otter' tissue{1} 'Tumor.csv'],'ReadRowNames',...
            false,'ReadVariableNames',false);
    end
    
    ppi = readtable(['PPI_matrix_' tissue{1} 'Tumor_otter.txt']);

    expression =readtable(['tcga_' tissue{1} 'Tumor_TPM_withHeader_otter.txt'],'PreserveVariableNames',1);

    size(motif)
    size(expression)
    %%
    %resave
    if isequal(tissue{1},'breast')
        network.Properties.VariableNames = geneNames.Var1;
        network.Properties.RowNames      = tfNames.Var1;
    end
    ppi.Properties.VariableNames     = tfNames.Var1;
    ppi.Properties.RowNames          = tfNames.Var1;
    motif.Properties.VariableNames   = tfNames.Var1; 
    motif.Properties.RowNames        = geneNames.Var1; 
    expression.Properties.RowNames   = geneNames.Var1;
    cd nets
    if isequal(tissue{1},'breast')
        writetable(network,['cancer_' tissue{1} '_otter_network'],'WriteRowNames',true,'WriteVariableNames',true);
    end
    writetable(ppi,['cancer_' tissue{1} '_otter_ppi'],'WriteRowNames',true,'WriteVariableNames',true);
    writetable(motif,['cancer_' tissue{1} '_otter_motif'],'WriteRowNames',true,'WriteVariableNames',true);
    writetable(expression,['cancer_' tissue{1} '_otter_expression'],'WriteRowNames',true,'WriteVariableNames',true);
    cd ..
end

