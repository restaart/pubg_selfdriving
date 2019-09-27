
# coding: utf-8

# In[1]:


import pickle
from sklearn.linear_model import LogisticRegression
import numpy as np


with open("digit_detector.pkl",'rb') as file:
        digit_detector = pickle.load(file)

