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
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.feature_extraction.text import CountVectorizer
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import gensim
from gensim.models import Word2Vec
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from torch.utils.data import DataLoader
import csv

def select_symptoms(symptom_ICD):
    symptom_ICD['symptom_code_list'] = symptom_ICD['symptom_code'].apply(lambda x:x.split(','))
    symptom_ICD['symptom_code_list'] = symptom_ICD['symptom_code_list'].apply(lambda x:list(set(x)))
    code_num = symptom_ICD['symptom_code_list'].apply(lambda x:len(x))
    symptom_ICD['selected_symtom_code'] = [lst[:50] for lst in symptom_ICD['symptom_code_list']]
    selected_code_num = symptom_ICD['selected_symtom_code'].apply(lambda x:len(x))
    symptom_ICD=symptom_ICD[symptom_ICD['selected_symtom_code'].apply(lambda x:len(x)>=2)]
    symptom_ICD = symptom_ICD.reset_index(drop = True)
    return symptom_ICD

def select_diseases(symptom_ICD,n=50):
    symptom_ICD['icds'] = symptom_ICD['ICD_concat_CODEs'].astype(str).apply(lambda x: x.split(',')).apply(lambda y: [item[:3] for item in y])
    symptom_ICD['icds'] =symptom_ICD['icds'].apply(lambda x:list(set(x))) 
    df_exploded = symptom_ICD.explode('icds')
    common50_disease = list(df_exploded['icds'].value_counts()[:50].index)
    symptom_ICD['common50_icds'] = symptom_ICD['icds'].apply(lambda x: [item for item in x if item in common50_disease])
    symptom_ICD = symptom_ICD[symptom_ICD['common50_icds'].apply(lambda x:len(x)>0)]
    symptom_ICD = symptom_ICD.reset_index(drop = True)
    return symptom_ICD
