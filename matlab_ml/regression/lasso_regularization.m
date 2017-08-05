% Download Data
filename = 'diabetes.txt'; 
urlwrite('http://www.stanford.edu/~hastie/Papers/LARS/diabetes.data',filename); 

% Import data
formatSpec = '%f%f%f%f%f%f%f%f%f%f%f%[^\n\r]';
fileID = fopen(filename,'r');
dataArray = textscan(fileID, formatSpec, 'Delimiter', '\t', 'HeaderLines' ,1, 'ReturnOnError', false);
fclose(fileID);
diabetes = table(dataArray{1:end-1}, 'VariableNames', {'AGE','SEX','BMI','BP','S1','S2','S3','S4','S5','S6','Y'});
clearvars filename delimiter startRow formatSpec fileID dataArray ans;

% Delete the file
delete diabetes.txt

% Read the Predictors and Response Variables from the Table
predNames = diabetes.Properties.VariableNames(1:end-1);
X = diabetes{:,1:end-1};
y = diabetes{:,end};

% Perform Lasso Regularization
[beta, FitInfo] = lasso(X,y,'Standardize',true,'CV',10,'PredictorNames',predNames);
lassoPlot(beta,FitInfo,'PlotType','Lambda','XScale','log');

hlplot = get(gca,'Children');

% Generating colors for each line in the plot
colors = hsv(numel(hlplot));
for ii = 1:numel(hlplot)
    set(hlplot(ii),'color',colors(ii,:));
end

set(hlplot,'LineWidth',2)
set(gcf,'Units','Normalized','Position',[0.2 0.4 0.5 0.35])
legend('Location','Best')

% As a rule of thumb, one standard-error value is often used for choosing a smaller model with a good fit.
lam = FitInfo.Index1SE;
isImportant = beta(:,lam) ~= 0;
disp(predNames(isImportant))

% Fit a Linear Model with the Terms for Comparison
mdlFull = fitlm(X,y,'Intercept',false);
disp(mdlFull)

% Compare the MSE for regularized and unregularized models.
disp(['Lasso MSE: ', num2str(FitInfo.MSE(lam))])
disp(['Full  MSE: ', num2str(mdlFull.MSE)])

