% Load Data
load fisheriris
labels = unique(species);
disp(labels)

% Train a Linear Discriminant Analysis (LDA) Classifier
mdl = ClassificationDiscriminant.fit(meas,species); 

% Predict Species Using the LDA Model
predicted_species = predict(mdl,meas); 

% Compute and Visualize the Confusion Matrix
Conf_Mat = confusionmat(species,predicted_species);
disp(Conf_Mat)
HeatMap(Conf_Mat, labels, labels, 1,'Colormap','red','ShowAllTicks',1,'UseLogColorMap',true,'Colorbar',true);

