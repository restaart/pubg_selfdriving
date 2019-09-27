import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.linear_model import LogisticRegression
import pickle

with open('azimut_digit_detector_clf.plk', 'rb') as f:
    azimut_digit_detector_clf = pickle.load(f)

with open('azimut_percise_detector_clf.plk', 'rb') as f:
    azimut_percise_detector_clf = pickle.load(f)
    
def preprocess(img):
    if img.max()>1:
        return (img/255).flatten()
    else:
        return img.flatten()
    
def get_azimut_digits(azimut_img,two_digit=False):
    if two_digit:
        return [(azimut_img[:,5:25][:,i*10:i*10+10][:,:,[0,1,2]].mean(axis=2)) for i in range(2)]
    else:
        return [(azimut_img[:,i*10:i*10+10][:,:,[0,1,2]].mean(axis=2)) for i in range(3)]
    
def get_azimut_image(img):
    return img[57:73,945:975]

def azimuth_from_image(img):
    digits = [preprocess(digit) for digit in get_azimut_digits(get_azimut_image(img))]
    preds = azimut_digit_detector_clf.predict(digits)
    if 'two-digit' in preds:
        preds = azimut_digit_detector_clf.predict([preprocess(digit) for digit in get_azimut_digits(img,two_digit=True)])
    replace_vals = dict(zip([' N ','NE',' E ','SE',' S ','SW',' W ','NW',' N '],
                            [ '0', '45','90','135','180','225','270','315','360']))
    pred = ''.join(preds)
    if pred in replace_vals:
        pred = replace_vals[pred]
        
    percise_img = img[20:73,910:1010][25:30,50:96][:,:,[0,1,2]].mean(axis=2).flatten()
    if percise_img.max()<=1:
        percise_img = percise_img*255
    percise_pred = azimut_percise_detector_clf.predict([percise_img])
    pred = int(pred)
    pred = pred//15 * 15
    pred_shift = (percise_pred[0]/22.5)
    if pred_shift >= 13:
        pred = pred-15
    return pred + pred_shift