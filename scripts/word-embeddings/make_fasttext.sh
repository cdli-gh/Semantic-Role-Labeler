#Script for training fasttext.

#Usage - call the following in the fasttext folder downloadable from https://github.com/facebookresearch/fastText
# ./make_fasttext.sh [path_to_fasttext_exec] [data_file] [skipgram/cbow] [model_output_file]

if [[ $# -ne 4 ]]
then
	echo "Usage: ./make_fasttext.sh [path_to_fasttext_exec] [data_file] [skipgram/cbow] [model_output_file]"
	exit
fi


if [[ $3 == "cbow" ]]
then
	$1 cbow -input $2 -output $4
elif [[ $3 == "skipgram" ]]
then
	$1 skipgram -input $2 -output $4
else
	echo "Usage: ./make_fasttext.sh [path_to_fasttext_exec] [data_file] [skipgram/cbow] [model_output_file]"
	exit
fi