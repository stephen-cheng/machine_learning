% Generate Swiss Roll Data
rng(10); % for reproducibility
N = 1500;
noise = 0.05;
t = 3*pi/2 * (1 + 2*rand(N,1));
h = 11 * rand(N,1);
X = [t.*cos(t), h, t.*sin(t)] + noise*randn(N,3);

% Cluster Data Using K-Means and Agglomerative Clustering
figure('units','normalized','Position',[0.2 0.4 0.55, 0.35]),
subplot(1,2,1)

c = clusterdata(X,'linkage','ward','maxclust',6);
scatter3(X(:,1),X(:,2),X(:,3),[],c,'fill','MarkerEdgeColor','k');
view(-20,5)
title('Agglomerative Clustering')

subplot(1,2,2)
c = kmeans(X,6);
scatter3(X(:,1),X(:,2),X(:,3),[],c,'fill','MarkerEdgeColor','k');
title('KMEANS Clustering')
view(-20,5)

% Use Nearest Neighbors to Compute the Linkage
% Compute 40 nearest neighbors
[idx,Dist]=knnsearch(X,X,'k',40);

% Create the adjacency matrix for linkage
D = zeros(size(X,1));
for ii = 1:length(X)
    D(ii,idx(ii,2:end)) = 1;
end

% Cluster the data with structure defined by neighbors
cLinks = linkage(D, 'ward');
c = cluster(cLinks, 'maxclust', 6);

% Visualize
figure(2)
scatter3(X(:,1),X(:,2),X(:,3),[],c,'fill','MarkerEdgeColor','k');
title('Structured Hierarchical Clustering')
view(-20,5)

