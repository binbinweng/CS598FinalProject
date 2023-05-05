
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

def symptoms(symptoms):
    symptom_copy = symptoms
    emptyrow=symptoms[8].isnull()
    for i in range(symptoms.shape[0]):
        if emptyrow[i]:
            s = symptoms.loc[i,0].split('|')
            symptom_copy.loc[i,:len(s)-1]=s
    num_list = [str(i) for i in range(merged_data.shape[0])]
    l = []
    for i in range(symptom_copy.shape[0]):
        if symptom_copy.loc[i,0] not in num_list:
            if '\n' in symptom_copy.loc[i,0]:
                #l.append(i)
                s = symptom_copy.loc[i,0].split('\n')
                if s[1] in num_list:
                    symptom_copy.loc[i,0] = s[1]
                else:
                    l.append(i)
            else:
                l.append(i)
    symptom_copy2 = symptom_copy.drop(index = l)
    def concat_values(group):
        return pd.Series({
            'symptom_code': ','.join(group[4]),
            'symptom': ','.join(group[3])
        })
    symptoms_final = symptom_copy2.groupby(0).apply(concat_values)
    symptoms_final = symptoms_final.reset_index()
    symptoms_final = symptoms_final.rename(columns = {0:'index'})
    symptoms_final['index']=symptoms_final['index'].astype(int)
    symptoms_final = symptoms_final.sort_values(by='index')
    symptoms_final = symptoms_final.reset_index()
    symptoms_final = symptoms_final.drop('level_0',axis = 1)
    return symptoms_final