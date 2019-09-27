import pickle
from sklearn.linear_model import LogisticRegression
import numpy as np


with open("digit_detector.pkl",'rb') as file:
        digit_detector = pickle.load(file)

def getSpeedDigits(full_img):
    img = (full_img[987:1019,150:205].mean(axis =2) > 240).astype(np.int8)
    return [img[:,:16],img[:,17:33],img[:,35:51]]

def speed_from_image(full_img):    
    value = ("".join(digit_detector.predict(np.array([d.flatten() for d in getSpeedDigits(full_img)]))))
    return value if value!='   ' else None