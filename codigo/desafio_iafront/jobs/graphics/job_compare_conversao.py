from functools import partial

import click
import os

from bokeh.io.output import output_file
from bokeh.io.saving import save
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.escala_pedidos.constants import scale_methods
from desafio_iafront.jobs.graphics.utils import plot_vbar
from sklearn.preprocessing import Normalizer, StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler, PowerTransformer

from desafio_iafront.data.saving import save_partitioned
from desafio_iafront.jobs.common import prepare_dataframe, transform, columns_to_scale, filter_date


@click.command()
@click.option('--dataset-clustered', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=False, file_okay=True))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
def plot_conversao(dataset_clustered:str, saida, data_inicial, data_final):
    dataset_clustered = os.path.join(dataset_clustered, 'cluster_first')
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    dataset = read_partitioned_json(file_path=dataset_clustered, filter_function=filter_function)
    output_file(saida)

    clusters = dataset['cluster_label'].unique().tolist()
    x = [('Cluster:{}'.format(cluster), convertido) for cluster in clusters for convertido in ['Convertido', 'Não-convertido']]
    clusters_conversao = dict()

    counts = []
    for cluster in clusters:
        convertido_counts = dataset[dataset['cluster_label'] == cluster]['convertido'].value_counts().to_dict()
        counts.append(convertido_counts[1])
        counts.append(convertido_counts[0])
    print(clusters_conversao)
    p = plot_vbar(x, counts, title="Conversão por cluster")
    save(p)


    # salva resultado
    # save_partitioned(result_scaled, saida, ['data', 'hora'])


if __name__ == '__main__':
    plot_conversao()
