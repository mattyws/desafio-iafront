import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering, AffinityPropagation, SpectralClustering, OPTICS


def kmeans(vector: np.array, n: int, init='k-means++', n_init=10, max_iter=300, tol=0.0001,
           precompute_distances='deprecated', verbose=0, random_state=None,
           copy_x=True, n_jobs='deprecated', algorithm='auto'):
    k = KMeans(n_clusters=n, init=init, n_init=n_init, max_iter=max_iter, tol=tol,
               precompute_distances=precompute_distances, verbose=verbose, random_state=random_state, copy_x=copy_x,
               n_jobs=n_jobs, algorithm=algorithm)
    cluster_coordinate = k.fit_transform(vector)
    cluster_label = k.fit(vector)

    return cluster_coordinate, cluster_label.labels_

def agglomerative_clustering(vector:np.array, n_clusters, affinity='euclidean', memory="./agglomerative_memory/", connectivity=None,
                             compute_full_tree='auto', linkage='ward', distance_threshold=None):
    agglomerative = AgglomerativeClustering(n_clusters, affinity=affinity, memory=memory, connectivity=connectivity,
                                            compute_full_tree=compute_full_tree, linkage=linkage, distance_threshold=distance_threshold)
    agglomerative = agglomerative.fit(vector)

    return agglomerative.labels_

def affinity_propagation(vector:np.array, damping=0.5, max_iter=200, convergence_iter=15, copy=True,
                         preference=None, affinity='euclidean', verbose=False, random_state=0):
    affinity_clustering = AffinityPropagation(damping=damping, max_iter=max_iter, convergence_iter=convergence_iter,
                                              copy=copy, preference=preference, affinity=affinity, verbose=verbose,
                                              random_state=random_state)
    affinity_clustering = affinity_clustering.fit(vector)
    return affinity_clustering.labels_

def spectral_clustering(vector:np.array, n_clusters, eigen_solver=None, n_components=None, random_state=None, n_init=10, gamma=1.0,
                        affinity='rbf', n_neighbors=10, eigen_tol=0.0, assign_labels='kmeans', degree=3, coef0=1,
                        kernel_params=None, n_jobs=None):
    spectral_cluster = SpectralClustering(n_clusters=n_clusters, eigen_solver=eigen_solver, n_components=n_components,
                                             random_state=random_state, n_init=n_init, gamma=gamma, affinity=affinity,
                                             n_neighbors=n_neighbors, eigen_tol=eigen_tol, assign_labels=assign_labels,
                                             degree=degree, coef0=coef0, kernel_params=kernel_params, n_jobs=n_jobs)
    spectral_cluster = spectral_cluster.fit(vector)
    return spectral_cluster.labels_

def optics_clustering(vector:np.array, min_samples=5, max_eps=np.inf, metric='minkowski', p=2, metric_params=None,
                      cluster_method='xi', eps=None, xi=0.05, predecessor_correction=True,
                      min_cluster_size=None, algorithm='auto', leaf_size=30, n_jobs=None):
    optics = OPTICS(min_samples=min_samples, max_eps=max_eps, metric=metric, p=p, metric_params=metric_params,
                    cluster_method=cluster_method, eps=eps, xi=xi, predecessor_correction=predecessor_correction,
                    min_cluster_size=min_cluster_size, algorithm=algorithm, leaf_size=leaf_size, n_jobs=n_jobs)
    optics = optics.fit(vector)

    return optics.labels_