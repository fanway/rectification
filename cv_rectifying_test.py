import numpy as np
import cv2

# Load an color image in grayscale
img = cv2.imread('windy.png',0)

#cv2.waitKey(0)
#cv2.destroyAllWindows()

lines = []
coords = []
i = 0

# mouse callback function
def mouse_callback(event,x,y,flags,param):
    global i, coords, lines
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,y)
        cv2.circle(img, (x,y), 5, (0,255,0), -1)
        if len(lines) < 4:
            if i % 2 == 0:
                print("Select second point to complete the line")
                coords = [x,y,1]
            if i % 2 == 1:
                print("Line added")
                #l_coords = np.array(list((x-y for x,y in zip((x,y), coords))))
                print(f'coords: {coords}')
                l_coords = cross_product([[x,y,1], coords])
                l_coords = np.reshape(l_coords, (1, 3))
                print(f'lcoords before normalization: {l_coords}')
                #l_coords[0,0] //= l_coords[0,2]
                #l_coords[0,1] //= l_coords[0,2]
                #l_coords[0,2] //= l_coords[0,2]
                #l_coords[0,2] = 1
                print(f'lcoords after normalization: {l_coords}')                
                lines.append(l_coords)
                print(lines)
            i += 1

def cross_product(lines):
    return np.cross(lines[0], lines[1])



w, h = 1024, 768
cv2.namedWindow('image', cv2.WINDOW_NORMAL) # Can be resized
#cv2.resizeWindow('image', w, h) #Reasonable size window
cv2.setMouseCallback('image', mouse_callback) #Mouse callback
while True:
    cv2.imshow('image', img)
    k = cv2.waitKey(0) & 0xFF
    if k == 113:
        break
    vp1 = cross_product([lines[0], lines[1]]) if len(lines) == 4 else None
    vp2 = cross_product([lines[2], lines[3]]) if len(lines) == 4 else None
    vp_line = cross_product([vp1, vp2]) if len(lines) == 4 else None
    print(vp_line)
    if vp_line is not None:
        scale = 1
        #vp1, vp2 = vp[0,0]//(vp[0,2]*scale), vp[0,1]//(vp[0,2]*scale)
        #cv2.circle(img,(vp1, vp2), 10, (0,255,0), -1)
        H = np.identity(3)
        H[2,0], H[2,1] = vp_line[0, 0] / vp_line[0, 2], vp_line[0, 1] / vp_line[0, 2]
        print(H)
        img = cv2.warpPerspective(img, H, (img.shape[1], img.shape[0]))

cv2.destroyAllWindows()