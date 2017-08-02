clear all
clc
warning off


%% iterate over entire training set
batchSize = 1e4;
numLines = 4e6;

% define network architecture
hiddenLayerSize = [128];

% pick a method for this run
method = 'regression';

net = create_network(hiddenLayerSize, method);

count = 1;
perfs = [];

for i = 1:batchSize:numLines
    
    %% Load input data

    data = csvreader('train.csv', ',', i, batchSize);

    %% Clean up input data

    data = processData(data, i, batchSize);


    %% split data

    % clear previous data
    clear input target

    % split into input and target data
    input = data(:, 1:end-3);  % input data

    target = build_target(data, method);

    % transpose to format for neural network input. Columns = training samples
    input = input';
    target = target';


    %% Create a Pattern Recognition/Classification Network
%     clc
%     clear net tr output

    [net, tr] = train_net(net, input, target, hiddenLayerSize, method);

    % Test the Network
    output = net(input);
    M = max(output)
%     output(:,1:30)';


    %% Evaluate performance
    % evaluate only on test set

    per = eval_performance(output, target, tr);
    
    fprintf('Trained on batch %i, with performance of %2.2f \n ', count, per);
    count = count + 1;
    perfs(count) = per;

end

save('performance_128.mat', 'perfs')
%% performance / hyperparameters

% influence of # neurons, compute mean and 
n = [512 256 128 64 32 16 8]; P = []; E = [];
perfs_512 = importdata('performance_512.mat'); 
P(1) = mean(perfs_512(1:10)); 
E(1) = std(perfs_512(1:10));

perfs_256 = importdata('performance_256.mat'); 
P(2) = mean(perfs_256(1:10));
E(2) = std(perfs_256(1:10));

perfs_128 = importdata('performance_128.mat'); 
P(3) = mean(perfs_128(1:10));
E(3) = std(perfs_128(1:10));

perfs_64 = importdata('performance_64.mat'); 
P(4) = mean(perfs_64(1:10));
E(4) = std(perfs_64(1:10));

perfs_32 = importdata('performance_32.mat'); 
P(5) = mean(perfs_32(1:10));
E(5) = std(perfs_32(1:10));

perfs_16 = importdata('performance_16.mat'); 
P(6) = mean(perfs_16(1:10));
E(6) = std(perfs_16(1:10));

perfs_8 = importdata('performance_8.mat'); 
P(7) = mean(perfs_8(1:10));
E(7) = std(perfs_8(1:10));

t = [277.1487 56.0656 7.8155 1.0393 0.6542 0.2523 0.1687];

figure
yyaxis left
errorbar(n, P, E, '^--','linewidth', 1.5)
ylim([0 .8])
ylabel('RMSE')

yyaxis right
loglog(n, t,'s--', 'linewidth', 1.5)
ylabel('Average training time [s]')

xlabel('Hidden units')
title('RMSE and training time')
grid on


%% Inference
clear all

% load trained network
load('checkpoint_regr_FINAL_256.mat')
net = checkpoint.net;

clear batchSize numLines
batchSize = 1e4;
numLines = 4959192;
ind = 0;

for i = 1:batchSize:numLines
    
    % Load input data from the start of the last query of the previous
    % search
    data = csvreader('test.csv', ',', i-ind, batchSize);

    % Clean up input data
    data = processDataTest(data, i-ind, batchSize);

    % split data
    % clear previous data
    clear input target
    
    % the first two columns of data are search ID and property ID
    srch_id = data(:,8);
    prop_id = data(:,9);
    data(:, 8:9) = [];
    
    % we have to make sure we have all current queries in our current data
    % slice. Hence, we omit the last query to prevent it from 'chopping'
    % off and put that into the next data slice
    last_id = srch_id(end);
    ind = find(srch_id==last_id, 1, 'first');
    
    % remove from the data the cut-off last query
    srch_id(ind:end) = [];
    prop_id(ind:end) = [];
    data(ind:end, :) = [];
    
    data = data';
    % now find all unique queries in the data, iterate over them and write
    % their rankings to file
    ids = unique(srch_id);  % list of search ids in this data slice
    
    fileID = fopen('submission.txt','a');  % append to prediction file
    
    for I = ids'
        
        indices = find(srch_id == I);
        
        nn_input = data(:, indices);
        nn_propids = prop_id(indices);

        % inference
        nn_output = net(nn_input);
        
        % sort descending based on score
        [B,II] = sort(nn_output, 'descend');
        sorted_propids = nn_propids(II);
        
        % write this to file
        for prop_id_to_print = sorted_propids'
            fprintf(fileID,'%i, %i \n', [I prop_id_to_print]);
        end 
        
               
    end
    
    fclose(fileID);
    fprintf('writted query IDs %i to %i',[ids(1) ids(end)]);
 
end

