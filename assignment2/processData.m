function processed_data = processData(data, lineInd, batchSize)
% this function removes missing data points and obsolete columns

file = strcat('data_', num2str(lineInd), '_', num2str(lineInd+batchSize));

if exist(strcat('matlab_data/', file, '.mat'), 'file')

	processed_data = importdata(strcat('matlab_data/', file, '.mat'));

else

	percentages = importdata('data/train/percentages01.txt');
	mean = importdata('data/train/mean01.txt');
	std = importdata('data/train/std01.txt');

	for i = 1:size(data, 1)
	    ind = find(strcmp(data(i,:), 'NULL'));
	    
	    for k = ind
	        if percentages(2,k) < 0.2
	            mu = mean(k);
	            sigma = std(k);
	            pd = makedist('Normal','mu',mu,'sigma',sigma);
	            
	            % replace missing data with average when there is enough data
	            data{i,k} = num2str(random(pd));
	        else
	            % replace all NULLs by minus 1.
	            data{i,k} = '-1';
	        end
	    end
	    
	end

	processed_data = [];

	% remove title blocks
	labels = data(1,:);
	% data(1,:) = [];


	% process date
	formatIn = 'yyyy-mm-dd HH:MM:SS';

	DateStrings = data(:, 2);

	date = datevec(DateStrings,formatIn);
	day_of_week = weekday(DateStrings);
    
    % TODO: Count number of competitors


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
	processed_data = [processed_data, date];
	processed_data = [processed_data, day_of_week];

	% remove date
	data(:,2) = [];

	preprocessed_data = str2double(data);

	% Standard vars:
% 	varlist = {'prop_starrating', 'prop_review_score', 'prop_brand_bool', 'prop_location_score1', 'prop_location_score2', 'promotion_flag', 'srch_length_of_stay', 'srch_booking_window', 'srch_query_affinity_score', 'orig_destination_distance'};
    varlist = [9 10 11 12 13 17 19 20 25 26 52 53 54];
    
% 	for i = varlist
% 	    index = ismember(labels,i);
    processed_data = [processed_data, preprocessed_data(:,varlist-1)];
%     end
    
    save(strcat('matlab_data/', file), 'processed_data');


end


end
