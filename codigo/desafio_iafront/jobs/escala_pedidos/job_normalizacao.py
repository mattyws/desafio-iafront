import click
from desafio_iafront.jobs.escala_pedidos.constants import scale_methods
from sklearn.preprocessing import Normalizer, StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler, PowerTransformer

from desafio_iafront.data.saving import save_partitioned
from desafio_iafront.jobs.common import prepare_dataframe, transform


@click.command()
@click.option('--visitas-com-conversao', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--departamentos', type=str, help="Departamentos separados por virgula")
@click.option('--metodo-escala', type=click.Choice(scale_methods),
              help="Escolha o método de escala usado")
def main(visitas_com_conversao, saida, data_inicial, data_final, departamentos, metodo_escala):
    departamentos_lista = [departamento.strip() for departamento in departamentos.split(",")]

    result = prepare_dataframe(departamentos_lista, visitas_com_conversao, data_inicial, data_final)

    # Faz a escala dos valores
    scaler = None
    if metodo_escala == "normalizer":
        scaler = Normalizer()
    elif metodo_escala == "standard":
        scaler = StandardScaler()
    elif metodo_escala == "min_max":
        scaler = MinMaxScaler()
    elif metodo_escala == "max_abs":
        scaler = MaxAbsScaler()
    elif metodo_escala == "robust":
        scaler = RobustScaler()
    elif metodo_escala == "power":
        scaler = PowerTransformer()
    result_scaled = transform(result, scaler)

    # salva resultado
    save_partitioned(result_scaled, saida, ['data', 'hora'])


if __name__ == '__main__':
    main()
