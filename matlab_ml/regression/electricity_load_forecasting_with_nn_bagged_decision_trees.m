% Load Data
load trainSet 
load testSet 

% Regression Tree Model
mdlTree = RegressionTree.fit(trainX,trainY,'PredictorNames',labels);

% Store Forecasts in a stucture
forecast(1).Y = predict(mdlTree,testX);

% Neural Network Model
net = fitnet(20);
net = train(net, trainX', trainY');
forecast(2).Y = net(testX')';

% Bagged Decision Trees Model
mdlTreeBag = TreeBagger(100, trainX, trainY, 'method', 'regression', ...
                       'oobpred', 'on', 'minleaf', 30);
forecast(3).Y = predict(mdlTreeBag, testX);

% Visualize Prediction Performance
idx = testDates > datenum('Jun-01-2008') & testDates < datenum('Jul-01-2008');

Dates = testDates(idx);

figure('Units','Normalized','Position',[0.05,0.4,0.4,0.5]), subplot(2,1,1)

hPlot1 = plot(Dates, [testY(idx),forecast(1).Y(idx),...
    forecast(2).Y(idx),forecast(3).Y(idx)],'LineWidth',2);
set(hPlot1(1),'LineWidth',5,'Color',[1 1 0],'DisplayName','Actual');
set(hPlot1(2),'Color',[0 1 0],'DisplayName','Regression Tree');
set(hPlot1(3),'DisplayName','Neural Network');
set(hPlot1(4),'Color',[0.5 0.5 0.5],'DisplayName','Bagged Regression Trees');
legend('show'),
datetick('x','mmm-dd','keepticks'), xlabel('Time'),
ylabel('Load'),
title('Load Prediction','FontSize',12,'FontWeight','Bold')

subplot(2,1,2)
hPlot2 = plot(Dates,[testY(idx)-forecast(1).Y(idx)...
    testY(idx)-forecast(2).Y(idx),testY(idx)-forecast(3).Y(idx)]);
set(hPlot2(1),'Color',[0 1 0],'DisplayName','Regression Tree Error');
set(hPlot2(2),'Color','r','DisplayName','Neural Network Error');
set(hPlot2(3),'Color',[0.5 0.5 0.5],'DisplayName','Bagged Regression Trees Error');
datetick('x','mmm-dd','keepticks'), xlabel('Time'),
title('Prediction Error','FontSize',12,'FontWeight','Bold')
ylabel('Residuals'), grid on
legend('show')

