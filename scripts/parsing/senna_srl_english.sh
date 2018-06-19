############################################################
#
# Usage : [./senna_srl_english.sh] [path_to_senna_dir] [input_file] [output_file]
#
############################################################

#Function to get the absolute filepath
function absolute_path() {
  filename=$1
  parentdir=$(dirname "${filename}")

  if [ -d "${filename}" ]; then
      echo "$(cd "${filename}" && pwd)"
  elif [ -d "${parentdir}" ]; then
    echo "$(cd "${parentdir}" && pwd)/$(basename "${filename}")"
  fi
}

#Exit program if no. of arguments are not equal to 3
if [[ $# -ne 3 ]]
then
	echo "Usage: ./senna_srl_english.sh [path_to_senna_dir] [input_file] [output_file]"
	exit
fi

#Store the input file in a variable
INPUT_FILE=$(absolute_path $2)
OUTPUT_FILE=$(absolute_path $3)

#RUN THE SCRIPT FOR SENNA
echo "Getting SRL tags..."
cd $1;
./senna -srl < $INPUT_FILE > $OUTPUT_FILE;
echo "Done!"