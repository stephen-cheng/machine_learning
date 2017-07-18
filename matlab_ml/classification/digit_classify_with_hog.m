% load data
% Load training and test data using |imageDatastore|.
syntheticDir   = fullfile(toolboxdir('vision'), 'visiondata','digits','synthetic');
handwrittenDir = fullfile(toolboxdir('vision'), 'visiondata','digits','handwritten');

% |imageDatastore| recursively scans the directory tree containing the
% images. Folder names are automatically used as labels for each image.
trainingSet = imageDatastore(syntheticDir,   'IncludeSubfolders', true, 'LabelSource', 'foldernames');
testSet     = imageDatastore(handwrittenDir, 'IncludeSubfolders', true, 'LabelSource', 'foldernames');

countEachLabel(trainingSet)
countEachLabel(testSet)

% Show a few of the training and test images
figure;

subplot(2,3,1);
imshow(trainingSet.Files{102});

subplot(2,3,2);
imshow(trainingSet.Files{304});

subplot(2,3,3);
imshow(trainingSet.Files{809});

subplot(2,3,4);
imshow(testSet.Files{13});

subplot(2,3,5);
imshow(testSet.Files{37});

subplot(2,3,6);
imshow(testSet.Files{97});

% Show pre-processing results
exTestImage = readimage(testSet,37);
processedImage = imbinarize(rgb2gray(exTestImage));

figure;

subplot(1,2,1)
imshow(exTestImage)

subplot(1,2,2)
imshow(processedImage)

img = readimage(trainingSet, 206);

% Extract HOG features and HOG visualization
[hog_2x2, vis2x2] = extractHOGFeatures(img,'CellSize',[2 2]);
[hog_4x4, vis4x4] = extractHOGFeatures(img,'CellSize',[4 4]);
[hog_8x8, vis8x8] = extractHOGFeatures(img,'CellSize',[8 8]);

% Show the original image
figure;
subplot(2,3,1:3); imshow(img);

% Visualize the HOG features
subplot(2,3,4);
plot(vis2x2);
title({'CellSize = [2 2]'; ['Length = ' num2str(length(hog_2x2))]});

subplot(2,3,5);
plot(vis4x4);
title({'CellSize = [4 4]'; ['Length = ' num2str(length(hog_4x4))]});

subplot(2,3,6);
plot(vis8x8);
title({'CellSize = [8 8]'; ['Length = ' num2str(length(hog_8x8))]});

%  HOG feature vector
cellSize = [4 4];
hogFeatureSize = length(hog_4x4);

% Train a Digit Classifier
% Loop over the trainingSet and extract HOG features from each image. A
% similar procedure will be used to extract features from the testSet.
numImages = numel(trainingSet.Files);
trainingFeatures = zeros(numImages, hogFeatureSize, 'single');

for i = 1:numImages
    img = readimage(trainingSet, i);

    img = rgb2gray(img);

    % Apply pre-processing steps
    img = imbinarize(img);

    trainingFeatures(i, :) = extractHOGFeatures(img, 'CellSize', cellSize);
end
% Get labels for each image.
trainingLabels = trainingSet.Labels;

% Next, train a classifier using the extracted features.
% fitcecoc uses SVM learners and a 'One-vs-One' encoding scheme.
classifier = fitcecoc(trainingFeatures, trainingLabels);

% Evaluate the Digit Classifier
% Extract HOG features from the test set. The procedure is similar to what
% was shown earlier and is encapsulated as a helper function for brevity.
[testFeatures, testLabels] = helperExtractHOGFeaturesFromImageSet(testSet, hogFeatureSize, cellSize);

% Make class predictions using the test features.
predictedLabels = predict(classifier, testFeatures);

% Tabulate the results using a confusion matrix.
confMat = confusionmat(testLabels, predictedLabels);

helperDisplayConfusionMatrix(confMat)

