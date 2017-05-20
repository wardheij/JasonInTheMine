clear all
clc
warning off

%% Load input data
% input = 0:1000;
% target = zeros(length(input), 2);
% target(end/2:end, 2) = 1;
% target(1:end/2, 1) = 1;
% target = target';


data = csvreader('train.csv', ',', 100000);

%% Clean up input data

for i = 1:size(data, 1)
    ind = find(strcmp(data(i,:), 'NULL'));
    
    for k = ind
        data{i,k} = '0';
    end
    
end

% remove title blocks
labels = data(1,:);
data(1,:) = [];

% remove date
data(:,2) = [];

data = str2double(data);


%% split data

% split into input and target data
input = data(:, 1:50);  % input data
target = data(:, 51:53);  % click bool, booking price and booking bool

% remove price
target(:, 2) = [];

% encode into format useable to patternnet. The target data for pattern 
% recognition networks should consist of vectors of all zero values except 
% for a 1 in element i, where i is the class they are to represent.
% three classes: [1 0 0] for booked, [0 1 0] for click, [0 0 1] for no
% click

for k = 1:length(target)
    
    % if booked 
    if ismember(target(k,:), [1 1], 'rows')
        new_target(k,:) = [1 0 0];
    % if clicked
    elseif ismember(target(k,:), [1 0], 'rows')
        new_target(k,:) = [0 1 0];
    else
        new_target(k,:) = [0 0 1];
    end
end
target = new_target;

% transpose to format for neural network input. Columns = training samples
input = input';
target = target';


%% Create a Pattern Recognition/Classification Network
clc
clear net tr outputs
hiddenLayerSize = [1000];
net = patternnet(hiddenLayerSize, 'trainscg', 'crossentropy');

% solvers tried:
% trainlm -> slow, not for classification
% trainbr -> very slow, promising performance
% trainbfg -> never again
% trainrp -> fast -- good for classification
% trainscg -> fast, poor performance -- good for classification
% traincgb -> fast, poor performance
% train


% net = lvqnet(10);

% % Set up Division of Data for Training, Validation, Testing
% net.divideParam.trainRatio = 70/100;
% net.divideParam.valRatio = 15/100;
% net.divideParam.testRatio = 15/100;

% Train the Network
[net,tr] = train(net,input,target);

% Test the Network
outputs = net(input);
outputs(:,1:30)'


%%
errors = gsubtract(targets,outputs);
performance = perform(net,targets,outputs)

% View the Network
view(net)

% Plots
% Uncomment these lines to enable various plots.
figure, plotperform(tr)
% figure, plottrainstate(tr)
% figure, plotconfusion(targets,outputs)
% figure, ploterrhist(errors)