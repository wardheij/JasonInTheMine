function net = train_net(input, target, layers, method)


if strcmp(method, 'classification')
    
    % set up net
    net = patternnet(layers, 'trainscg', 'crossentropy');
    
    % train network
    [net,~] = train(net,input,target);
    
elseif strcmp(method, 'regression')
    
    % set up net
    net = feedforwardnet(layers);
    
    % train network
    net = train(net,input, target);
    
else
    error('Invalid method specified. Select either "classification" or "regression"')
    
end



end


%% solvers tried for classification:
% trainlm -> slow, not for classification
% trainbr -> very slow, promising performance
% trainbfg -> never again
% trainrp -> fast -- good for classification
% trainscg -> fast, poor performance -- good for classification
% traincgb -> fast, poor performance

%% To split test/train/val:
% % Set up Division of Data for Training, Validation, Testing
% net.divideParam.trainRatio = .8;
% net.divideParam.valRatio = 0.1;
% net.divideParam.testRatio = 0.1;