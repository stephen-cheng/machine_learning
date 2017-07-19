% Load the digit sample data as an ImageDatastore object.
digitDatasetPath = fullfile(matlabroot,'toolbox','nnet','nndemos', ...
        'nndatasets','DigitDataset');
digitData = imageDatastore(digitDatasetPath, ...
        'IncludeSubfolders',true,'LabelSource','foldernames');
		
% Display some of the images in the datastore.
figure;
perm = randperm(10000,20);
for i = 1:20
    subplot(4,5,i);
    imshow(digitData.Files{perm(i)});
end

% Check the number of images in each category.
CountLabel = digitData.countEachLabel;
img = readimage(digitData,1);
size(img)

% Specify Training and Test Sets
trainingNumFiles = 750;
rng(1) % For reproducibility
[trainDigitData,testDigitData] = splitEachLabel(digitData, ...
				trainingNumFiles,'randomize');
				
% Define the Network Layers
layers = [imageInputLayer([28 28 1])
          convolution2dLayer(5,20)
          reluLayer
          maxPooling2dLayer(2,'Stride',2)
          fullyConnectedLayer(10)
          softmaxLayer
          classificationLayer()];
		  
% Specify the Training Options
options = trainingOptions('sgdm','MaxEpochs',15, ...
	'InitialLearnRate',0.0001);
	
% Train the Network Using Training Data
convnet = trainNetwork(trainDigitData,layers,options);

% Classify the Images in the Test Data and Compute Accuracy
YTest = classify(convnet,testDigitData);
TTest = testDigitData.Labels;
accuracy = sum(YTest == TTest)/numel(TTest)

