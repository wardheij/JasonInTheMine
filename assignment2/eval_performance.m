function accuracy = eval_performance(pred_labels, true_labels, tr)

% check whether regression or classification was used
[m,n] = size(pred_labels);

if m == 1
    % regression output, so compute RMSE
    cum_err = sum(sqrt((pred_labels(tr.testInd) - true_labels(tr.testInd)).^2), 'omitnan');
    accuracy = cum_err/length(pred_labels(tr.testInd));
end


end
