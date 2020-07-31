netTypes={'cancer','tissue','cell','drug'};
for i=1:length(netTypes)
    switch netTypes{i}
        case 'cancer'
            tbl=readtable('cancerlanding.csv');
            tbl=readtable('cancerlanding.csv','Format',repmat('%s',1,size(tbl,2)));
            l=height(tbl);
        case 'tissue'
            tbl=readtable('tissueslanding.csv');
            tbl=readtable('tissueslanding.csv','Format',repmat('%s',1,size(tbl,2)));
            l=height(tbl);
        case 'cell'
            tbl=readtable('cells.csv');
            tbl=readtable('cells.csv','Format',repmat('%s',1,size(tbl,2)));
            l=height(tbl);
        case 'drug'
            tbl=readtable('drugslanding.csv','Delimiter',',','PreserveVariableNames',1);
            l=1;
    end
    
    for j=1:l
        netZoo     = tbl.netzoo{j};
        netZooVer  = tbl.netzooRel{j};
        netZooTool = tbl.tool{j};
        ppiLink    = tbl.ppi{j};
        motifLink  = tbl.motif{j};
        networkLink= tbl.network{j};
        expLink    = tbl.expression{j};

        filetext   = fileread('reproduceGrandNetwork.m');
        addText=['netZoo     = ''' netZoo ''';' newline 'netZooVer  = ''' netZooVer ''';' ...
            newline 'netZooTool = ''' netZooTool ''';' newline 'ppiLink    = ''' ...
            ppiLink ''';' newline 'motifLink  = ''' motifLink ''';' newline 'expLink    = '''...
            expLink ''';' newline 'networkLink= ''' networkLink ''';' newline];

        t=[addText filetext];
        
        fileID = fopen(['scripts/' netTypes{i} '/reproduce' netTypes{i} num2str(j) 'Network.m'],'w');
        fprintf(fileID,t);
        fclose(fileID);
    end

end



