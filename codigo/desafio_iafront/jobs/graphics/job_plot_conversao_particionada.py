import click
import pandas
from bokeh.io import output_file, save
from functools import partial


from desafio_iafront.jobs.graphics.utils import plot, plot_cluster_temporal_conversao
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.common import filter_date
from desafio_iafront.jobs.particiona_dados.utils import columns_to_aggregate


@click.command()
@click.option('--dataset-conversao-agregada', type=click.Path(exists=True))
@click.option('--agregar-por', type=click.Choice(columns_to_aggregate))
@click.option('--saida', type=click.Path(exists=False, dir_okay=False, file_okay=True))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
def analise_conversao_temporal(dataset_conversao_agregada: str, agregar_por:str, saida:str, data_inicial, data_final):
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    dataframe = read_partitioned_json(dataset_conversao_agregada, filter_function=filter_function)

    if agregar_por == 'data':
        dataframe['label'] = pandas.to_datetime(dataframe['data'], format="%Y-%m-%d")
    elif agregar_por == 'hora':
        dataframe.loc[:, 'hora'] = dataframe['hora'].apply('{0:0>2}'.format)
        dataframe['label'] = pandas.to_datetime(dataframe.apply(lambda x: "{} {}".format(x['data'], x['hora']), axis=1),
                                                format="%Y-%m-%d %H")
    elif agregar_por == 'minuto':
        dataframe['label'] = pandas.to_datetime(dataframe.apply(lambda x: "{} {}:{}".format(x['data'], x['hora'],
                                                                                            x['minuto']), axis=1),
                                                format="%Y-%m-%d %H:%M")
    dataframe = dataframe.sort_values(by=['label'])

    output_file(saida)

    figura = plot_cluster_temporal_conversao(dataframe, title="Análise conversão temporal de clusteres")

    save(figura)


if __name__ == '__main__':
    analise_conversao_temporal()
