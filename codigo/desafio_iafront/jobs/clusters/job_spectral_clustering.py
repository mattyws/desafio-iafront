from functools import partial

import click
import numpy as np

from desafio_iafront.jobs.clusters.clusters import spectral_clustering
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.clusters.utils import save_clustered_data
from desafio_iafront.jobs.common import filter_date


@click.command()
@click.option('--dataset', type=click.Path(exists=True), required=True)
@click.option('--number-of-cluster', type=click.INT, required=True)
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False), required=True)
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]), required=True)
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]), required=True)
@click.option('--eigen-solver', type=click.STRING, default=None, required=False)
@click.option('--n-components', type=click.INT, default=None, required=False)
@click.option('--random-state', type=click.INT, default=None, required=False)
@click.option('--n-init', type=click.INT, default=10, required=False)
@click.option('--gamma', type=click.FLOAT, default=1.0, required=False)
@click.option('--affinity', type=click.STRING, default='rbf', required=False)
@click.option('--n-neighbors', type=click.INT, default=10, required=False)
@click.option('--eigen-tol', type=click.FLOAT, default=0.0, required=False)
@click.option('--assign-labels', type=click.STRING, default='kmeans', required=False)
@click.option('--degree', type=click.FLOAT, default=3.0, required=False)
@click.option('--coef0', type=click.FLOAT, default=1.0, required=False)
@click.option('--n-jobs', type=click.INT, default=-1, required=False)
def spectral(dataset: str, number_of_cluster:int, saida: str, data_inicial, data_final, eigen_solver:str, n_components:int,
           random_state:int, n_init:int, gamma:float, affinity:str, n_neighbors:int, eigen_tol:float, assign_labels:str,
           degree:float, coef0:float, n_jobs:int):
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    dataset = read_partitioned_json(file_path=dataset, filter_function=filter_function)
    vector = np.asarray(list(dataset['features'].to_numpy()))
    labels = spectral_clustering(vector, number_of_cluster, eigen_solver=eigen_solver, n_components=n_components,
                                 random_state=random_state, n_init=n_init, gamma=gamma, affinity=affinity,
                                 n_neighbors=n_neighbors, eigen_tol=eigen_tol, assign_labels=assign_labels,
                                 degree=degree, coef0=coef0, n_jobs=n_jobs)
    dataset['cluster_label'] = list(labels)

    save_clustered_data(dataset, saida)


if __name__ == '__main__':
    spectral()
