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
from desafio_iafront.jobs.common import prepare_dataframe, transform, columns_to_scale, filter_date, convert, \
    extract_path_partitions_and_values
import multiprocessing as mp
import sys

def create_data_for_plot(departamento:str, path:str, filter_function, manager_queue:mp.Queue):
    partition_path = os.path.join(path, f"departamento={departamento}")
    departamento_df = read_partitioned_json(file_path=partition_path, filter_function=filter_function)
    if departamento_df.empty:
        manager_queue.put(departamento)
        return None
    departamento_df = convert(departamento_df)
    data = dict()
    data[departamento] = dict()
    conversao_value_count: pandas.Series = departamento_df['convertido'].value_counts()
    if 1 in conversao_value_count.index:
        data[departamento]['Convertido'] = conversao_value_count[1]
    else:
        data[departamento]['Convertido'] = 0
    if 0 in conversao_value_count.index:
        data[departamento]['Não Convertido'] = conversao_value_count[0]
    else:
        data[departamento]['Não Convertido'] = 0
    data[departamento]['Total'] = data[departamento]['Não Convertido'] + data[departamento]['Convertido']
    manager_queue.put(departamento)
    return data

def multiprocessing_create_data_for_plot(path:str, values, filter_function):
    with mp.Pool(processes=4) as pool:
        total_partitions = len(values)
        manager = mp.Manager()
        manager_queue = manager.Queue()
        # data = create_data_for_plot(values[0], path, filter_function, manager_queue)
        # data.update(create_data_for_plot(values[1], path, filter_function, manager_queue))
        process_func = partial(create_data_for_plot, path=path, filter_function=filter_function, manager_queue=manager_queue)
        map_obj = pool.map_async(process_func, values)
        consumed = 0
        while not map_obj.ready() or manager_queue.qsize() != 0:
            for _ in range(manager_queue.qsize()):
                manager_queue.get()
                consumed += 1
            sys.stderr.write('\rPartições consumidas {0:%}'.format(consumed / total_partitions))
        print()
        result = map_obj.get()
        data = dict()
        for r in result:
            if r is not None:
                data.update(r)
        return data

@click.command()
@click.option('--visitas-com-conversao', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=False, file_okay=True))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
def plot_conversao_by_departament(visitas_com_conversao:str, saida, data_inicial, data_final):
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    feature, values = extract_path_partitions_and_values(visitas_com_conversao)
    if feature == 'departamento':
        data = multiprocessing_create_data_for_plot(visitas_com_conversao, values, filter_function)
        departamentos_sorted = sorted(data.items(), reverse=True, key=lambda kv: (kv[1]['Total'], kv[0]))
        plot_figures = []
        plot_rows = []
        categories = ['Convertido', 'Não Convertido']
        for departamento in departamentos_sorted:
            values = departamento[1]
            values = [values['Convertido'], values['Não Convertido']]
            taxa_conversao = values[0] / (values[0] + values[1])
            figure = plot_vbar(categories, values,
                               title = "Análise de conversão no departamento {} (TC: {:.2f})".format(departamento[0],
                                                                                                     taxa_conversao),
                               plot_width = 500)
            if len(plot_rows) == 3:
                plot_figures.append(plot_rows)
                plot_rows = [figure]
            else:
                plot_rows.append(figure)
        if len(plot_rows) > 0:
            plot_figures.append(plot_rows)

        figure = gridplot(plot_figures, toolbar_location=None)
        output_file(saida)
        save(figure)
    else:
        print('Análise funciona com dados particionados por departamento.')
        exit(1)




if __name__ == '__main__':
    plot_conversao_by_departament()
