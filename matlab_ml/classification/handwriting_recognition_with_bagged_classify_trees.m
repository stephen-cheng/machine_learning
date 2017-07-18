% Load Training and Test Data
clear
load('usps_all');

reduce_dim = false;
X = double(reshape(data,256,11000)');
ylabel = [1:9 0];

y = reshape(repmat(ylabel,1100,1),11000,1);

clearvars data

% Visualize Six Random Handwritten Samples
figure(1)
for ii = 1:6
    subplot(2,3,ii)
    rand_num = randperm(11000,1);
    image(reshape(X(rand_num,:),16,16))
    title((y(rand_num)),'FontSize',20)
    axis off
end
colormap gray

% Randomly Partition the Data into Training and Validation Sets
cv = cvpartition(y, 'holdout', .5);
Xtrain = X(cv.training,:);
Ytrain = y(cv.training,1);

Xtest = X(cv.test,:);
Ytest = y(cv.test,1);

% Train and Predict Using a Single Classification Tree
mdl_ctree = ClassificationTree.fit(Xtrain,Ytrain);
ypred = predict(mdl_ctree,Xtest);
Confmat_ctree = confusionmat(Ytest,ypred);

% Train and Predict Using Bagged Decision Trees
mdl = fitensemble(Xtrain,Ytrain,'bag',200,'tree','type','Classification');
ypred = predict(mdl,Xtest);
Confmat_bag = confusionmat(Ytest,ypred);

% Compare Confusion Matrices
figure,
HeatMap(Confmat_ctree, 0:9, 0:9, 1,'Colormap','red','ShowAllTicks',1,'UseLogColorMap',true,'Colorbar',true);
title('Confusion Matrix: Single Classification Tree')
figure,
HeatMap(Confmat_bag, 0:9, 0:9, 1,'Colormap','red','ShowAllTicks',1,'UseLogColorMap',true,'Colorbar',true);
title('Confusion Matrix: Ensemble of Bagged Classification Trees')
