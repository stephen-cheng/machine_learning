% Load Data for Classification
rng(5); % For reproducibility
load ionosphere;
labels = unique(Y);

% Partition 70% of the Data into a Training Set and 30% into a Test Set
cv = cvpartition(Y,'holdout',0.3);
Xtrain = X(training(cv),:);
Ytrain = Y(training(cv));
Xtest = X(test(cv),:);
Ytest = Y(test(cv));

% Use Bagged Decision Trees to Classify the Ionosphere Data
% Classification Tree is chosen as the learner
mdl1 = ClassificationTree.template('NVarToSample','all');
RF1 = fitensemble(Xtrain,Ytrain,'Bag',150,mdl1,'type','classification');

% Classification Tree with surrogate splits is chosen as the learner
mdl2 = ClassificationTree.template('NVarToSample','all','surrogate','on');
RF2 = fitensemble(Xtrain,Ytrain,'Bag',150,mdl2,'type','classification');

Xtest(rand(size(Xtest))>0.5) = NaN;

% Predict Responses Using Both Approaches
y_pred1 = predict(RF1,Xtest);
confmat1 = confusionmat(Ytest,y_pred1);

y_pred2 = predict(RF2,Xtest);
confmat2 = confusionmat(Ytest,y_pred2);

disp('Confusion Matrix - without surrogates')
disp(confmat1)
disp('Confusion Matrix - with surrogates')
disp(confmat2)

% Visualize Misclassification Error
figure
subplot(2,2,1:2)
plot(loss(RF1,Xtest,Ytest,'mode','cumulative'),'LineWidth',3);
hold on;
plot(loss(RF2,Xtest,Ytest,'mode','cumulative'),'r','LineWidth',3);
legend('Regular trees','Trees with surrogate splits');
xlabel('Number of trees');
ylabel('Test classification error','FontSize',12);

subplot(2,2,3)
[hImage, hText, hXText] = HeatMap(confmat1, labels, labels, 1,'Colormap','red','ShowAllTicks',1);
title('Confusion Matrix - without surrogates')
subplot(2,2,4)
heatmap(confmat2, labels, labels, 1,'Colormap','red','ShowAllTicks',1);
title('Confusion Matrix - with surrogates')

