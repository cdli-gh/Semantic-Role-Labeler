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