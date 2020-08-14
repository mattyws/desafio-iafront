from functools import partial

import click
import os

import numpy
import numpy as np

from desafio_iafront.jobs.clusters.clusters import optics_clustering
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.clusters.utils import save_clustered_data
from desafio_iafront.jobs.common import filter_date


@click.command()
@click.option('--dataset', type=click.Path(exists=True), required=True)
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False), required=True)
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]), required=True)
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]), required=True)
@click.option('--min-samples', type=click.INT, default=5, required=False)
@click.option('--max-eps', type=click.FLOAT, default=numpy.inf, required=False)
@click.option('--metric', type=click.STRING, default='minkowski', required=False)
@click.option('--minkowski-p', type=click.INT, default=2, required=False)
@click.option('--cluster-method', type=click.STRING, default='xi', required=False)
@click.option('--eps', type=click.FLOAT, default=None, required=False)
@click.option('--xi', type=click.FLOAT, default=0.05, required=False)
@click.option('--predecessor-correction', type=click.BOOL, default=True, required=False)
@click.option('--min-cluster-size', type=(click.INT, click.FLOAT), default=None, required=False)
@click.option('--algorithm', type=click.STRING, default='auto', required=False)
@click.option('--leaf-size', type=click.INT, default=30, required=False)
@click.option('--n-jobs', type=click.INT, default=None, required=False)
def optics(dataset: str, saida: str, data_inicial, data_final, min_samples:int, max_eps:int, metric:str, minkowski_p:int,
           cluster_method:str, eps:float, xi:float, predecessor_correction:bool, min_cluster_size, algorithm:str,
           leaf_size:int, n_jobs:int):

    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    dataset = read_partitioned_json(file_path=dataset, filter_function=filter_function)
    vector = np.asarray(list(dataset['features'].to_numpy()))
    labels = optics_clustering(vector, min_samples=min_samples, max_eps=max_eps, metric=metric, p=minkowski_p,
                               cluster_method=cluster_method, eps=eps, xi=xi, predecessor_correction=predecessor_correction,
                               min_cluster_size=min_cluster_size, algorithm=algorithm, leaf_size=leaf_size, n_jobs=n_jobs)
    dataset['cluster_label'] = list(labels)

    save_clustered_data(dataset, saida)


if __name__ == '__main__':
    optics()
