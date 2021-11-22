#import libraries
import cv2
import numpy as np
from openvino.inference_engine import IECore

def vehicleDetect(loc, allCoor):
    #initiate inference engine
    ie = IECore()
    net_vd = ie.read_network(
        model = 'openVINO-models/vehicle-detection-0202/vehicle-detection-0202.xml',       
        weights = 'openVINO-models/vehicle-detection-0202/vehicle-detection-0202.bin'
    )
    model_vehicle_detection = ie.load_network(net_vd,'CPU')

    #load input
    vid_raw = cv2.VideoCapture(loc)

    while (vid_raw.isOpened()):
        _, img = vid_raw.read()
        ##resize to the same height as preview frame
        def resizeImg(img, height):
            dim = None
            (h,w) = img.shape[:2]
            r = height / float(h)
            dim = (int(w*r),height)
            resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
            return resized

        img = resizeImg(img, 560)
        ##frame processing for detection
        #RGB2BGR
        imgd = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        #resize
        imgd_resized = cv2.resize(imgd,(512,512))
        #transpose
        imgd_transposed = np.transpose(imgd_resized,(2,0,1))
        #new array
        imgd_input = np.array([imgd_transposed],dtype=np.float32)

        ##inferencing solution using the model
        img_out = model_vehicle_detection.infer({'image':imgd_input})

        ##outputting solution
        #draw line(s)
        for item in allCoor:
            cv2.line(
                img,
                item[0],
                item[1],
                (255,0,0),
                3
                )
        ##draw box(es)
        for item in img_out['detection_out'][0][0]:
            height,width,_ = img.shape
            if item[2] > 0.7:
               ##detect collision line-block
                isViolating = False
                for coor in allCoor:

                    if coor[0][1] < coor[1][1]:
                            yRange = range(coor[0][1],coor[1][1])
                    elif coor[1][1] < coor[0][1]:
                        yRange = range(coor[1][1],coor[0][1])
                    else:
                        yRange = range(coor[0][1],coor[1][1] + 1)

                    for i in range(int(item[3]*width), int(item[5]*width)):
                        y = int(((coor[1][1] - coor[0][1]) * ((i - coor[0][0]) / (coor[1][0] - coor[0][0]))) + coor[0][1] )

                        if (y == int(item[6]*height)) and (y in yRange):
                            isViolating = True
                            break
                    if isViolating:
                        break
                    
                if isViolating:
                    cv2.rectangle(
                        img,
                        (int(item[3]*width), int(item[4]*height)),
                        (int(item[5]*width), int(item[6]*height)),
                        (0,0,255), 3
                    )
                else:
                    cv2.rectangle(
                        img,
                        (int(item[3]*width), int(item[4]*height)),
                        (int(item[5]*width), int(item[6]*height)),
                        (0,255,0), 3
                    )

        ##display output window
        cv2.imshow('Output',img)
        if cv2.waitKey(1) & 0xFF == ord('p'):
            cv2.imwrite('images\pauseframe.png',img)
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid_raw.release()
    cv2.destroyAllWindows()