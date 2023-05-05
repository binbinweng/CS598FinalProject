import os
import pickle
import random
import numpy as np
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import time
import re
import pandas as pd

def text_processing(text):
    text = re.sub('\n', ' ', text)
    text = re.sub('\[[^\]]*\]', ' ', text)
    text = re.sub('\s+', ' ', text.strip())
    negations = ['no', 'not', 'never', 'none', 'nobody', 'nothing', 
                 'neither', 'nor', 'nowhere', 'cannot', 'can\'t', 
                 'doesn\'t', 'don\'t', 'won\'t', 'shouldn\'t', 
                 'couldn\'t', 'wouldn\'t', 'isn\'t', 'aren\'t', 'wasn\'t', 
                 'weren\'t', 'didn\'t', 'hadn\'t', 'hasn\'t', 'haven\'t',
                 'denies', 'without','denied']
    adv_conjs = ['but','yet','however','nevertheless','still','on the other hand',
                 'in contrast','in contrast','notwithstanding','although','despite that',
                 'even though', 'in spite of','nonetheless', 'despite']
    negation_pattern = "(?:" + "|".join(negations) + ")"
    adv_conj_pattern = "(?:" + "|".join(adv_conjs) + ")"
    regex = r'\b(' + '|'.join(negations) + r')\b\s*(.*?)\s*(?=\b(' + '|'.join(adv_conjs) + r')\b|\.|$)'
    text = re.sub(regex, "", text, flags=re.IGNORECASE)
    text = " ".join(word for word in text.split() if word.lower() not in stop_words)
    text = re.sub('\s+', ' ', text.strip())
    return text

def processing_text_for_MetaMap(t1,t2):
    merged_data = pd.merge(t1,t2,on = 'HADM_ID',how = 'inner')
    merged_data['processed_text']=merged_data['TEXT_concat'].apply(text_processing)
    merged_data.to_csv('merged_data.csv',index = False)
    data_for_metamapBatch = merged_data.loc[:,['processed_text']]
    for i in range(merged_data.shape[0]):
        data_for_metamapBatch['processed_text'][i] = str(i)+'|'+data_for_metamapBatch['processed_text'][i]
    data_for_metamapBatch.to_csv('data_for_metamapBatch_full.txt',sep = '\n',index = False,header = False)