features='frete prazo preco cep_prefixo'
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
    for f1 in $features; do
        for f2 in $features; do
            if [ "$f1" != "$f2" ]; then
                if [ "$f1" \> "$f2" ]; then
                    arquivo_saida=$dir_analise/$m\_$f1\_x_$f2.html
                    x=$f1
                    y=$f2
                else
                    arquivo_saida=$dir_analise/$m\_$f2\_x_$f1.html
                    x=$f2
                    y=$f1
                fi
                if  [ ! -f "$arquivo_saida" ]; then
                    echo $arquivo_saida
                    escala-analise-distribuicao-scatter --dataframe-path $output_dir/visitas_escaladas_$m/ --saida $arquivo_saida --x-axis $x --y-axis $y --data-inicial $data_inicial --data-final $data_final
		fi
            fi
        done
#	escala-analise-distribuicao-histograma --dataframe-path visitas_escaladas_$m/ --saida $dir_analise/histogram_$m\_$f.html --feature $f --data-inicial $data_inicial --data-final $data_final        
    done
done


#escala-analise-distribuicao-scatter --dataframe-path visitas_escaladas_normalizer/ --saida normalizer_preço_x_prazo.html --x-axis preco --y-axis prazo --data-inicial 01/06/2020 --data-final 08/06/2020

