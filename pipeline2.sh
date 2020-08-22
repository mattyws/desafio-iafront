#!/bin/bash

helpFunction()
{
   echo ""
   echo "Usage: $0 -i 01/06/2020 -f 31/07/2020 -e visitas_convertidas/ -s saida/ -d cama_mesa_banho -a data "
   echo -e "\t-i Data de início escolhido para os dados"
   echo -e "\t-f Data final escolhida para os dados"
   echo -e "\t-e Diretório das vissitas particionadas por departamento"
   echo -e "\t-s Diretório de saída onde serão armazenados os objetos gerados aqui"
   echo -e "\t-d Departamento usado para as análises"
   echo -e "\t-a Partionamento dos clusters para análise temporal"   
   exit 1 # Exit script after printing help
}

while getopts "i:f:e:s:d:a:" opt
do
   case "$opt" in
      i ) data_inicial="$OPTARG" ;;
      f ) data_final="$OPTARG" ;;
      e ) input_dir="$OPTARG" ;;
      s ) output_dir="$OPTARG" ;;
      d ) departamento="$OPTARG" ;;
      a ) agrupar_por="$OPTARG" ;;      
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$data_inicial" ] || [ -z "$data_final" ] || [ -z "$input_dir" ] || [ -z "$output_dir" ] || [ -z "$departamento" ] || [ -z "$agrupar_por" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

echo "Executando escala dos dados"
script_file='executa_escala_dados.sh'
if [ ! -f "$script_file" ]; then
   echo "Script $script_file not found"
   exit 1
fi
sh $script_file $input_dir $output_dir $departamento $data_inicial $data_final

echo "Clusterizando dados"
script_file='executa_clusterings.sh'
if [ ! -f "$script_file" ]; then
   echo "Script $script_file not found"
   exit 1
fi
sh $script_file $output_dir $data_inicial $data_final

echo "Criando análise temporal para os dados clusterizados"
script_file='executa_analise_conversao_temporal_clusters.sh'
if [ ! -f "$script_file" ]; then
   echo "Script $script_file not found"
   exit 1
fi
sh $script_file $output_dir $agrupar_por $data_inicial $data_final