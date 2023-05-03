
CS598 Final Project:
Author: Binbin Weng (binbinw2@illinois.edu)

How to use the `code.ipynb`:
The method I am implementing in this project is from the paper, `A disease inference method based on symptom extraction and bidirectional Long Short Term Memory networks`, which introduces a method of multi-label classifier for disease inference with clinical text data. There are several steps to do to get the results. These steps are involved in the markdown sections in the code.ipynb file. Here I list the steps, but to get the results, you need follow the instructions in the markdown sections in the `code.ipynb` file.

Step 1: Prepare the data.
In this project, two tables will be used, `NOTEEVENTS` and `DIAGNOSES_ICD`, from MIMIC-III. Please follow the instruction in the page https://physionet.org/content/mimiciii/1.4/ to download the two tables. After downloading these two tables, please save the tables to the same folder as you save the code.

Step 2: Prepare the data for Batch MetaMap.
The purpose of the original paper is to use the clinical text data to build a multi-label classifier for disease inference. The first thing needs to do is to extract symptoms from the clinical text data. It uses the techniques introduced by MetaMap to extract symptoms from the clinical text data. 
MetaMap provides a database which you can download and set up the environment for it so that you can run the extraction from your local side. I tried this method, which was very slow. It took about 25 CPU hours to extract symptoms from about 1000 records. The data contains about 50,000 records, so obviously this method is not efficient enough. But you still can try this method. Please go to the website page, https://lhncbc.nlm.nih.gov/ii/tools/MetaMap/run-locally/MainDownload.html, to download related database and follow the instructions to set up the environment.  
Luckily, MetaMap also provides the service of Batch MetaMap, where you can upload your file and it will help extract symptoms from your file and return results to you. So the part of the code after step 2 is to prepare the data which you can upload to Batch MetaMap. After running this part of code, you will see some statistics of the original datasets, and two files will be generated, `merged_data.csv` and `data_for_metamapBatch_full.txt`. The file, `merged_data.csv` is for later modeling use which contains labels for each records. The file, `data_for_metamapBatch_full.txt`, is to submit in Batch MetaMap to get the symptoms for each records.

Step 3: Upload the file `data_for_metamapBatch_full.txt` to Batch MetaMap and get symptoms.
Register an account on National Library of Medicine, https://www.nlm.nih.gov/. It may take some time to review your registration.
After your registration gets approved, go to https://ii.nlm.nih.gov/Batch/UTS_Required/MetaMap.html,Enter, enter FULL Email Address (which is used to contact you when the job is finished), upload the data_for_metamapBatch_full.txt from the previous step, in the Out/Display Options select Fielded MMI output (-N), in the Batch Specific Options select Single Line Delimited Input w/ ID, in the I would like to only use specific Semantic Types, enter `sosy,dsyn,neop,fngs,bact,virs,cgab,acab,lbtr,inpo,mobd,comd,anab`, then submit Batch MetaMap. It then will give you a link to track your job. It takes about 3 days to process the data. When the job finishes, you will receive an email containing link for the output files. Download the `text.out` file and `text.out.ERR` file to the same folder you store your other datasets.

Step 4: Prepare data for modeling.
After we get the results from Batch MetaMap, we need to process the results and merge the results with the `merged_data` that we generated in step 2 to prepare data for the modeling. The part of code after step 4 is to prepare the data, including merging the symptoms with the lables, calculating TF-IDF scores for each symptoms, building word2vec model, generating forward and backward X because we will build BiLSTMa in the later part. After running this part of code, several files will be generated,`symptom_ICD.csv`, `tfidf_matrix.csv`, `word2vec_model`. These files are saved just in case the program is stopped unexpectedly.

Step 5: Modeling, evaluating and comparing
After prepare the data for modeling, in the part of code after step 5, we will build and compare several models with the prepared data. 
The models are:
1. the bidirectional LSTM with the X representation of TF-IDF
2. the bidirectional LSTM with the X representation of word2vec
3. simply combine the results from the two models above
4. training two bidirectional LSTMs with the X representations of both TF-IDF and word2vec together
5. training two bidirectional GRUs with the X representations of both TF-IDF and word2vec together