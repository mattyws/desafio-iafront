from functools import partial

import click
import os
import numpy as np

from desafio_iafront.jobs.clusters.clusters import agglomerative_clustering
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.clusters.utils import save_clustered_data
from desafio_iafront.jobs.common import filter_date


@click.command()
@click.option('--dataset', type=click.Path(exists=True), required=True)
@click.option('--number-of-cluster', type=click.INT, required=True)
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False), required=True)
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]), required=True)
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]), required=True)
@click.option('--affinity', type=click.STRING, default='euclidean', required=False)
@click.option('--linkage', type=click.STRING, default='ward', required=False)
@click.option('--distance-threshold', type=click.FLOAT, default=None, required=False)
def agglomerative(dataset: str, number_of_cluster: int, saida: str, data_inicial, data_final,
                  affinity:str, linkage:str, distance_threshold:float):
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)

    dataset = read_partitioned_json(file_path=dataset, filter_function=filter_function)
    vector = np.asarray(list(dataset['features'].to_numpy()))
    labels = agglomerative_clustering(vector, number_of_cluster, affinity=affinity, linkage=linkage,
                                                   distance_threshold=distance_threshold)
    dataset['cluster_label'] = list(labels)
    save_clustered_data(dataset, saida)

if __name__ == '__main__':
    agglomerative()
