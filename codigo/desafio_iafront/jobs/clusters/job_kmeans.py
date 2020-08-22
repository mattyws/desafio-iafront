from functools import partial

import click
import numpy as np
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.clusters.clusters import kmeans_clustering
from desafio_iafront.jobs.clusters.utils import save_clustered_data
from desafio_iafront.jobs.common import filter_date


@click.command()
@click.option('--dataset', type=click.Path(exists=True))
@click.option('--number-of-cluster', type=click.INT)
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))

@click.option('--init', type=click.STRING, default='k-means++', required=False)
@click.option('--n-init', type=click.INT, default=10, required=False)
@click.option('--max-iter', type=click.INT, default=300, required=False)
@click.option('--tol', type=click.FLOAT, default=0.0001, required=False)
@click.option('--verbose', type=click.INT, default=0, required=False)
@click.option('--random-state', type=click.INT, default=None, required=False)
@click.option('--copy-x', type=click.BOOL, default=True, required=False)
@click.option('--algorithm', type=click.STRING, default='auto', required=False)
def kmeans(dataset: str, number_of_cluster: int, saida: str, data_inicial, data_final, init:str, n_init:int,
         max_iter:int, tol:float, verbose:int, random_state:int, copy_x:bool, algorithm:str):
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)

    dataset = read_partitioned_json(file_path=dataset, filter_function=filter_function)
    vector = np.asarray(list(dataset['features'].to_numpy()))
    coordinates, labels = kmeans_clustering(vector, number_of_cluster, init=init, n_init=n_init, max_iter=max_iter, tol=tol,
                                 verbose=verbose, random_state=random_state, copy_x=copy_x, algorithm=algorithm)
    dataset['cluster_coordinate'] = list(coordinates)
    dataset['cluster_label'] = list(labels)
    save_clustered_data(dataset, saida)


if __name__ == '__main__':
    kmeans()
