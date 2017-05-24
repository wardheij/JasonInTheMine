clear all
clc
warning off

%% Load input data

data = csvreader('train.csv', ',', 1000);

%% Clean up input data

data = processData(data);


%% split data

% clear previous data
clear input target

% split into input and target data
input = data(:, 1:50);  % input data

% pick a method for this run
method = 'regression';

target = build_target(data, method);

% transpose to format for neural network input. Columns = training samples
input = input';
target = target';


%% Create a Pattern Recognition/Classification Network
clc
clear net tr output

% define network architecture
hiddenLayerSize = [256];

net = train_net(input, target, hiddenLayerSize, method);

% Test the Network
output = net(input);
output(:,1:30)'


%%
errors = gsubtract(target,output);
performance = perform(net,target,output)

% View the Network
view(net)

% Plots
% Uncomment these lines to enable various plots.
figure, plotperform(tr)
% figure, plottrainstate(tr)
% figure, plotconfusion(targets,output)
% figure, ploterrhist(errors)