function [net, tr] = train_net(net, input, target, layers, method)

numDelays = 120;

if strcmp(method, 'classification')
       
    % train network
    [net, tr] = train(net,input,target, 'CheckpointFile','checkpoint_class.mat','CheckpointDelay',numDelays);
    
elseif strcmp(method, 'regression')
       
    % train network
    [net, tr] = train(net,input, target, 'CheckpointFile','checkpoint_regr.mat','CheckpointDelay',numDelays);
    
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