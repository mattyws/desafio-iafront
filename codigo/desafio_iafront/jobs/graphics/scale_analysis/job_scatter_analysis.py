import click
import pandas
from bokeh.io import output_file, save
from functools import partial

from bokeh.layouts import gridplot
from desafio_iafront.jobs.graphics.utils import plot_scatter
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.common import filter_date, columns_to_scale, get_feature_index


@click.command()
@click.option('--dataframe-path', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=False, file_okay=True))
@click.option('--x-axis', type=click.Choice(columns_to_scale), help="Coluna dos dados para usar no eixo x")
@click.option('--y-axis', type=click.Choice(columns_to_scale), help="Coluna dos dados para usar no eixo y")
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
def scatter_scale_analysis(dataframe_path: str, saida: str, x_axis, y_axis, data_inicial, data_final):
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    dataframe = read_partitioned_json(dataframe_path, filter_function=filter_function)

    output_file(saida)

    x_values = dataframe[x_axis]
    y_values = dataframe[y_axis]

    figura_before = plot_scatter(x_values, y_values, x_axis, y_axis,
                                 title="Antes da escala: {} x {}".format(x_axis.capitalize(), y_axis.capitalize()))
    x_feature_index = get_feature_index(x_axis)
    y_feature_index = get_feature_index(y_axis)

    features_values = dataframe['features']
    x_values = [x[x_feature_index] for x in features_values.values.tolist()]
    x_values = pandas.Series(x_values, index=dataframe.index)
    y_values = [y[y_feature_index] for y in features_values.values.tolist()]
    y_values = pandas.Series(y_values, index=dataframe.index)

    figura_after = plot_scatter(x_values, y_values, x_axis, y_axis,
                                 title="Depois da escala: {} x {}".format(x_axis.capitalize(), y_axis.capitalize()))

    p = gridplot([[figura_before, figura_after]], toolbar_location=None)

    save(p)


if __name__ == '__main__':
    scatter_scale_analysis()
