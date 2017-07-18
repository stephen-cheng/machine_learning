% Load Data
clear
load fisheriris
X = meas(:,1:2);
y = categorical(species);
labels = categories(y);

figure(1)
gscatter(X(:,1), X(:,2), species,'rgb','osd');
xlabel('Sepal length');
ylabel('Sepal width');

% Train Four Different Classifiers and Store the Models in a Cell Array
classifier{1} = NaiveBayes.fit(X,y);
classifier{2} = ClassificationDiscriminant.fit(X,y);
classifier{3} = ClassificationTree.fit(X,y);
classifier{4} = ClassificationKNN.fit(X,y);
classifier_name = {'Naive Bayes','Discriminant Analysis','Classification Tree','Nearest Neighbor'};

% Predict Species Using All Classifiers
[xx1, xx2] = meshgrid(4:.01:8,2:.01:4.5);

figure(2)
for ii = 1:numel(classifier)
   ypred = predict(classifier{ii},[xx1(:) xx2(:)]);

   h(ii) = subplot(2,2,ii);
   gscatter(xx1(:), xx2(:), ypred,'rgb');

   title(classifier_name{ii},'FontSize',15)
   legend off, axis tight
end

legend(h(1), labels,'Location',[0.35,0.01,0.35,0.05],'Orientation','Horizontal')

