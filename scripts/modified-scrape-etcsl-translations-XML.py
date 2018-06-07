# Modified for English translations : June 2018, Bakhtiyar Syed 
# Rest of the header is for original attribution.
# coding: utf-8
# Usage: Use the .ipynb files in the subfolder above.

# # Formatting ETCSL TEI XML files
# ## Introduction
# 
# The Electronic Text Corpus of Sumerian Literature ([ETCSL](http://etcsl.orinst.ox.ac.uk) 1998-2006) provides editions and translations of some 400 Sumerian literary texts. Goal of this Notebook is to format the ETCSL data in such a way that the (lemmatized) texts are made available for computational text analysis. In order to make the data compatible with output scraped from [ORACC](http://oracc.org), the Notebook ETCSL-to-EPSD2 should be run after running the current scraper.
# 
# For most purposes you do not need to run this scraper, because the final output is made available to you. However, if you need output in a different format or if you wish to know how the output was produced, you may read, adapt, and run this Notebook.
# 
# The original [ETCSL](http://etcsl.orinst.ox.ac.uk) files in TEI XML are available upon request from the [Oxford Text Archive](http://ota.ox.ac.uk/desc/2518). Note the following description on the OTA site:
# 
# > ## The Electronic Text Corpus of Sumerian Literature. Revised edition.
# 
# > ### Editor	
# > Cunningham, Graham (ed.); Ebeling, Jarle (ed.); Black, Jeremy (deceased) (ed.); Flückiger-Hawker, Esther (ed.); Robson, Eleanor (ed.); Taylor, Jon (ed.); Zólyomi, Gábor (ed.)
# 
# > ### Availability	
# > Use of this resource is restricted in some manner. Usually this means that it is available for non-commercial use only with prior permission of the depositor and on condition that this header is included in its entirety with any copy distributed.
# 
# The [manual](http://etcsl.orinst.ox.ac.uk/edition2/etcslmanual.php) of the ETCSL project explains in full detail the editorial principles and the technical details. According to the manual the ETCSL data are freely available and the XML source files can be downloaded.
# 
# The TEI XML source files were sent to me by the Oxford Text Archive upon request September 3rd 2015. Any (non-commercial) re-use of the data produced in this Notebook should reproduce the header quoted above ('Editor' and 'Availability') and is understood to be licensed under a [Creative Commons Share Alike](http://creativecommons.org/licenses/by-nc-sa/4.0/) license.
# 
# 

# # The Scraper
# 
# This scraper expects the following files:
# 
# 1. Directory Input
#   * etcsl.txt  a list of ETCSL text numbers
# 2. Directory ../etcsl/transliterations/
#   * This directory should contain the ETCSL TEI XML files.
# 3. Directory Equivalencies
#   * ampersands.txt a list of HTML entities and their unicode equivalents
#   * version_equivalencies.txt a list of ETCSL version names with their abbreviated forms.
# 
# The output is saved in the `Output` directory as a set of .txt files.

# ## 1. Setting Up
# First import the proper packages: 
# 
# - re: Regular Expressions
# - StringIO: enable treating strings as files (used for ElementTree)
# - os: enable Python to perform basic Operating System functions (such as making a directory)
# - ElementTree: read and analyze an XML file as an ordered tree
# - time: allows the program to 'sleep' for a brief period
# - tqdm: creates a progress bar
# 
# If you installed Python 3 and Jupyter by installing the [Anaconda Navigator](https://www.continuum.io/downloads), then most of these packages should already be installed, with the exception of tqdm. The first line in the cell below installs tqdm. It needs to be installed just once, after installing it you may invalidate that line by putting a # in front of it.

# In[1]:


get_ipython().system(u' pip install tqdm')
import re
import xml.etree.ElementTree as ET
from io import StringIO
import os
import time
from tqdm import *


# ## 2. Text Preparation 1: HTML-entities
# The ETCSL TEI XML files are written in ASCII and represent special characters (such as š or ī) by a sequence of characters that begins with & and ends with ; (e.g. &c; represents š). These so-called HTML entities are used in translation, bibliography, and introductory text, but not in the transliteration of the Sumerian text itself (see below). The entities are for the most part project-specific and are declared and described elsewhere in the ETCSL file set. The ElementTree package cannot deal with these entities and thus we have to replace them with the actual (unicode) character that they represent, before feeding the data to ElementTree. 
# 
# All the entities are listed with their corresponding unicode character (or expression) in the file `Input/ampersands.txt` separated by a space:
# 
#     &aacute; á
#     &aleph; ʾ
#     &amacr; ā
#     &ance; {anše}
#     etc.
#     
# in the main process (below 11) the file `ampersands.txt` is read and made into the Python dictionary `findreplace` in which each of the HTML entities is a key, with its unicode equivalent as value. The function `ampersands()` uses this dictionary for a search-replace action.
# 
# The function `ampersands()` is called in `parsetext()` before the ElementTree is built. Note that the .xml files themselves are not changed by this process (or by any other process in this Notebook).

# In[2]:


def ampersands(x):
    for amp in findreplace:
        x = x.replace(amp, findreplace[amp])
    return x


# ## 3. Text Preparation 2: Transliteration Conventions
# 
# Transliteration of Sumerian text in ETCSL TEI XML files uses **c** for **š**, **j** for **ŋ** and regular numbers for index numbers. The function `tounicode()` replaces each of those. For example **cag4** is replaced by **šag₄**. This function is called in the function `getword()` to format citation forms and forms (transliteration). The function `tounicode` uses the dictionary `ascii_unicode` which is defined in the main process (below 11).

# In[3]:


def tounicode(x):
    for char in ascii_unicode:
        x = x.replace(char, ascii_unicode[char])
    return x


# ## 4. Text Preparation 3: Removing 'Secondary Text'
# 
# The ETCSL web pages include variants, indicated as '(1 ms. has instead: )', with the variant text enclosed in curly brackets. Two types of variants are distinguished: 'additional text' and 'secondary text'. 'Additional text' refers to a line that appears in a minority of sources (often in only one). 'Secondary text' refers to variant words or variant lines that are found in a minority of sources. The function `secondary()` removes the words of 'secondary text' but leaves the 'additional text' in place. 
# 
# In ETCSL TEI XML secondary text is introduced by a tag of the type:
# 
# > `<addSpan to="c141.v11" type="secondary"/>`
# 
# The number c141 represents the text number in ETCSL (in this case Inana's Descent, text c.1.4.1). The return to the primary text is indicated by a tag of the type:
# 
# > `<anchor id="c141.v11"/>`
# 
# Note that the `id` attribute in the `anchor` tag is identical to the `to` attribute in the `addSpan` tag.
# 
# The function `secondary()` uses regular expressions to identify and remove the Sumerian words and lines between those tags. The DOTALL flag (in re.DOTALL) allows the search in the regular expression to continue over multiple lines.
# 
# The function `secondary()` is called by the function `parse()` (see below, section 8). If you prefer to have both primary and secondary text in your data set, simply remove (or invalidate) the line `xmltext = secondary(xmltext)` in the function `parse()`. Alternatively, remove the '#' before `return xmltext` in the function `secondary()`. As a result the function will return the variable `xmltext` without altering anything.

# In[4]:


def secondary(xmltext, textid):
    #return xmltext
    textid = textid.replace('.', '')
    find = re.compile('(<addSpan to=("' + textid + '.v[0-9]{1,3}") type="secondary"/>.*?<anchor id=\\2/>)', re.DOTALL)
    word = re.compile('<w .*?</w>', re.DOTALL) # identify a single word in "secondary text"
    line = re.compile('<l .*?</l>', re.DOTALL) # identify an entire line of "secondary text"
    secondary = re.findall(find, xmltext) # make a list of "secondary text" passages
    secondary = [second[0] for second in secondary] #findall creates a list of tuples; take the first of each tuple
    noword = [re.sub(word, '', instance) for instance in secondary] # remove the single secondary words from each "secondary" passage
    noline = [re.sub(line, '', instance) for instance in noword] #remove entire secondary lines from each "secondary" passage
    for idx, val in enumerate(secondary): # swap the original "secondary" passage for the one without words and lines.
        xmltext = xmltext.replace(val, noline[idx])
    return xmltext


# ## 5. Format Output
# 
# The function `outputformat()` defines what the output of the lemmatized forms will look like. This function may be adapted in various ways to produce different types of output. The function takes a dictionary as input with the following keys: lang (Language), citform (Citation Form), guideword (Guide Word), pos (Part of Speech), and form (transliteration). In the standard format the output will look like: sux:lugal[king]N. One may adapt the output, for instance, by omitting the element lang (lugal[king]N) or by selecting for certain parts of speech, or for certain language codes. For instance:
# 
#     if output['pos'] == 'N':
#         output_formatted = output['citform'] + "\t" + output['guideword']
# 
# This will create output in the form lugal   king (lugal and king seperated by TAB), selecting only Nouns.
# 
#     if output['lang'] == 'sux-x-emesal':
#         output_formatted = output['citform'] + "[" + output['guideword'] + "]" + output['pos']
# 
# This will create output in the form suba[shepherd]N, selecting only Emesal words.
# In order to select both Sumerian (sux) and Emesal (sux-x-emesal) forms one could use:
# 
#     if output['lang'][0:3] == 'sux':
# 

# In[5]:


def outputformat(output):
    output_formatted = ''
    output_formatted = output['form']
    return output_formatted


# ## 6. Formatting Words
# 
# A word in the ETCSL files is represented by a number of nodes in the XML tree that identify the form (transliteration), citation form, guide word, part of speech, etc. The function `getword()` formats the word as closely as possible to the ORACC conventions. Three different types of words are treated in three different ways: Proper Nouns, Sumerian words and Emesal words.
# 
# In ETCSL **proper nouns** are nouns, which are qualified by a 'type' (Divine Name, Personal Name, Geographical Name, etc.; abbreviated as DN, PN, GN, etc.). In ORACC a word has a single POS; for proper nouns this is DN, PN, GN, etc. - so what is 'type' in ETCSL becomes POS in ORACC. ORACC proper nouns usually do not have a guide word (only a number to enable disambiguation of namesakes). The ETCSL guide words ('label') for names come pretty close to ORACC citation forms. Names are therefore formatted differently from other nouns.
# 
# **Sumerian words** are treated in basically the same way in ETCSL and ORACC, but the citation forms and guide words are often different. Transformation of citation forms and guide words to ORACC (epsd2) standards takes place in the Notebook ETCSL-toEPSD2. This harmonization process uses a set of dictionaries (prepared by Niek Veldhuis and Terri Tanaka) that record ETCSL to EPSD2 equivalencies.
# 
# **Emesal words** in ETCSL use their Sumerian equivalents as citation form ('lemma'), adding a separate node ('emesal') for the Emesal form proper. This Emesal form is the one that is used as citation form in the output.
# 
# Guide words need removal of commas and spaces. Removal of commas will allow the output files to be read as Comma Separated Value (csv) files, which is an efficient input format for processes in Python and R. In the output file commas separate different fields from each other (text ID, text name, line number and text). Spaces need to be removed because standard tokenizers will understand spaces as word dividers. 

# In[6]:


def getword(node):
    if node.get('pos'):
        pos = node.get('pos')
    else:
        pos = 'X'
    citform = node.get('lemma')
    guideword = node.get('label')
    form = node.get('form')
    form = tounicode(form)
    if node.get('emesal'):
        citform = node.get('emesal')
        lang = "sux-x-emesal"
    else:
        lang = "sux"
    if pos != 'NU':
        citform = tounicode(citform)
    if node.get('type') and pos == 'N':
        if node.get('type') != 'ideophone':
            pos = node.get('type')
            citform = node.get('label')
            guideword = '1'

    guideword = guideword.replace(",", ";") #remove commas from guide words (replace by semicolon) to prevent
                                            #problems with processing of the csv format
    guideword = guideword.replace(" ", "-") #remove spaces from guide words (replace by hyphen). Spaces
                                            #create problems with tokenizers in computational text analysis.

    return {'lang': lang, 'citform':citform, 'guideword':guideword, 'pos':pos, 'form':form}


# ## 7. Formatting Lines
# 
# Each line consist of a series of words. The function `getline()` iterates over a line, taking one word at a time. The words and their various features (language, citation form, guideword, part of speech and form) are retrieved calling the function `getword()`, which returns a dictionary. This dictionary is forwarded to the function `outputformat()` for formatting.
# 
# In its current form the function skips words that have no Part of Speech tag. These are words that are damaged, or unknown or have not been lemmatized for some other reason. If you wish to include these words, remove the condition `if node.get('pos'):` The function should then look like this:
# 
# ```python
# def getline(lnode, line):
#     wordsinline = []
#     for node in lnode.iter('w'):
#         output = getword(node)
#         output_formatted = outputformat(output)
#         wordsinline.append(output_formatted)
#     line = line + ' '.join(wordsinline) + '\n'
#     return line
# ```
# 
# The function `getword()` will supply the Part of Speech 'X' to each word that has no POS tag already.

# In[7]:


def getline(lnode, line):
    wordsinline = [] #initialize list for the words in this line
    for node in lnode.iter('w'):
        if node.get('pos'): #if the Part of Speech node is absent, the word is not lemmatized
                                        # (unknown or damaged word) and is skipped
            output = getword(node)
            output_formatted = outputformat(output)
            wordsinline.append(output_formatted)
    line = line + ' '.join(wordsinline) + '\n'
    return line


# ## 8. Sections
# 
# Some compositions are divided into **sections**. That is the case, in particular, when a composition has gaps of unknown length. 
# 
# The function `getsection()` is called by `getcversion()` and receives three arguments: `tree` (an ElementTree object), `line_prefix` (which contains textid and the text name, and version name where applicable), and `csvformat` (which contains the header of the output CSV file). The function `getsection` checks to see whether a sub-division into sections is present. If so, it iterates over these sections. Each section (or, if there are no sections, the composition/version as a whole) consists of series of lines. The function `getline()` is called to request the contents of each line. The function returns the variable `csvformat`, which contains the formatted data.

# In[8]:


def getsection(tree,line_prefix, csvformat):
    
    sections = tree.find('.//div1')
    if sections != None: # if the text is not divided into sections - skip to else:
        for snode in tree.iter('div1'):
            section = snode.get('n')
            for lnode in snode.iter('p'):
                #line = getline(lnode, line)
                text = (''.join(lnode.itertext()))
                text= text.strip()
                text = text.replace('\n', ' ')
                line = line_prefix + '\t' + section + lnode.get('n') + '\t'
                line = line + text + '\n'
                csvformat = csvformat + line
    else:
    
        for lnode in tree.iter('p'):
            if (lnode.get('n')==None):
                continue
            text = (''.join(lnode.itertext()))
            text= text.strip()
            text = text.replace('\n', ' ')
            #print (lnode.get('n'))

            line = line_prefix + '\t' + lnode.get('n') + '\t'
            #line = getline(lnode, line)
            #print (line)
            #print (lnode.text)
            line = line + text + '\n'
            #print (line)
            csvformat = csvformat + line
    return csvformat


# ## 9. Versions
# 
# In some cases an ETCSL file contains different versions of the same composition. The versions may be distinguished as 'Version A' vs. 'Version B' or may indicate the provenance of th version ('A version from Urim' vs. 'A version from Nibru'). In the edition of the proverbs the same mechanism is used to distinguish between numerous tablets (often lentils) that contain just one proverb, or a few, and are collected in the files "Proverbs from Susa," "Proverbs from Nibru," etc. (ETCSL c.6.2.1 - c.6.2.5).
# 
# The function `getversion()` is called by the function `parse()` and receives three arguments: `tree` (an ElementTree object), `line_prefix` (which contains the textid and the text name), and `csvformat` (which contains the header of the output CSV file). The function checks to see if versions are available in the file that is being parsed. If so, the function iterates over these versions while adding the version name to the variable `line_prefix`. If there are no versions, the version name is left empty. The parsing process is continued by calling `getsection()` to see if the composition/version is further divided into sections.

# In[9]:


def getversion(tree, line_prefix, csvformat):
    versions = tree.find('.//head')
    if versions != None: # if the text is not divided into versions - skip 'getversion()':
        for vnode in tree.iter('body'):
            version = vnode.find('head').text
            version = equiv_dic[version]
            line_pr = line_prefix + '\t' + version
            csvformat = getsection(vnode, line_pr, csvformat)
    else:
        version = ''
        line_pr = line_prefix + '\t' + version
        #print (line_pr)
        csvformat = getsection(tree, line_pr, csvformat)
    return csvformat


# ## 10. Parse a Text
# 
# The function `parsetext()` takes one xml file (a composition in ETCSL) and parses it, calling a variety of functions defined above. The function returns the variable `csvformat`. It contains a line-by-line representation of the text with version label (where applicable), line numbers (including section labels, where applicable) and all the lemmatized words.
# 
# The parsing is done by the ElementTree (ET) package. ET.parse expects a file, but instead it receives a variable here (`xmltext`). The function `StringIO()` allows a string to be treated as a file.

# In[10]:


def parsetext(textid):
    csvformat ='id_text\ttext_name\tversion\tl_no\ttext\n' #initialize output variable
    with open('translations/' + textid + '.xml') as f:
        xmltext = f.read()
    xmltext = ampersands(xmltext)
    #print (xmltext[10:25])
    #xmltext = secondary(xmltext, textid)
    
    tree = ET.parse(StringIO(xmltext))
    name = tree.find('.//title').text
    foreign = tree.find('.//title/foreign') #some titles have children with <foreign> tag for Sumerian words
    if foreign != None:
        name = name + foreign.text + foreign.tail
    name = name.replace(' -- an English prose translation', '')
    name = name.replace(',', '')
    line_prefix = textid + '\t' + name
    #print (line_prefix)
    
    csvformat = getversion(tree, line_prefix, csvformat)

    return csvformat


# ## 11. Main Process
# 
# The code below opens a file `etcsl.txt` (in the directory `Input`) which contains all the numbers of ETCSL compositions (such as c.1.1.4). For each such number the corresponding xml file is opened and the content of the file is sent to the function `parsetext()`. `Parsetext()` returns the variabe `csvformat` which contains the formatted text. This is saved in the `Output` directory with a .txt extension. The main process also creates a dictionary, equiv_dic, which contains version names and abbreviated version names. This dictionary is used in the function `getversion()`(see above 9. Versions).

# In[11]:


with open("Input/etcsl-translated.txt", "r") as f:
    textlist = f.read().splitlines()
if not os.path.exists('Output-translated'):
    os.mkdir('Output-translated')

ascii_unicode = {'1':'₁', '2':'₂', '3':'₃','4':'₄', '5':'₅', '6':'₆', '7': '₇','8': '₈','9': '₉','0': '₀',
                     'x': 'ₓ','j': 'ŋ', 'J':'Ŋ','c': 'š','C': 'Š' }
findreplace = {}
equiv_dic = {}
    
with open("Equivalencies/ampersands.txt", 'r', encoding='utf8', errors='replace') as amp:
    ampersands_l = amp.read().splitlines()
for line in ampersands_l:
    amp = line.split(' ')[0]
    uni = line.split(' ')[1]
    findreplace[amp] = uni
    
with open('Equivalencies/version_equivalencies.txt', 'r', encoding='utf8', errors='replace') as g:
    v_equiv = g.read().splitlines()
    for equiv in v_equiv:
        version = equiv.split('; ')[0]
        abbrev = equiv.split('; ')[1]
        equiv_dic[version] = abbrev

for eachtextid in tqdm(textlist):
    csvformat = parsetext(eachtextid)
    outputfile = '../../Semantic-Role-Labeler/inputs/processed-etcsl-eng/' + eachtextid + '.txt'
    with open(outputfile, mode = 'w', encoding='utf8', errors='replace') as writeFile:
        writeFile.write(csvformat)  

