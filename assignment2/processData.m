function processed_data = processData(data)
% this function removes missing data points and obsolete columns

percentages = importdata('data/train/percentages_new.txt');
mean = importdata('data/train/mean.txt');
std = importdata('data/train/std.txt');

for i = 1:size(data, 1)
    ind = find(strcmp(data(i,:), 'NULL'));
    
    for k = ind
        if percentages(2,k) < 0.2
            mu = mean(k);
            sigma = std(k);
            pd = makedist('Normal','mu',mu,'sigma',sigma);
            
            % replace missing data with average when there is enough data
            data{i,k} = random(pd);
        else
            if k > 28
                % k > 28 holds competitors. We don't want -1 here
                data{i,k} = 'NULL';
            else
                % replace all NULLs by minus 1.
                data{i,k} = '-1';
            end
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

% TODO: Count number of competitors

% Process before use
preprocessed_data = str2double(data);

% DEPRICATED BOOL IS ALWAYS 0!
% dest_bool = zeros(size(data,1));
% country = find(ismember(labels, "visitor_location_country_id"), 1, 'first');
% prop_country = find(ismember(labels, "prop_country_id"), 1, 'first');
% 
% for i = 1:size(data, 1)
%     
%     if (preprocessed_data(i, country) == preprocessed_data(i, prop_country))
%         dest_bool(i) = 1;
%     else
%         dest_bool(i) = 0;
%     end
% end

% Standard vars:
varlist = ["prop_starrating", "prop_review_score", "prop_brand_bool", "prop_location_score1", "prop_location_score2", "promotion_flag", "srch_length_of_stay", "srch_booking_window", "srch_query_affinity_score", "orig_destination_distance"];

for i = varlist
    index = find(ismember(labels,i), 1, 'first');
    processed_data = [processed_data, preprocessed_data(:,index)];
end


end
