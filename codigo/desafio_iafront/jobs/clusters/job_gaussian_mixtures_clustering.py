from functools import partial

import click
import numpy as np
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.clusters.clusters import gaussian_mixtures_clustering
from desafio_iafront.jobs.clusters.utils import save_clustered_data
from desafio_iafront.jobs.common import filter_date


@click.command()
@click.option('--dataset', type=click.Path(exists=True))
@click.option('--number-of-cluster', type=click.INT)
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
def gaussian_mixtures(dataset: str, number_of_cluster: int, saida: str, data_inicial, data_final):
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)

    dataset = read_partitioned_json(file_path=dataset, filter_function=filter_function)
    vector = np.asarray(list(dataset['features'].to_numpy()))
    labels = gaussian_mixtures_clustering(vector, number_of_cluster)
    dataset['cluster_label'] = list(labels)
    save_clustered_data(dataset, saida)


if __name__ == '__main__':
    gaussian_mixtures()
