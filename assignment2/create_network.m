function net = create_network(layers, method)


if strcmp(method, 'classification')
    
    % set up net
    net = patternnet(layers, 'trainscg', 'crossentropy');
    
    
elseif strcmp(method, 'regression')
    
    % set up net
    net = feedforwardnet(layers);
    
else
    error('Invalid method specified. Select either "classification" or "regression"')
    
end

% Set up Division of Data for Training, Validation, Testing
net.divideParam.trainRatio = 1;
net.divideParam.valRatio = 0.1;
net.divideParam.testRatio = 0.1;

end