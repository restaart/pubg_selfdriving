import matplotlib.pyplot as plt
import cv2
import numpy as np
import numpy as np

def get_minimap(img):
    map_coords = (794,1626)
    map_dim = (256,256)
    return img[map_coords[0]:map_coords[0]+map_dim[0],map_coords[1]:map_coords[1]+map_dim[1]].copy()
    

def get_minimap_meters_per_pixel(minimap):
    minimap_edges = cv2.Canny(minimap, threshold1 = 100, threshold2=100)
    lines = cv2.HoughLinesP(minimap_edges,
                            rho = 1.1,
                            theta = 90*np.pi/180,
                            threshold = 125,
                            minLineLength = 200,
                            maxLineGap = 200)
    lines = lines[:,0,:]
    line_angles = np.arctan2(lines[:,2] - lines[:,0] , lines[:,1] - lines[:,3])*180/3.14
    
    vert_lines = lines[np.abs(line_angles)<0.05]
    hor_lines = lines[np.abs(line_angles-90)<0.05]
    vert_lines

    x=[]
    for xi  in np.sort(hor_lines[:,1]):
        if len(x)==0:
            x.append(xi)
        else:
            if xi - x[-1] < 10:
                x[-1] = x[-1]*0.5 + xi*0.5
            else:
                x.append(xi)

    y=[]
    for yi  in np.sort(vert_lines[:,0]):
        if len(y)==0:
            y.append(yi)
        else:
            if yi - y[-1] < 10:
                y[-1] = y[-1]*0.5 + yi*0.5
            else:
                y.append(yi)

    all_dif = np.hstack([np.diff(y),np.diff(x)])

    return 100/np.median(all_dif)

class minimap_gps(object):
    
    map_files =  {'camp_jackal' : '..\\map\\low_res\\Camp_Jackal_Main_Low_Res.png',
                  'miramar'     : '..\\map\\low_res\\Miramar_Main_Low_Res.png'}
    
    map_size_meters = {'camp_jackal' : 2000,
                       'miramar'     : 8000}
    
    def __init__(self,map_name, map_scale = 0.5):
        assert map_name in self.map_files, 'Wrong map name'
        self.map_image =(plt.imread(self.map_files[map_name])*255).astype(np.uint8)
        self.map_image = cv2.resize(self.map_image,(0,0), fx = map_scale, fy =map_scale)   
        self.map_meters_per_pixel = self.map_size_meters[map_name] / self.map_image.shape[0]
        self.player_point_img = plt.imread('player_point.jpg').astype(np.uint8)
        
    def find_template(self,img,template):
        res = cv2.matchTemplate(img,template,cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        return np.array(min_loc),min_val
    
    def get_position(self,img,return_confidence = False):
        'by full screenshot returns on-map player position in meters'
        minimap = get_minimap(img)
        scale_factor = get_minimap_meters_per_pixel(minimap)/self.map_meters_per_pixel
        scaled_minimap  =  cv2.resize(minimap,(0,0), fx = scale_factor, fy =scale_factor)

        player_offset = self.find_template(minimap,self.player_point_img)[0] + np.array([7,7])
        
        minimap_pos,conf =  self.find_template(self.map_image,scaled_minimap)
        
        player_position = minimap_pos + player_offset*scale_factor
        
        if return_confidence:
            return player_position*self.map_meters_per_pixel,1-conf
        else:
            return player_position*self.map_meters_per_pixel
        