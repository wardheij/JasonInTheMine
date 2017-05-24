function target = build_target(data, method)

target = data(:, end-2:end);  % click bool, booking price and booking bool

% remove price
target(:, 2) = [];

% encode into format useable to patternnet. The target data for pattern 
% recognition networks should consist of vectors of all zero values except 
% for a 1 in element i, where i is the class they are to represent.
% three classes: [1 0 0] for booked, [0 1 0] for click, [0 0 1] for no
% click


%% target data for training classification net
if strcmp(method, 'classification')
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
    
%% target data for training regression net
elseif strcmp(method, 'regression')
    for k = 1:length(target)

        % if booked 
        if ismember(target(k,:), [1 1], 'rows')
            new_target(k) = 5;
        % if clicked
        elseif ismember(target(k,:), [1 0], 'rows')
            new_target(k) = 1;
        else
            new_target(k) = 0;
        end
    end
    
    target = new_target';
    
else
    error('Invalid method specified. Select "classification" or "regression"')
    
end
    
end


