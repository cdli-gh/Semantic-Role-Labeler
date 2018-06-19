# Semantic Role Labeling system for Sumerian

This project is a work undertaken for Google Summer of Code - GSoC 2018 under the organisation CDLI.
Its larger goal is to develop a standalone semantic role labeler for the Sumerian language.


## Contents

* **[data](data)** - Contains all the data files required for the project. These contain _non-processed_ raw data files which are download  
	* [cdli-data](data/cdli-data) : Has the parallel data from the CDLI-UrIII corpus - contains normalised files which have NUMB and ordNUMB for numbers, etc. Downloaded from https://github.com/cdli-gh/mtaac_cdli_ur3_corpus
	* [etcsl](data/etcsl) : It contains all the etcsl files provided by http://ota.ox.ac.uk/desc/2518 , which includes XML versions of the transliterations & the translations of the complete etcsl corpus.
	* [preproposal-data](data/preproposal-data) : Contains data files from the pre-proposal phase.
	* [misc](data/misc) : Miscallenous data files.

* **[embeddings](embeddings)** - Contains trained word2vec vectors trained on monolingual Sumerian data using the skipgram as well as cbow word vector models.
	* [skipgram](embeddings/skipgram) : It contains word vectors trained using the skipgram model - contains tweaking of various parameters like no. of dimensions (50, 100, 200, 300), usage of hierarchical softmax(_indicated by _hs_ in the respective stored files_), and change in the window size while training(either 3 or 4 context words). 
	* [cbow](embeddings/cbow) : Same as above except the method of training used the Continuous Bag of Words(CBoW) model.


* **[scripts](scripts)** - Contains all the scripts used in the project. Usage mechanisms for each of the files are provided in the header of the scripts.
	* [alignments](scripts/alignments) : Has scripts which modify/deal with word aligned Sumerian-English data.
		* [label_to_word.py](scripts/alignments/label_to_word.py) Script for creating words-aligned representation from Pharaoh format index-labeled aligned data. 
	* []

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

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.