from functools import partial

import click
import os
import pandas

from bokeh.io.output import output_file
from bokeh.io.saving import save
from bokeh.layouts import gridplot
from desafio_iafront.data.dataframe_utils import read_partitioned_json, read_csv
from desafio_iafront.jobs.escala_pedidos.constants import scale_methods
from desafio_iafront.jobs.graphics.utils import plot_vbar, plot_vbar_stacked
from sklearn.preprocessing import Normalizer, StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler, PowerTransformer

from desafio_iafront.data.saving import save_partitioned
from desafio_iafront.jobs.common import prepare_dataframe, transform, columns_to_scale, filter_date, convert


@click.command()
@click.option('--visitas-com-conversao', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=False, file_okay=True))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--top-ceps', type=click.INT)
@click.option('--departamentos', type=str, help="Departamentos separados por virgula", default=None, required=False)
def plot_conversao_by_cep(visitas_com_conversao:str, saida, data_inicial, data_final, top_ceps:int,
                          departamentos):

    if departamentos is not None:
        departamentos_lista = [departamento.strip() for departamento in departamentos.split(",")]
    else:
        departamentos_lista = None

    dataset = prepare_dataframe(departamentos_lista, visitas_com_conversao, data_inicial, data_final)

    ceps = dataset['cep_prefixo'].value_counts().sort_values(ascending=False)
    ceps = ceps.index.tolist()[:top_ceps]
    convertido = []
    nao_convertido = []
    for cep in ceps:
        cep_df = dataset[dataset['cep_prefixo'] == cep]
        conversao_count: pandas.Series = cep_df['convertido'].value_counts()
        if 1 in conversao_count.index:
            convertido.append(conversao_count[1])
        else:
            convertido.append(0)
        if 0 in conversao_count.index:
            nao_convertido.append(conversao_count[0])
        else:
            nao_convertido.append(0)
    ceps = [str(cep) for cep in ceps]
    data = {'categories': ceps, 'Convertido': convertido, 'Não Convertido': nao_convertido}
    figure = plot_vbar_stacked(ceps, data, ['Convertido', 'Não Convertido'],
                               title="Conversão para os top {} ceps nos departamentos {}".format(top_ceps, departamentos),
                               plot_width=1500)
    output_file(saida)
    save(figure)


if __name__ == '__main__':
    plot_conversao_by_cep()
