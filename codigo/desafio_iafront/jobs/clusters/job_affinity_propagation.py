from functools import partial

import click
import numpy as np

from desafio_iafront.jobs.clusters.clusters import affinity_propagation
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.clusters.utils import save_clustered_data
from desafio_iafront.jobs.common import filter_date


@click.command()
@click.option('--dataset', type=click.Path(exists=True), required=True)
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False), required=True)
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]), required=True)
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]), required=True)
@click.option('--damping', type=click.FLOAT, default=0.5, required=False)
@click.option('--max-iter', type=click.INT, default=200, required=False)
@click.option('--convergence-iter', type=click.INT, default=15, required=False)
@click.option('--copy', type=click.BOOL, default=True, required=False)
@click.option('--affinity', type=click.STRING, default='euclidean', required=False)
@click.option('--verbose', type=click.BOOL, default=False, required=False)
@click.option('--random-state', type=click.INT, default=0, required=False)
def affinity(dataset: str, saida: str, data_inicial, data_final, damping:float, max_iter:int, convergence_iter:int,
             copy:bool, affinity:str, verbose:bool, random_state:int):
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    dataset = read_partitioned_json(file_path=dataset, filter_function=filter_function)
    vector = np.asarray(list(dataset['features'].to_numpy()))
    labels = affinity_propagation(vector, damping=damping, max_iter=max_iter, convergence_iter=convergence_iter,
                                  copy=copy, affinity=affinity, verbose=verbose, random_state=random_state)
    dataset['cluster_label'] = list(labels)

    save_clustered_data(dataset, saida)


if __name__ == '__main__':
    affinity()
