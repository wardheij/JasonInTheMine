function accuracy = eval_performance(pred_labels, true_labels)

% check whether regression or classification was used
[m,n] = size(pred_labels);

if m == 1
    % regression output, so compute RMSE
    cum_err = sum(sqrt((pred_labels - true_labels).^2), 'omitnan');
    accuracy = cum_err/length(pred_labels);
end


end
