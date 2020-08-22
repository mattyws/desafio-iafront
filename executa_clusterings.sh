methods='minmax robust standard'
output_dir=$1
data_inicial=$2
data_final=$3
data_inicial_dir="$( echo "$data_inicial" | tr '/' '-')"
data_final_dir="$( echo "$data_final" | tr '/' '-')"
dir_analise=$output_dir/analise_cluster_$data_inicial_dir\_to_$data_final_dir
mkdir $dir_analise
for m in $methods; do
	echo $m	
	echo "Kmeans clustering"
	cluster_output_dir=$output_dir/kmeans_$m/
	if [ ! -d "$cluster_output_dir" ]; then
		kmeans-clustering --dataset $output_dir/visitas_escaladas_$m/  --number-of-cluster 4 --saida $cluster_output_dir --data-inicial $data_inicial --data-final $data_final		
	fi	
	analise_file_name=$dir_analise/kmeans_instancias_$m.html
	echo $analise_file_name
	if [ ! -f "$analise_file_name" ]; then
		analise-instancias-cluster --dataset-clustered $cluster_output_dir --saida $analise_file_name --data-inicial $data_inicial --data-final $data_final
	fi
	analise_file_name=$dir_analise/kmeans_conversao_$m.html
	echo $analise_file_name
	if [ ! -f "$analise_file_name" ]; then
		analise-conversao-cluster --dataset-clustered $cluster_output_dir --saida $analise_file_name --data-inicial $data_inicial --data-final $data_final
	fi


	echo "Birch clustering"
	cluster_output_dir=$output_dir/birch_$m/
	if [ ! -d "$cluster_output_dir" ]; then
		birch-clustering --dataset $output_dir/visitas_escaladas_$m/  --number-of-cluster 4 --saida $cluster_output_dir --data-inicial $data_inicial --data-final $data_final		
	fi	
	analise_file_name=$dir_analise/birch_instancias_$m.html
	if [ ! -f "$analise_file_name" ]; then
		analise-instancias-cluster --dataset-clustered $cluster_output_dir --saida $analise_file_name --data-inicial $data_inicial --data-final $data_final
	fi
	analise_file_name=$dir_analise/birch_conversao_$m.html
	if [ ! -f "$analise_file_name" ]; then
		analise-conversao-cluster --dataset-clustered $cluster_output_dir --saida $analise_file_name --data-inicial $data_inicial --data-final $data_final
	fi
	
	echo "Gaussian mixtures clustering" 
	cluster_output_dir=$output_dir/gaussian_$m/
	if [ ! -d "$cluster_output_dir" ]; then
		gaussian-mixtures-clustering --dataset $output_dir/visitas_escaladas_$m/ --number-of-cluster 4 --saida $cluster_output_dir --data-inicial $data_inicial --data-final $data_final		
	fi	
	analise_file_name=$dir_analise/gaussian_instancias_$m.html
	if [ ! -f "$analise_file_name" ]; then
		analise-instancias-cluster --dataset-clustered $cluster_output_dir --saida $analise_file_name --data-inicial $data_inicial --data-final $data_final
	fi
	analise_file_name=$dir_analise/gaussian_conversao_$m.html
	if [ ! -f "$analise_file_name" ]; then
		analise-conversao-cluster --dataset-clustered $cluster_output_dir --saida $analise_file_name --data-inicial $data_inicial --data-final $data_final
	fi

done

#agglomerative-clustering --dataset --number-of-cluster --saida --data-inicial --data-final
#kmeans-clustering --dataset --number-of-cluster --saida --data-inicial --data-final
#optics-clustering --dataset --saida --data-inicial --data-final
#affinity-clustering --dataset (uma execução para cada escala) --saida (diretório) --data-inicial --data-final
#spectral-clustering --dataset --number-of-cluster --saida --data-inicial --data-final
