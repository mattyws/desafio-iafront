features='frete prazo preco'
echo $features
methods='normalizer maxabs minmax power robust standard'
input_dir=$1
output_dir=$2
departamento=$3
data_inicial=$4
data_final=$5
for m in $methods; do    
	escala-visitas --visitas-com-conversao $input_dir --saida $output_dir/visitas_escaladas_$m/ --data-inicial $data_inicial --data-final $data_final --metodo-escala $m --departamentos $departamento
done



