function processed_data = processData(data)
% this function removes missing data points and obsolete columns

for i = 1:size(data, 1)
    ind = find(strcmp(data(i,:), 'NULL'));
    
    % for now, replace all NULLs by minus 1.
    for k = ind
        data{i,k} = '-1';
    end
    
end

% remove title blocks
labels = data(1,:);
data(1,:) = [];


% TODO: process date



% remove date
data(:,2) = [];

preprocessed_data = str2double(data);

processed_data = [];

% This order:
varlist = ["prop_starrating", "prop_review_score", "prop_brand_bool", "prop_location_score1", "prop_location_score2", "promotion_flag", "srch_length_of_stay", "srch_booking_window", "srch_query_affinity_score", "orig_destination_distance"];

for i = varlist
    index = find(labels, i);
    processed_data = append(processed_data, preprocessed_data(:,index));
end

end
