import click
import pandas
from bokeh.io import output_file, save
from functools import partial

from bokeh.layouts import gridplot
from desafio_iafront.jobs.graphics.utils import plot_scatter, plot_histogram
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.common import filter_date, columns_to_scale, get_feature_index


@click.command()
@click.option('--dataframe-path', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=False, file_okay=True))
@click.option('--feature', type=click.Choice(columns_to_scale), help="Coluna dos dados para usar no eixo x")
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
def histogram_scale_analysis(dataframe_path: str, saida: str, feature:str, data_inicial, data_final):
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    dataframe = read_partitioned_json(dataframe_path, filter_function=filter_function)
    output_file(saida)
    feature_values = dataframe[feature]
    figura_before = plot_histogram(feature_values, feature,
                                 title="Histograma para {} antes da escala".format(feature.capitalize()))
    feature_index = get_feature_index(feature)
    features_values = dataframe['features']
    feature_values = [x[feature_index] for x in features_values.values.tolist()]
    feature_values = pandas.Series(feature_values, index=dataframe.index)
    figura_after = plot_histogram(feature_values, feature,
                                   title="Histograma para {} depois da escala".format(feature.capitalize()))
    p = gridplot([[figura_before, figura_after]], toolbar_location=None)
    save(p)


if __name__ == '__main__':
    histogram_scale_analysis()
