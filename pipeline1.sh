#!/bin/bash

helpFunction()
{
   echo ""
   echo "Usage: $0 -i 01/06/2020 -f 31/07/2020 -p pedidos/ -v visitas/ -r produtos.csv -s saida/"
   echo -e "\t-i Data de início escolhido para os dados"
   echo -e "\t-f Data final escolhida para os dados"
   echo -e "\t-p Diretório dos pedidos particionados"
   echo -e "\t-v Diretório de visitas particionadas"
   echo -e "\t-r Arquivo .csv dos produtos"
   echo -e "\t-s Diretório de saída onde serão armazenados os objetos gerados aqui"
   exit 1 # Exit script after printing help
}

while getopts "i:f:p:v:r:s:" opt
do
   case "$opt" in
      i ) data_inicial="$OPTARG" ;;
      f ) data_final="$OPTARG" ;;
      p ) pedidos="$OPTARG" ;;
      v ) visitas="$OPTARG" ;;
      r ) produtos="$OPTARG" ;;
      s ) saida="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$data_inicial" ] || [ -z "$data_final" ] || [ -z "$pedidos" ] || [ -z "$visitas" ] || [ -z "$produtos" ] || [ -z "$saida" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

dir_saida="$saida/visitas_particionadas/"
if [ ! -d "$dir_saida" ]; then
   prepara-pedidos --pedidos $pedidos --visitas $visitas --produtos $produtos --saida $dir_saida --data-inicial $data_inicial --data-final $data_final
fi
analise_conversao_departamento="$saida/analise_conversao_departamento.html"
if [ ! -f "$analise_conversao_departamento" ]; then
   analise-conversao-por-departamento --visitas-com-conversao $dir_saida --saida $analise_conversao_departamento --data-inicial $data_inicial --data-final $data_final
fi
