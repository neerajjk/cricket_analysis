import matplotlib.pyplot as plt
import cv2
import numpy as np
import os
import pandas as pd
vid = cv2.VideoCapture('/content/test.mp4')

# video = cv2.VideoCapture(0)

if (vid.isOpened() == False): 
    print("Error reading video file")
  
# We need to set resolutions.
# so, convert them from float to integer.
frame_width = int(vid.get(3))
frame_height = int(vid.get(4))
   
size = (frame_width, frame_height)

out = cv2.VideoWriter('filename.avi', cv2.VideoWriter_fourcc(*'MJPG'),10, size)

def get_iou(boxA, boxB):
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])
	xB = min(boxA[2], boxB[2])
	yB = min(boxA[3], boxB[3])
	# compute the area of intersection rectangle
	interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
	# compute the area of both the prediction and ground-truth
	# rectangles
	boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
	boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

	iou = interArea / float(boxAArea + boxBArea - interArea)
	# return the intersection over union value
	return iou

def maxx(x,y,z):
  if (x>y) and (x>z):
    maximum= x
  elif (y>x) and (y>z):
    maximum = y
  elif (z>x) and (z>y):
    maximum = z
  return maximum

# idx="1"
blcnt=1
df= pd.DataFrame(columns=['ball count', 'hit/miss'])
# df = pd.read_csv("/content/hit.csv", sep=',', encoding="utf-8")

while(vid.isOpened()):
  #ab
  ret, frame = vid.read()
  if ret == False:
    break

  dh, dw = frame.shape[0], frame.shape[1]

  # print("dvkz")

  files=os.listdir('/content/yolov5/runs/detect/exp/labels')
  for a in files:
    # print(type(a))
    # for id in range(25,50):
    #   st="txt_"+str(id)
      # f1=open('/content/yolov5/runs/detect/exp/labels/'+st, 'r')
    f1=open('/content/yolov5/runs/detect/exp/labels/'+a, 'r')
       
    data = f1.readlines()
    f1.close()
    _0=0
    _1=0
    # print(list)
    blcnt=1
    for j in data:
      _, x, y, w, h = j.split(' ')
   
      
      if _==str(0):
        _0=1
        #bat
        l = int((float(x) - float(w) / 2) * dw)
        r = int((float(x) + float(w) / 2) * dw)
        t = int((float(y) - float(h) / 2) * dh)
        b = int((float(y) + float(h) / 2) * dh)
        
        if l < 0:
            l = 0
        if r > dw - 1:
            r = dw - 1
        if t < 0:
            t = 0
        if b > dh - 1:
            b = dh - 1

        cv2.rectangle(frame, (l, t), (r, b), (0, 0, 255), 1)
        # a = Bbox([l,t,r,b])

        b1=[l,t,r,b]  

        cv2.rectangle(frame,(l,t),(r,b-int((b-t)*0.7)),(0.10,255),2)#upper
    
        cv2.rectangle(frame,(l,t+int((b-t)*0.3)),(r,b-int((b-t)*0.3)),(0.10,255),2) #mid
        cv2.rectangle(frame,(l,t+int((b-t)*0.7)),(r,b),(0.10,255),2)  # lower
    
   
        bat1=[l,t,r, b-int((b-t)*0.7)]  #up

        bat2=[l,t+int((b-t)*0.3),r,b-int((b-t)*0.3)] #mid
        
        bat3=[l,t+int((b-t)*0.7),r,b]  #low
        # print("bat")
     
      elif _==str(1):
        _1=1
       
        l = int((float(x) - float(w) / 2) * dw)
        r = int((float(x) + float(w) / 2) * dw)
        t = int((float(y) - float(h) / 2) * dh)
        b = int((float(y) + float(h) / 2) * dh)
        
        if l < 0:
            l = 0
        if r > dw - 1:
            r = dw - 1
        if t < 0:
            t = 0
        if b > dh - 1:
            b = dh - 1

        cv2.rectangle(frame, (l, t), (r, b), (0, 0, 255), 1)
        b2=[l,t,r,b] 
        # print("ball")
        # b = Bbox([l,t,r,b])
        
        
#   out.write(frame)        
# vid.release()
# out.release()     
      if _0==1 and _1==1:
        upbat= get_iou(bat1,b2)
        midbat=get_iou(bat2,b2)
        lowbat=get_iou(bat3,b2)
        
        # if(upbat>0):
        #   df.loc[df.index.max()+1] = [blcnt, 'upper' ] 
        #   print("upper")
        #   blcnt=blcnt+1
        # elif(midbat>0):
        #   df.loc[df.index.max()+1] = [blcnt, 'mid' ] 
        #   print('mid')
        #   blcnt=blcnt+1
        # elif(lowbat>0):
        #   df.loc[df.index.max()+1] = [blcnt, 'lower' ] 
        #   print('lower')
        #   blcnt=blcnt+1
        


          #  if((ab>0.1 and ab<=1.0)or(cd>0.1 and cd<=1.0)or(ef>0.1 and ef<=1.0)):
            
        largest=max(upbat,midbat,lowbat)
        if (largest==upbat):
              df.loc[df.index.max()+1] = [blcnt, 'upper' ] 
              # print("upper")
        elif (largest==midbat):             
              df.loc[df.index.max()+1] = [blcnt, 'mid' ] 
              # print("mid")
        if (largest==lowbat):        
              df.loc[df.index.max()+1] = [blcnt, 'lower' ] 
              # print("low")
       
      df.to_csv('/content/hit.csv',index=False)    
      