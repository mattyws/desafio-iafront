import os
from functools import partial

import click
from datetime import timedelta
import multiprocessing as mp

import numpy
import sys
from desafio_iafront.data.dataframe_utils import read_csv
from desafio_iafront.jobs.pedidos.utils import partition_data_by_department


@click.command()
@click.option('--pedidos', type=click.Path(exists=True))
@click.option('--visitas', type=click.Path(exists=True))
@click.option('--produtos', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
def main(pedidos, visitas, produtos, saida, data_inicial, data_final):
    produtos_df = read_csv(produtos)
    produtos_df["product_id"] = produtos_df["product_id"].astype(str)
    delta: timedelta = (data_final - data_inicial)
    date_partitions = [data_inicial.date() + timedelta(days=days) for days in range(delta.days)]
    total_partitions = len(date_partitions)
    date_partitions_split = numpy.array_split(date_partitions, 4)
    # Usando multiprocessing para acelerar o processo de consumo das partições
    # Tendo em vista que os resultados finais estão sendo salvos em disco, facilita o uso da biblioteca
    with mp.Pool(processes=4) as pool:
        manager = mp.Manager()
        manager_queue = manager.Queue()
        # Usando partial para fixar os valor nas variáveis
        process_func = partial(partition_data_by_department, pedidos=pedidos, produtos_df=produtos_df,
                               saida=saida, visitas=visitas, manager_queue=manager_queue)
        map_obj = pool.map_async(process_func, date_partitions_split)
        consumed = 0
        while not map_obj.ready() or manager_queue.qsize() != 0:
            for _ in range(manager_queue.qsize()):
                manager_queue.get()
                consumed += 1
            sys.stderr.write('\rPartições consumidas {0:%}'.format(consumed / total_partitions))
    print("\nTudo pronto!")

if __name__ == '__main__':
    main()
