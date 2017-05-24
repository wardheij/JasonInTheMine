function processed_data = processData(data)
% this function removes missing data points and obsolete columns

for i = 1:size(data, 1)
    ind = find(strcmp(data(i,:), 'NULL'));
    
    % for now, replace all NULLs by zeros.
    for k = ind
        data{i,k} = '0';
    end
    
end

% remove title blocks
labels = data(1,:);
data(1,:) = [];

% remove date
data(:,2) = [];

processed_data = str2double(data);


% TODO: add Wouters code that converts data to useful variables


end
