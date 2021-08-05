# AMI Dataset Preprocess

This code can be used to preprocess AMI dataset for meeting summarization from scratch.

## 1. Get [ACL 2018](https://aclanthology.org/P18-1062/) Preprocessed Dataset
* Download files from [ACL18-code](https://bitbucket.org/dascim/acl2018_abssumm).
* Copy files **dascim-acl2018_abssumm-3ee827b34472/data/meeting/ami/\*** to **./data/acl18-ami/\***.
* Copy files **dascim-acl2018_abssumm-3ee827b34472/data/meeting/lists/list.ami, list.ami.train, list.ami.eval, list.ami.test** to **./data/\**.
> Now, you will have **data/acl18-ami/\***, **data/list.ami**, **data/list.ami.train**, **data/list.ami.eval** and **data/list.ami.test**

## 2. Get AMI Dataset
* Download the AMI dataset from [AMI manual annotations v1.6.2 ](http://groups.inf.ed.ac.uk/ami/download/) and unzip it to **./data/**. Finally you can get **./data/ami_public_manual_1.6.2/\***, which contains original AMI files.
* Run `python delete_useless_files.py`
> `python delete_useless_files.py`: Following previous setting, we only use part of the meeting files, so we first filter out useless files. This script is used to extract **words**, **topics** and **summaries** according to the useful file list **./data/list.ami**. Output files are in **data/ami/words, data/ami/summary, data/ami/topics**

## 3. Process AMI Data
* Run `python ami_preprocess.py`, results are shown in **data/ami/train, data/ami/valid, data/ami/test**
> `python ami_preprocess.py` will first create dirs **train,valid,test** under **data/ami/** and then extract speaker, time, utterance, topic from **data/ami/words** and **data/ami/topics**, in each line, the data format is **speaker \t time \t utterance \t topic**.

## 4. Clean Data
* First copy stopwords from **dascim-acl2018_abssumm-3ee827b34472/resources/stopwords/meeting/filler_words.en.txt** to **data/ami/stop_words.txt**. Note that you should rename the file.
* Run `python create_clean_data.py`.
> `create_clean_data.py` will first creat output dirs **cleaned**, **cleaned/train**, **cleaned/valid**, **cleaned/test** at **data/ami/**, then clean utterances.

## 5. Get AMI Meeting Summary
* Run `python get_summary.py`. 
> `python get_summary.py` will create a output dir **data/ami/final_summary** and extract the summary from xml files for each meeting.

## 6. Final
Now, you have meetings in **data/ami/train, data/ami/valid, data/ami/test** and also summaries in **data/ami/final_summary**.