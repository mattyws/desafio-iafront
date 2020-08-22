methods='minmax robust standard'
cluster_methods='kmeans gaussian birch'
output_dir=$1
agregar_por=$2
data_inicial=$3
data_final=$4
data_inicial_dir="$( echo "$data_inicial" | tr '/' '-')"
data_final_dir="$( echo "$data_final" | tr '/' '-')"
dir_analise=$output_dir/analise_conversao_cluster_$data_inicial_dir\_to_$data_final_dir
mkdir $dir_analise
for m in $methods; do
	for cm in $cluster_methods; do
		echo $cm, $m
		input_dir=$output_dir/$cm\_$m/
		partitioned_output_dir=$output_dir/$cm\_$m\_conversao_$agregar_por/
		analise_file_name=$dir_analise/$cm\_conversao_temporal_$m.html
		if [ ! -d "$analise_file_name" ]; then
			particiona-conversao --dataset-clustered $input_dir --agregar-por $agregar_por --saida $partitioned_output_dir --data-inicial $data_inicial --data-final $data_final
		fi
		if [ ! -f "$analise_file_name" ]; then
			analise-conversao-temporal --dataset-conversao-agregada $partitioned_output_dir --agregar-por $agregar_por --saida $analise_file_name --data-inicial $data_inicial --data-final $data_final
		fi		
	done
done
