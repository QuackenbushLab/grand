load('AgNetCell.mat')
load('gtNetCell.mat')
exp_file = 'Hugo_exp1_lcl.txt';
disp('Reading in expression data!');
tic
a=readtable(exp_file,'FileType','text');
Exp = a{:,2:end};
GeneNames = a{:,1};
[NumGenes, NumConditions] = size(a);
motif_file = 'Hugo_motifCellLine.txt';
disp('Reading in motif data!');
tic
    [TF, gene, weight] = textread(motif_file, '%s%s%f');
    TFNames = unique(TF);
    NumTFs  = length(TFNames);
    [~,i]   = ismember(TF, TFNames);
    [~,j]   = ismember(gene, GeneNames);
    commonInd = i&j;
    i = i(commonInd);
    j = j(commonInd);
    weight = weight(commonInd);
    RegNet  = zeros(NumTFs, NumGenes);
    RegNet(sub2ind([NumTFs, NumGenes], i, j)) = weight;
    fprintf('%d TFs and %d edges!\n', NumTFs, length(weight));
toc
% reduce RegNet    
gt        = readtable('ENCODE_ChIP-seq.gmt','FileType','text','Delimiter','\t','ReadVariableNames',false);
% Fetch network
edgeIndex = find(cellfun(@(x) contains(x,'_GM12878_HG19'), gt{:,1}));
% Build gtFNames
TFpos     = cellfun(@(x) strfind(x,'_GM12878_HG19'), gt{:,1}, 'UniformOutput', false);

TFpos     = TFpos(~cellfun('isempty',TFpos));
gtTFNames = cell(length(TFpos),1);
% Set ground truth gene names
for i=1:length(edgeIndex)
    a            = gt{edgeIndex(i),1};
    gtTFNames{i} = a{1}(1:TFpos{i}-1);
end

gtf         = gt{edgeIndex,:};

% reduce predicted and gt network 
[commonTFs, ipredTF, igtTFs] = intersect(TFNames ,gtTFNames);
RegNet1 = RegNet(ipredTF,:);
%%
motif_file = 'motif_complete_reduced.txt';
disp('Reading in motif data!');
tic
    [TF, gene, weight] = textread(motif_file, '%s%s%f');
    TFNames = unique(TF);
    NumTFs  = length(TFNames);
    [~,i]   = ismember(TF, TFNames);
    [~,j]   = ismember(gene, GeneNames);
    commonInd = i&j;
    i = i(commonInd);
    j = j(commonInd);
    weight = weight(commonInd);
    RegNet  = zeros(NumTFs, NumGenes);
    RegNet(sub2ind([NumTFs, NumGenes], i, j)) = weight;
    fprintf('%d TFs and %d edges!\n', NumTFs, length(weight));
toc

% reduce predicted and gt network 
[commonTFs2, ipredTF, igtTFs] = intersect(TFNames ,gtTFNames);
RegNet2 = RegNet(ipredTF,:);
%%
indChip1 = logical(AgNetCell{1});
indMotif1= logical(RegNet1);
figure;
subplot(1,2,1)
hold on;
h1=histogram(gtNetCell{1})
h2=histogram(gtNetCell{1}(indChip1))
xlabel('Edge weight','fontsize',18)
ylabel('Distribution','fontsize',18)
title('Chip-seq','fontsize',18)
legend('PANDA','Chip-seq')
set(gca,'FontSize',18);
h1.FaceColor = 'b';
h1.EdgeColor = 'none';
h2.FaceColor = 'r';
h2.EdgeColor = 'none';
subplot(1,2,2)
hold on;
h1=histogram(gtNetCell{1})
h2=histogram(gtNetCell{1}(indMotif1))
xlabel('Edge weight','fontsize',18)
ylabel('Distribution','fontsize',18)
title('Motif','fontsize',18)
legend('PANDA','motif')
set(gca,'FontSize',18);
h1.FaceColor = 'b';
h1.EdgeColor = 'none';
h2.FaceColor = 'r';
h2.EdgeColor = 'none';
%%
% plot roc curve for motif
[x,y,t,auc]=perfcurve(RegNet1(:),gtNetCell{1}(:),1);
figure;
plot(x,y,'LineWidth',2)
xlabel('False positive rate','fontsize',18)
ylabel('True positive rate','fontsize',18)
set(gca,'FontSize',18);
title('Prediction of motif from PANDA','fontsize',18)
%%
indChip6 = logical(AgNetCell{6});
figure;
subplot(1,2,1)
hold on;
h1=histogram(gtNetCell{6})
h2=histogram(gtNetCell{6}(indChip6))
xlabel('Edge weight')
ylabel('Distribution')
title('Chip-seq')
legend('PANDA','Chip-seq')
set(gca,'FontSize',18);
h1.FaceColor = 'b';
h1.EdgeColor = 'none';
h2.FaceColor = 'r';
h2.EdgeColor = 'none';
subplot(1,2,2)
hold on;
h1=histogram(gtNetCell{6})
h2=histogram(gtNetCell{6}(indMotif1))
xlabel('Edge weight')
ylabel('Distribution')
title('Motif')
legend('PANDA','motif')
set(gca,'FontSize',18);
h1.FaceColor = 'b';
h1.EdgeColor = 'none';
h2.FaceColor = 'r';
h2.EdgeColor = 'none';
%%
% plot roc curve for motif
[x,y,t,auc]=perfcurve(RegNet2(:),gtNetCell{6}(:),1);
figure;
plot(x,y,'LineWidth',2)
xlabel('False positive rate','fontsize',18)
ylabel('True positive rate','fontsize',18)
set(gca,'FontSize',18);
title('Prediction of motif from PANDA','fontsize',18)