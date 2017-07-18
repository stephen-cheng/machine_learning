% Load Data
clear
load fisheriris
X = meas;
y = categorical(species);

% Evaluate Multiple Clusters from 1 to 10 to Find the Optimal Cluster
eva = evalclusters(X,'kmeans','CalinskiHarabasz','KList',[1:10]);
plot(eva)
disp(categories(y)')

% Dimensionality Reduction for Visualization
% Since none of our features are negative, lets use nnmf to confirm the 3
% clusters visually
Xred = nnmf(X,2);
gscatter(Xred(:,1),Xred(:,2),y)
xlabel('Column 1')
ylabel('Column 2')
legend(categories(y))
grid on