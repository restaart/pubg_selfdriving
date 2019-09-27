import pickle
from sklearn.linear_model import LogisticRegression
import numpy as np

import os

package_directory = os.path.dirname(os.path.abspath(__file__))

with open(package_directory + "/digit_detector.pkl",'rb') as file:
        digit_detector = pickle.load(file)

def getSpeedDigits(full_img):
    img = get_speed_img(full_img)
    digit_width = 18
    return [img[:,i*18:(i+1)*18] for i in range(3)]

def get_speed_img(full_img):
    img_x = 156
    img_y = 988
    img_width = 18*3
    img_height = 30
    speed_img = full_img[img_y:img_y+img_height,img_x:img_x + img_width][:,:,:3].mean(axis =2)
    
    if(0<=speed_img.max()<=1):
        speed_img = speed_img*255
    return (speed_img > 240).astype(np.int8)

def speed_from_image(full_img):    
    value = ("".join(digit_detector.predict(np.array([d.flatten() for d in getSpeedDigits(full_img)]))))
    return value if value!='   ' else None