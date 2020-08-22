features='frete prazo preco'
echo $features
methods='normalizer maxabs minmax power robust standard'
output_dir=$1
data_inicial=$2
data_final=$3
data_inicial_dir="$( echo "$data_inicial" | tr '/' '-')"
data_final_dir="$( echo "$data_final" | tr '/' '-')"
dir_analise=$output_dir/analise_scale_$data_inicial_dir\_to_$data_final_dir
mkdir $dir_analise
for m in $methods; do    
    for f in $features; do
        echo $m, $f
		escala-analise-distribuicao-histograma --dataframe-path $output_dir/visitas_escaladas_$m/ --saida $dir_analise/histogram_$m\_$f.html --feature $f --data-inicial $data_inicial --data-final $data_final        
    done
done



