clear all
clc
warning off


%% iterate over entire training set
batchSize = 100000;
numLines = 4e6;

% define network architecture
hiddenLayerSize = [256];

% pick a method for this run
method = 'regression';

net = create_network(hiddenLayerSize, method);

count = 1;
perfs = [];

for i = 1:batchSize:numLines
    
    %% Load input data

    data = csvreader('train.csv', ',', i, batchSize);

    %% Clean up input data

    data = processData(data);


    %% split data

    % clear previous data
    clear input target

    % split into input and target data
    input = data(:, 1:50);  % input data

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
%     output(:,1:30)';


    %% Evaluate performance
    % evaluate only on test set

    per = eval_performance(output, target, tr);
    
    fprintf('Trained on batch %i, with performance of %2.2f \n ', count, per);
    count = count + 1;
    perfs(count) = per;

end

%%
% errors = gsubtract(target,output);
% performance = perform(net,target,output);
% 
% % View the Network
% view(net)
% 
% % Plots
% % Uncomment these lines to enable various plots.
% figure, plotperform(tr)
% % figure, plottrainstate(tr)
% % figure, plotconfusion(targets,output)
% % figure, ploterrhist(errors)