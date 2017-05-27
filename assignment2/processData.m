function processed_data = processData(data)
% this function removes missing data points and obsolete columns

percentages = importdata('data/train/percentages_new.txt');

for i = 1:size(data, 1)
    ind = find(strcmp(data(i,:), 'NULL'));
    
    mu = percentage(4,i);
    sigma = percentage(4,i);
    pd = makedist('Normal','mu',mu,'sigma',sigma);
    
    % for now, replace all NULLs by minus 1.
    for k = ind
        if percentages(2,i) < 0.2
            data{i,k} = random(pd);
        else
            data{i,k} = '-1';
        end
    end
    
end

processed_data = [];

% remove title blocks
labels = data(1,:);
data(1,:) = [];


% process date
formatIn = 'yyyy-mm-dd HH:MM:SS';

DateStrings = data(:, 2);

date = datevec(DateStrings,formatIn);
day_of_week = weekday(DateStrings);

processed_data = [processed_data, date];
processed_data = [processed_data, day_of_week];

% remove date
data(:,2) = [];

preprocessed_data = str2double(data);

% Standard vars:
varlist = ["prop_starrating", "prop_review_score", "prop_brand_bool", "prop_location_score1", "prop_location_score2", "promotion_flag", "srch_length_of_stay", "srch_booking_window", "srch_query_affinity_score", "orig_destination_distance"];

for i = varlist
    index = ismember(labels,i);
    processed_data = [processed_data, preprocessed_data(:,index)];
end



end
