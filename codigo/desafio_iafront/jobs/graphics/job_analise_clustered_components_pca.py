from functools import partial

import click
import os
import numpy as np
import pandas
from bokeh.io import export_png

from bokeh.io.output import output_file
from bokeh.io.saving import save
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.escala_pedidos.constants import scale_methods
from desafio_iafront.jobs.graphics.utils import plot_vbar, transform_pca_2d, set_color, plot_scatter
from sklearn.preprocessing import Normalizer, StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler, PowerTransformer

from desafio_iafront.data.saving import save_partitioned
from desafio_iafront.jobs.common import prepare_dataframe, transform, columns_to_scale, filter_date


@click.command()
@click.option('--dataset-clustered', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=False, file_okay=True))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
def plot_analise_pontos_cluster(dataset_clustered:str, saida, data_inicial, data_final):
    dataset_clustered = os.path.join(dataset_clustered, 'cluster_first')
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    dataset = read_partitioned_json(file_path=dataset_clustered, filter_function=filter_function)
    output_file(saida)

    print("Transform with pca")
    features = np.asarray(dataset['features'].tolist())
    new_space = transform_pca_2d(features)
    print("End with pca")
    clusters = dataset['cluster_label'].unique().tolist()
    # Defining colors
    colormap = dict()
    for num, cluster in enumerate(clusters):
        colormap[cluster] = set_color(num)
    colors = [colormap[x] for x in dataset['cluster_label']]
    x = pandas.Series([value[0] for value in new_space])
    y = pandas.Series([value[1] for value in new_space])

    p = plot_scatter(x, y, x_axis='x', y_axis='y', color=colors, title="Análise distribuição clusters (features reduzidas por PCA)")
    save(p)


if __name__ == '__main__':
    plot_analise_pontos_cluster()
