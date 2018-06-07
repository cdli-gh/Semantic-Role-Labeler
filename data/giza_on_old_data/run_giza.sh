#!/bin/bash

## SEE https://hoxuanvinh.wordpress.com/2016/01/27/using-giza-for-aligning-words-with-sh-file-on-ubuntu/


declare -a arr=("sumerian:english" "english:sumerian")

for i in "${arr[@]}"
do
a=(${i//:/ })

##main variables:
source_name=${a[0]}
target_name=${a[1]}
output_path="data/output/${source_name}_${target_name}"

##files:
source_plain="data/${source_name}"
target_plain="data/${target_name}"
source_vcb="data/${source_name}.vcb"
target_vcb="data/${target_name}.vcb"
source_vcb_classes="data/${source_name}.vcb.classes" 
target_vcb_classes="data/${target_name}.vcb.classes"
source_target_snt="data/${source_name}_${target_name}.snt"  
source_target_cooc="data/${source_name}_${target_name}.cooc"

##commands:
plain2snt="./GIZA++-v2/plain2snt.out"
mkcls="./mkcls-v2/mkcls"
snt2cooc="./GIZA++-v2/snt2cooc.out"
giza="./GIZA++-v2/GIZA++"

##execute:
echo "$plain2snt $source_plain $target_plain"
$plain2snt $source_plain $target_plain

echo "$mkcls -p$source_plain -V$source_vcb_classes"
$mkcls -p$source_plain -V$source_vcb_classes

echo "$mkcls -p$target_plain -V$target_vcb_classes"
$mkcls -p$target_plain -V$target_vcb_classes

echo "$snt2cooc $source_vcb $target_vcb $source_target_snt > $source_target_cooc"
$snt2cooc $source_vcb $target_vcb $source_target_snt > $source_target_cooc


mkdir -p $output_path
echo "$giza -S $source_vcb -T $target_vcb -C $source_target_snt -CoocurrenceFile $source_target_cooc -o Result -outputpath $output_path"
$giza -S $source_vcb -T $target_vcb -C $source_target_snt -CoocurrenceFile $source_target_cooc -o Result -outputpath $output_path

done

