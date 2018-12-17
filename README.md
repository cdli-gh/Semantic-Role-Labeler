# Towards building the first Semantic Role Labeling(SRL) system for Sumerian

This project is a work undertaken for Google Summer of Code - GSoC 2018 under the organisation CDLI.
Its larger goal is to develop a standalone semantic role labeler for the Sumerian language.


## Authors

* **Bakhtiyar Syed** - [bakszero](https://github.com/bakszero)

## Mentors

This project is mentored by:

* **Niko Schenk**
* **Ilya Khait**

## Resources

Here is a list of resources developed as part of the project which the community can use:

1. **[SRL projected data](outputs/projected/train/final_nlpnet.txt)** : Contains the projected SRL labeled data for Sumerian. 

2. **[SRL projected data - with collapsed labels](outputs/coarse-labeled/train.txt)** : Contains projected data - with labels from [A0-A5] collapsed to Level 1(L-1) and others like AM-* collapsed to Level-2(L-2).

Please [click here](data_format.dat) for the data format specifications for the above.

Note: The above links are for training data. The `dev/` and `test/` data are in the same parent folder that the current link points to.

## Description

Semantic role labeling (SRL) is a task in Natural Language Processing which helps in detecting the semantic arguments of the predicate/s of a sentence, and then classifies them into various pre-defined semantic categories thus assigning a semantic role to the syntactic constituents.

The larger goal of the project is to develop a supervised semantic role labeling system for Sumerian, a Mesopotamian language spoken in the 3rd millennium B.C.

Advancing in this direction, we propose to first use projections of English annotations onto Sumerian thus creating gold-standard SRL Sumerian data for the research community to use. We will then evaluate our system using existing architectures available for semantic role labeling with the projected SRL data. The final system also involves the production of word embeddings for Sumerian which can be documented and used for improving other downstream tasks like POS tagging, dependency parsing, etc. The developed SRL system will have many potential applications, viz. in the fields of document summarization, machine translation and also towards a better abstract semantic representation of the originally sparse textual data.

## Contents

1. **[data](data)** - Contains all the data files required for the project. These contain _non-processed_ raw data files which are download  
	1. [cdli-data](data/cdli-data) : Has the parallel data from the CDLI-UrIII corpus - contains normalised files which have NUMB and ordNUMB for numbers, etc. Downloaded from https://github.com/cdli-gh/mtaac_cdli_ur3_corpus
	2. [etcsl](data/etcsl) : It contains all the etcsl files provided by http://ota.ox.ac.uk/desc/2518 , which includes XML versions of the transliterations & the translations of the complete etcsl corpus.
	3. [preproposal-data](data/preproposal-data) : Contains data files from the pre-proposal phase.
	4. [misc](data/misc) : Miscellanous data files.
___
2. **[embeddings](embeddings)** - Contains trained word2vec vectors trained on monolingual Sumerian data using the skipgram as well as cbow word vector models.
	1. [skipgram](embeddings/skipgram) : It contains word vectors trained using the skipgram model - contains tweaking of various parameters like no. of dimensions (50, 100, 200, 300), usage of hierarchical softmax(_indicated by _hs_ in the respective stored files_), and change in the window size while training(either 3 or 4 context words). 
	2. [cbow](embeddings/cbow) : Same as above except the method of training used is the Continuous Bag of Words(CBoW) model.
___
3. **[scripts](scripts)** - Contains all the scripts used in the project. Usage mechanisms for each of the files are provided in the header of the scripts.
	1. **[alignments](scripts/alignments)** - Has scripts which modify/deal with word aligned Sumerian-English data.
		* [label_to_word.py](scripts/alignments/label_to_word.py) : Script for creating words-aligned representation from Pharaoh format index-labeled aligned data. 
	2. **[error-checking](scripts/error-checking)** - Scripts for error handling and analysing errors in files.
		* [error_check_alignment.py](scripts/error-checking/error_check_alignment.py) : Script for checking the percentage of error sentences in a word-aligned word-labeled Sum-Eng corpus.
	3. **[parsing](scripts/parsing)** - Scripts related to/for parsing English source data.
		* [mateparsing.py](scripts/parsing/mateparsing.py) : It is used for running mate-tools on the data to get the SRL labels for English. A python wrapper of mate-tools is used.
		* [senna_srl_english.sh](scripts/parsing/senna_srl_english.sh) : Used for obtaining SENNA's SRL parser output on the English data.
		* [fix-mate-output.py](scripts/parsing/fix-mate-output.py) : Script for extending arguments of prepositional phrases in output of mate-tools. Uses DFS(depth-first-search) to accomplish the task.
	4. **[scraping](scripts/scraping)** - Scripts for scraping data and reformating/storing it in a readable and coherent fashion.
		* [scrape-etcsl-XML.py](scripts/scraping/scrape-etcsl-XML.py) : It is used for scraping transliterations from ETCSL XML files. Reference: https://github.com/niekveldhuis/Digital-Assyriology/blob/master/Scrape-etcsl/scrape-etcsl-XML.ipynb
		* [modified-scrape-etcsl-translations-XML.py](scripts/scraping/modified-scrape-etcsl-translations-XML.py) : Modified version of the above script for scraping the translations from the ETCSL XML translations data file.

	5. **[word-embeddings](scripts/word-embeddings)** - Scripts for generating word vectors from monolingual data.
		* [make_fasttext.sh](scripts/word-embeddings/make_fasttext.sh) : Make word vectors using the FastText algorithm.
		* [make_word_vectors.py](scripts/word-embeddings/make_word_vectors.py) : Inducing word vectors using the traditional word2vec algorithms.

	6. **[processing](scripts/processing)** - Scripts for processing data and other files.
		* [create_parallel.py](scripts/processing/create_parallel.py) : Script for creating parallel aligned data from the existing XML parsed data for ETCSL. Converts the sentence transliterations to combine into paragraphs.
		* [etcsl_cdli_unifier.py](scripts/processing/etcsl_cdli_unifier.py) : Uses Ilya's script from the ```transliteration``` python class ([link here](https://github.com/cdli-gh/mtaac_cdli_ur3_corpus/blob/master/scripts/scripts_translated.py)) to normalise the tokenized data from an input file. (in this case, the ETCSL files)
		* [sentence_segment.py](scripts/processing/sentence_segment.py) : A simple heuristic to segment sentences in the CDLI English corpus - mainly used before applying mate-tools to the English data for better coverage.
		* [unicode_decode.py](scripts/processing/unicode_decode.py) : Script for normalising the english character set in the source English data.
		* [unnormalise.py](scripts/processing/unnormalise.py) : Script for removing normalisation elements from the CDLI data, and also making the parallel data ready as input for the _efmaral_ & _fast_align_ word aligners.
___
4. **[processed-data](processed-data)** - Contains all the processed data that has been used in the course of the workflow of the project.
	1. **[cdli/un-normalised](processed-data/cdli/un-normalised)** - Has the processed CDLI data which is un-normalised and also ready for use by word aligning software. A sample file is described below:
		* [sum_eng_train_unnorm.csv](processed-data/cdli/un-normalised/sum_eng_train_unnorm.csv) : Contains the input data (unnormalised) which contains side-by-side Sumerian sentences along with their English counterparts separated by ``` ||| ``` with the spaces. This format is required as input to word-aligners. 
		* ... : Other files similar to the above.
	2. **[etcsl](processed-data/etcsl)** - Contains ETCSL processed data.
		* [parallel-etcsl-eng](processed-data/etcsl/parallel-etcsl-eng) : Contains English texts arranged in paragraphs from the etcsl corpus.
		* [parallel-etcsl-sum](processed-data/etcsl/parallel-etcsl-sum) : Sumerian texts from ETCSL arranged paragraph-by-paragraph rather than line-by-line as in the original corpus.
		* [old-proc-eng](processed-data/etcsl/old-proc-eng) : Processed data for English as returned by the ETCSL scraper script.
		* [old-proc-sum](processed-data/etcsl/old-proc-sum) : Processed data for Sumerian as returned by the ETCSL scraper script. Difference is this has line-by-line transliterations along with the identification information for each text.

	3. **[unified](processed-data/unified)** - The plan is to include all unified parallel data here, for ETCSL and ETCSRI after converting to ASCII and normalising it.
		* [etcsl-transliteration-normalised.dat](processed-data/unified/etcsl-transliteration-normalised.dat) : A sample snapshot of the [unifier script](scripts/processing/etcsl_cdli_unifier.py) from above on etcsl text _c.1.1.1.txt_


	4. **[misc](processed-data/misc)** - Miscellaneous processed data. Currently contains outputs for a few sentence-combining heuristic functions for the CDLI-UrIII data.
___
5. **[outputs](outputs)** - This folder contains all the intermediate output files generated after applying the workflow processes.
	1. **[mate-parsing](outputs/mate-parsing)** : Contains outputs of SRL structure of English text via mate-tools. For both normalised and un-normalised data.
	2. **[senna-parsing](outputs/senna-parsing)** : Contains SRL structure of the English text via SENNA.
	3. **[word-alignments](outputs/word-alignments)** : Outputs containing the word-aligned Sum-Eng data. Both of the folders below contain both index-based and word-based alignments.
		* [efmaral-aligner](outputs/word-alignments/efmaral-aligner) : Word alignments induced via the efmeral aligner from https://github.com/robertostling/efmaral. Gives lesser errory alignments than fast-align.
		* [fast-align](outputs/word-alignments/fast-align) : Using fast-align (https://github.com/clab/fast_align) for the word alignments. 
	4. **[projected](outputs/projected)** : Contains SRL projected annotations for Sumerian and the error logs.
___
6. **[logs](logs)** - Contains log files of training and testing the SRL neural net system.
	
___

7. **[models](models)** - Contains the stored trained models for SRL system for Sumerian.
	1. [ubuntu_models](models/ubuntu_models) : Latest model - has stored numpy files and trained models which must be used for predicate detection. Trained on Ubuntu 16.04 system.
	2. [py3-models](models/py3-models) : Models trained with python 3.
	3. [old_trained](models/old_trained) : Old trained models. Faces errors while predicate detection.

## Progress Document

Update of the progress document of the project - contains minute details as well as comprehensive details of the challenges and the solution to many roadbloacks is being done here : https://docs.google.com/document/d/1ttPy-t14cTuVvAAnuWiOoCDEJHRfuyq9eXmpY4bnohg/edit?usp=sharing
 (Link sharing on only for mentors and admins)

## Prerequisites

What things you need to install the software and how to install them.
After installing nlpnet from https://github.com/erickrf/nlpnet, doing:
`pip install -r requirements.txt` after creating a virtualenv should be enough.

## Usage 

We use nlpnet to train our SRL system and the stored models after training are in the `models/` directory.
The latest trained model is located at `models/ubuntu_models`, which we will use below.

`nlpnet-tag.py srl --data models/ubuntu_models` will ask you to type in a sentence on the terminal.
It will tag all predicates - along with doing the argument classification.
Note: You must have nlpnet installed, otherwise this would not work.

## Contributing

Feel free to send in pull requests to us, we will be happy to incorporate meaningful changes and suggestions.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
