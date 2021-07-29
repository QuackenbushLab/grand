var recuerdaAgentes = introJs();
recuerdaAgentes.setOptions({
    showStepNumbers: true,
  });
$('#MSL-initialize-tour').on('click', function(e){
    recuerdaAgentes.start();
});

var recuerdaAgentes2 = introJs();
recuerdaAgentes2.setOptions({
    showStepNumbers: true,
    steps: [
        {
            element: '#step1',
            intro: 'Targeting scores are a useful network summary metric that allows to perform downstream analyses such as functional enrichment analysis. The first step consists of computing these score.',
        },
        {
            element: '#step2',
            intro: 'The number of genes to be plotted can be selected using this slider.',
        },
        {
            element: '#step3',
            intro: 'Just like network visualization, these genes can be selected by largest or smallest targeting scores, using either their signed values or absolute values.',
        },
        {
            element: '#step4',
            intro: 'Genes can be selected specifically by entering their symbols or ids in this box.',
        },
        {
            element: '#step5',
            intro: 'Or by specifiying a pathway selected from Gene Ontology biological processes.',
        },
        {
            element: '#step6',
            intro: 'Finally, genes can be selected by the GWAS trait they are involved in, as determined in the GWAS catalog.',
        },
        {
            element: '#step7',
            intro: 'The number of TFs can be selected too by either absolute or signed values.',
        },
        {
            element: '#btnFetchTar',
            intro: 'Clicking submit allows to compute the targeting scores based on the selected parameters.',
        },
        {
            element: '#step9',
            intro: 'Targeting scores will be plotted as barplots in this panel.',
        },
        {
            element: '#step10',
            intro: 'The second step is to use these targeting scores to perform additional analyses integrated in GRAND.',
        },
        {
            element: '#btnenrich',
            intro: 'The first one is TF enrichment analysis. Clicking the TF button allows to send targeting results to TF enrichment tool.',
        },
        {
            element: '#step12',
            intro: 'The second one in drug repurposing using CLUEreg which finds drugs that reverse a TF or gene targeting scores. Clicking this button specifies that the analysis will be done on TF targeting score.',
        },
        {
            element: '#step13',
            intro: 'Clicking the by gene button performs the analysis on the gene targeting scores.',
        },
        {
            element: '#btnFetchTarclue',
            intro: 'Clicking CLUEreg sends the data to the corresponding page with prefilled forms.',
        },
        {
            element: '#step15',
            intro: 'Finally, the targeting scores are presented in this table and can be downloaded for additional analyses.',
        },
    ]   
  });
$('#MSL-initialize-tour2').on('click', function(e){
    recuerdaAgentes2.start();
});


var recuerdaAgentes3 = introJs();
recuerdaAgentes3.setOptions({
    showStepNumbers: true,
    steps: [
        {
            element: '#step0',
            intro: 'The first step starts by selecting two networks to compare and evaluate for diffrential targeting analysis. Network 1 can be a normal tissue and network 2 a cancer tissue, but the selection can be done to compare two cancer tissues or two normal tissues.',
        },
        {
            element: '#step1',
            intro: 'Targeting scores are a useful network summary metric that allows to perform downstream analyses such as functional enrichment analysis. The first step consists of computing these score.',
        },
        {
            element: '#step2',
            intro: 'The number of genes to be plotted can be selected using this slider.',
        },
        {
            element: '#step3',
            intro: 'Just like network visualization, these genes can be selected by largest or smallest targeting scores, using either their signed values or absolute values.',
        },
        {
            element: '#step4',
            intro: 'Genes can be selected specifically by entering their symbols or ids in this box.',
        },
        {
            element: '#step5',
            intro: 'Or by specifiying a pathway selected from Gene Ontology biological processes.',
        },
        {
            element: '#step6',
            intro: 'Finally, genes can be selected by the GWAS trait they are involved in, as determined in the GWAS catalog.',
        },
        {
            element: '#step7',
            intro: 'The number of TFs can be selected too by either absolute or signed values.',
        },
        {
            element: '#btnFetchTar',
            intro: 'Clicking submit allows to compute the targeting scores based on the selected parameters.',
        },
        {
            element: '#step9',
            intro: 'Targeting scores will be plotted as barplots in this panel.',
        },
        {
            element: '#step10',
            intro: 'The second step is to use these targeting scores to perform additional analyses integrated in GRAND.',
        },
        {
            element: '#btnenrich',
            intro: 'The first one is TF enrichment analysis. Clicking the TF button allows to send targeting results to TF enrichment tool.',
        },
        {
            element: '#step12',
            intro: 'The second one in drug repurposing using CLUEreg which finds drugs that reverse a TF or gene targeting scores. Clicking this button specifies that the analysis will be done on TF targeting score.',
        },
        {
            element: '#step13',
            intro: 'Clicking the by gene button performs the analysis on the gene targeting scores.',
        },
        {
            element: '#btnFetchTarclue',
            intro: 'Clicking CLUEreg sends the data to the corresponding page with prefilled forms.',
        },
        {
            element: '#step15',
            intro: 'Finally, the targeting scores are presented in this table and can be downloaded for additional analyses.',
        },
    ]   
  });
$('#MSL-initialize-tour3').on('click', function(e){
    recuerdaAgentes3.start();
});


var recuerdaAgentes4 = introJs();
recuerdaAgentes4.setOptions({
    showStepNumbers: true,
    steps: [
        {
            element: '#up-tab',
            intro: 'First, the network file representing the adjacency matrix has to be uploaded in this tab.',
        },
        {
            element: '#net-tab',
            intro: 'Then, the file will be passed on to network visualization.',
        },
        {
            element: '#tar-tab',
            intro: 'Finally, targeting scores will be computed and used for additional analyses.',
        },
        {
            element: '#astep4',
            intro: 'In this tab, a network file of 500mb maximum can be uploaded using theis button.',
        },
        {
            element: '#astep5',
            intro: 'An example file is provided here.',
        },
        {
            element: '#astep6',
            intro: 'Finally, clicking upload will send the file to the server and display its name. The visualization and targeting tabs can be used now that the file has been uploaded.',
        }
    ]   
  });
  $('#MSL-initialize-tour4').on('click', function(e){
    recuerdaAgentes4.start();
});

var recuerdaAgentes5 = introJs();
recuerdaAgentes5.setOptions({
    showStepNumbers: true,
  });
$('#MSL-initialize-tour5').on('click', function(e){
    recuerdaAgentes5.start();
});