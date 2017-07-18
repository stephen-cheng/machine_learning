% Load Data
load filteredyeastdata
rng('default') % For reproducibility

% Clustering Genes Using a Hierarchical Cluster Tree
clusters = clusterdata(yeastvalues,'maxclust',16,'distance','correlation','linkage','average');
figure(1)
for c = 1:16
    subplot(4,4,c);
    plot(times,yeastvalues((clusters == c),:)');
    axis tight
end
suptitle('Hierarchical Clustering of Profiles');

% Use Principal Component Analysis and K-Means to Cluster in Lower Dimensions
figure(2)
[~,score,~,~,explainedVar] = pca(yeastvalues);
bar(explainedVar)
title('Explained Variance: More than 90% explained by first two principal components')
ylabel('PC')

% Retain first two principal components
yeastPC = score(:,1:2);

figure(3)
[clusters, centroid] = kmeans(yeastPC,6);
gscatter(yeastPC(:,1),yeastPC(:,2),clusters)
legend('location','southeast')
xlabel('First Principal Component');
ylabel('Second Principal Component');
title('Principal Component Scatter Plot with Colored Clusters');

% Label one gene in each cluster
[~, r] = unique(clusters);
text(yeastPC(r,1),yeastPC(r,2),genes(r),'FontSize',11);

% Use Principal Component Analysis and Self-Organizing Maps to Cluster in Lower Dimensions
net = newsom(yeastPC',[4 4]);
net = train(net,yeastPC');

distances = dist(yeastPC,net.IW{1}');
[d,center] = min(distances,[],2);
% center gives the cluster index

figure
gscatter(yeastPC(:,1),yeastPC(:,2),center); legend off;
hold on
plotsom(net.iw{1,1},net.layers{1}.distances);
hold off

