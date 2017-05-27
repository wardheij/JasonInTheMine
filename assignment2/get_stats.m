clear all
clc
warning off

vars = {'id', 'srch_id', 'date_time','site_id','visitor_location_country_id','visitor_hist_starrating','visitor_hist_adr_usd','prop_country_id','prop_id','prop_starrating','prop_review_score','prop_brand_bool','prop_location_score1','prop_location_score2','prop_log_historical_price','position','price_usd','promotion_flag','srch_destination_id','srch_length_of_stay','srch_booking_window','srch_adults_count','srch_children_count','srch_room_count','srch_saturday_night_bool','srch_query_affinity_score','orig_destination_distance','random_bool','comp1_rate','comp1_inv','comp1_rate_percent_diff','comp2_rate','comp2_inv','comp2_rate_percent_diff','comp3_rate','comp3_inv','comp3_rate_percent_diff','comp4_rate','comp4_inv','comp4_rate_percent_diff','comp5_rate','comp5_inv','comp5_rate_percent_diff','comp6_rate','comp6_inv','comp6_rate_percent_diff','comp7_rate','comp7_inv','comp7_rate_percent_diff','comp8_rate','comp8_inv','comp8_rate_percent_diff','click_bool','gross_bookings_usd','booking_bool'};

% load data
uniques = importdata('data/train/unique01.txt');
missings = importdata('data/train/missing01.txt');
zeros = importdata('data/train/zeros01.txt');
means = importdata('data/train/mean01.txt');
stds = importdata('data/train/std01.txt');

p_unique = get_percentage(uniques);
p_miss = get_percentage(missings);
p_zeros = get_percentage(zeros);

function percentages = get_percentage(variable_matrix)

% total number of entries
no_entries = 4958356;

percentages = variable_matrix / no_entries;

end


