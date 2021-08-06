# ICSI Dataset Preprocess

This code can be used to preprocess ICSI dataset for meeting summarization from scratch.


## 1. Get [ACL 2018](https://aclanthology.org/P18-1062/) Preprocessed Dataset
* Download files from [ACL18-code](https://bitbucket.org/dascim/acl2018_abssumm).
* Copy files **dascim-acl2018_abssumm-3ee827b34472/data/meeting/icsi/\*** to **./data/acl18-icsi/**.
* Copy files **dascim-acl2018_abssumm-3ee827b34472/data/meeting/lists/list.icsi, list.icsi.train, list.icsi.test** to **./data/**.
* Copy **develepment list** from **dascim-acl2018_abssumm-3ee827b34472/data/meeting/meeting_lists.py/icsi_development_set** to **./data/list.icsi.eval**.

## 2. Get ICSI dataset
* Download ICSI from [here](http://groups.inf.ed.ac.uk/ami/icsi/download/) and unzip it to **./data/ICSIplus**.

## 3. Process ICSI Data
* First copy stopwords from **dascim-acl2018_abssumm-3ee827b34472/resources/stopwords/meeting/filler_words.en.txt** to **./data/stop_words.txt**. Note that you should rename the file.
* Run `python icsi_preprocess.py`
> `icsi_preprocess.py` will first create output dirs **data/cleaned/train, data/cleaned/valid, data/cleaned/test**, then extract speakers and utterances from `.da` file.


## 4. Get ICSI Meeting Summary
* Run `python get_summary.py`. 
> `get_summary.py` will create a output dir **data/summary**, and extract summaries from files. Note that ICSI test files have multiple references.

## 4. Create Multi References
* Run `python create_multi_reference.py`
> `create_multi_reference.py` will first create output dir **data/reference**, and output three files **ref1.txt, ref2.txt, ref3.txt** for text files.

## 5. Final
Now, you have meetings in **data/cleaned/train, data/cleaned/valid, data/cleaned/test** and also summaries in **data/reference**.