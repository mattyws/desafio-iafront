import os
from functools import partial

import click
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.data.saving import save_partitioned
from desafio_iafront.jobs.common import filter_date
from desafio_iafront.jobs.particiona_conversao.utils import add_minutes_to_dataset, aggregate_conversao, \
    columns_to_aggregate


@click.command()
@click.option('--dataset-clustered', type=click.Path(exists=True))
@click.option('--agregar-por', type=click.Choice(columns_to_aggregate))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
def main(dataset_clustered:str, agregar_por:str, saida, data_inicial, data_final):
    dataset_clustered = os.path.join(dataset_clustered, 'cluster_first')
    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    dataset = read_partitioned_json(file_path=dataset_clustered, filter_function=filter_function)
    if agregar_por == 'minuto':
        dataset = add_minutes_to_dataset(dataset)
    label_index = columns_to_aggregate.index(agregar_por)
    columns = columns_to_aggregate[:label_index+1]
    aggregated_conversao = aggregate_conversao(dataset, columns)
    print(aggregated_conversao)
    save_partitioned(aggregated_conversao, saida, ['cluster_label'] + columns)

if __name__ == '__main__':
    main()