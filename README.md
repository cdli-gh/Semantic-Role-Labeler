# Semantic Role Labeling system for Sumerian

This project is a work undertaken for Google Summer of Code - GSoC 2018 under the organisation CDLI.
Its larger goal is to develop a standalone semantic role labeler for the Sumerian language.


## Contents

* **[data](data)** - Contains all the data files required for the project. These contain _non-processed_ raw data files which are download  
	* [cdli-data](data/cdli-data) : Has the parallel data from the CDLI-UrIII corpus - contains normalised files which have NUMB and ordNUMB for numbers, etc. Downloaded from https://github.com/cdli-gh/mtaac_cdli_ur3_corpus
	* [etcsl](data/etcsl) : It contains all the etcsl files provided by http://ota.ox.ac.uk/desc/2518 , which includes XML versions of the transliterations & the translations of the complete etcsl corpus.
	* [preproposal-data](data/preproposal-data) : Contains data files from the pre-proposal phase.
	* [misc](data/misc) : Miscellanous data files.

* **[embeddings](embeddings)** - Contains trained word2vec vectors trained on monolingual Sumerian data using the skipgram as well as cbow word vector models.
	* [skipgram](embeddings/skipgram) : It contains word vectors trained using the skipgram model - contains tweaking of various parameters like no. of dimensions (50, 100, 200, 300), usage of hierarchical softmax(_indicated by _hs_ in the respective stored files_), and change in the window size while training(either 3 or 4 context words). 
	* [cbow](embeddings/cbow) : Same as above except the method of training used is the Continuous Bag of Words(CBoW) model.


* **[scripts](scripts)** - Contains all the scripts used in the project. Usage mechanisms for each of the files are provided in the header of the scripts.
	* **[alignments](scripts/alignments)** - Has scripts which modify/deal with word aligned Sumerian-English data.
		* [label_to_word.py](scripts/alignments/label_to_word.py) : Script for creating words-aligned representation from Pharaoh format index-labeled aligned data. 
	* **[error-checking](scripts/error-checking)** - Scripts for error handling and analysing errors in files.
		* [error_check_alignment.py](scripts/error-checking/error_check_alignment.py) : Script for checking the percentage of error sentences in a word-aligned word-labeled Sum-Eng corpus.
	* **[parsing](scripts/parsing)** - Scripts related to/for parsing English source data.
		* [mateparsing.py](scripts/parsing/mateparsing.py) : It is used for running mate-tools on the data to get the SRL labels for English. A python wrapper of mate-tools is used.
		* [senna_srl_english.sh](scripts/parsing/senna_srl_english.sh) : Used for obtaining SENNA's SRL parser output on the English data.
	* **[scraping](scripts/scraping)** - Scripts for scraping data and reformating/storing it in a readable and coherent fashion.
		* [scrape-etcsl-XML.py](scripts/scraping/scrape-etcsl-XML.py) : It is used for scraping transliterations from ETCSL XML files. Reference: https://github.com/niekveldhuis/Digital-Assyriology/blob/master/Scrape-etcsl/scrape-etcsl-XML.ipynb
		* [modified-scrape-etcsl-translations-XML.py](scripts/scraping/modified-scrape-etcsl-translations-XML.py) : Modified version of the above script for scraping the translations from the ETCSL XML translations data file.

	* **[word-embeddings](scripts/word-embeddings)** - Scripts for generating word vectors from monolingual data.
		* [make_fasttext.sh](scripts/word-embeddings/make_fastttext.sh) : Make word vectors using the FastText algorithm.
		* [make_word_vectors.py](scripts/word-embeddings/make_word_vectors.py) : Inducing word vectors using the traditional word2vec algorithms.

	* **[processsing](scripts/processing)** - Scripts for processing data and other files.
		* [create_parallel.py](scripts/processing/create_parallel.py) : Script for creating parallel aligned data from the existing XML parsed data for ETCSL. Converts the sentence transliterations to combine into paragraphs.
		* [etcsl_cdli_unifier.py](scripts/processing/etcsl_cdli_unifier.py) : Uses Ilya's script from the ```transliteration``` python class ([link here](https://github.com/cdli-gh/mtaac_cdli_ur3_corpus/blob/master/scripts/scripts_translated.py)) to normalise the tokenized data from an input file. (in this case, the ETCSL files)
		* [sentence_segment.py](scripts/processing/sentence_segment.py) : A simple heuristic to segment sentences in the CDLI English corpus - mainly used before applying mate-tools to the English data for better coverage.
		* [unicode_decode.py](scripts/processing/unicode_decode.py) : Script for normalising the english character set in the source English data.
		* [unnormalise.py](scripts/processing/unnormalise.py) : Script for removing normalisation elements from the CDLI data, and also making the parallel data ready as input for the _efmaral_ & _fast_align_ word aligners.

* **[processed-data](processed-data)** - Contains all the processed data that has been used in the course of the workflow of the project.
	* **[cdli/un-normalised](processed-data/cdli/un-normalised)** - Has the processed CDLI data which is un-normalised and also ready for use by word aligning software. A sample file is described below:
		* [sum_eng_train_unnorm.csv](processed-data/cdli/un-normalised/sum_eng_train_unnorm.csv) : Contains the input data (unnormalised) which contains side-by-side Sumerian sentences along with their English counterparts separated by ``` ||| ``` with the spaces. This format is required as input to word-aligners. 
		* ... : Other files similar to the above.
	* **[etcsl](processed-data/etcsl)** - Contains ETCSL processed data.
		* [parallel-etcsl-eng](processed-data/etcsl/parallel-etcsl-eng) : Contains English texts arranged in paragraphs from the etcsl corpus.
		* [parallel-etcsl-sum](processed-data/etcsl/parallel-etcsl-sum) : Sumerian texts from ETCSL arranged paragraph-by-paragraph rather than line-by-line as in the original corpus.
		* [old-proc-eng](processed-data/etcsl/old-proc-eng) : Processed data for English as returned by the ETCSL scraper script.
		* [old-proc-sum](processed-data/etcsl/old-proc-sum) : Processed data for Sumerian as returned by the ETCSL scraper script. Difference is this has line-by-line transliterations along with the identification information for each text.

	* **[unified](processed-data/unified)** - The plan is to include all unified parallel data here, for ETCSL and ETCSRI after converting to ASCII and normalising it.
		* [etcsl-transliteration-normalised.dat](processed-data/etcsl/unified/etcsl-transliteration-normalised.dat) : A sample snapshot of the [unifier script](scripts/processing/etcsl_cdli_unifier.py) from above on etcsl text _c.1.1.1.txt_


	*  **[misc](processed-data/misc)** - Miscellaneous processed data. Currently contains outputs for a few sentence-combining heuristic functions for the CDLI-UrIII data.


### Prerequisites

What things you need to install the software and how to install them.
Will be updated as the project progresses.


### Installing

Will be updated as the project progresses.


## Contributing

Feel free to send in pull requests to us, we will be happy to incorporate meaningful changes and suggestions.


## Authors

* **Bakhtiyar Syed** - [bakszero](https://github.com/PurpleBooth)

## Mentors

This project is mentored by:

* **Niko Schenk**
* **Ilya Khait**


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.