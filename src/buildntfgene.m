% Drug list
%Read aws ls
setenv('LD_LIBRARY_PATH','');
[status,res]=system('aws s3 ls s3://granddb/drugs/drugNetworks/');

%save output to file
fileID = fopen('files.txt','w');
fprintf(fileID,res);
fclose(fileID);

%read file into table
outputNet=readtable('files.txt');

%remove file
system('rm files.txt');

drugs=[outputNet.Var4(:)]';
%%
tfs  = zeros(1,length(drugs));
genes= zeros(1,length(drugs));
parpool(16)
parfor i=1:length(drugs)
    i
    fds      = fileDatastore(['s3://granddb/drugs/drugNetworks/' drugs{i}], "ReadFcn", @load);
    data     = read(fds); 
    genes(i) =size(data.AgNet,2);
    tfs(i)   =size(data.AgNet,1);
end
T = table(drugs',tfs',genes');
writetable(T,'dimNet.csv')