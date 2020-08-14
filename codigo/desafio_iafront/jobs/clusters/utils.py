import pandas
import os

from desafio_iafront.data.saving import save_partitioned


def save_clustered_data(dataset:pandas.DataFrame, saida:str):
    date_first = os.path.join(saida, 'date_first')
    cluster_first = os.path.join(saida, 'cluster_first')

    save_partitioned(dataset, date_first, ['data', 'hora', 'cluster_label'])
    save_partitioned(dataset, cluster_first, ['cluster_label', 'data', 'hora'])